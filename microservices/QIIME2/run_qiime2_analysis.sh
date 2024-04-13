#!/bin/bash

#set mode to exit script if error occurs
set -o pipefail -e

#read db path from qiime2config.yml
config_path="/script/qiime2config.yml" # path in Docker container 
db_path=$(yq -r .database $config_path)

filename=$1
result_filename=$2

#check if filename is file or directory 
if [[ -d $filename ]]; then
    dir=$filename
elif [[ -f $filename ]]; then
    dir="$(dirname "${filename}")"
else
    echo "$filename is not valid"
    exit 1
fi

#switch to fastq subdirectory
parent_dir=$dir
dir=$dir"/fastq/"

result_filename=$result_filename"/"

#create directory
mkdir -p $result_filename

#list all files in directory for creating the metadata file 
allfiles=$(find $dir -maxdepth 1 -type f -printf "%f;")
IFS=';' read -ra allfiles_array <<< "$allfiles"

for val in "${allfiles_array[@]}"
do 
  IFS='_' read -ra name_parts <<< "$val"
  sampleIDs+=($name_parts) #first part is the sample name 
done

#get unique sampleIDs
uniqueIDs=($(printf "%s\n" "${sampleIDs[@]}" | sort -u))


#if there is already a metadata file in the input directory, created by the user 
if [[ -f ${parent_dir}"/metadata.tsv" ]]; then
  echo "- metadata file detected"
  cp ${parent_dir}"/metadata.tsv" ${result_filename}"metadata.tsv"
  echo "-- metadata file copied"
else
  echo "- preparing creation of metadata file"
  #write metadata.tsv
  echo -e "sampleid" > $result_filename"metadata.tsv"
  for val in "${uniqueIDs[@]}"
  do 
    echo -e "$val" >> $result_filename"metadata.tsv"
  done
  echo "-- metadata file written"
fi

#before starting the analysis, make sure that at least 1 sample is located in the input directory and that forward and reverse FASTQ files are present 
if [[ ${#allfiles_array[@]} -lt 2 ]]; then
  printf "ERROR:\tMake sure to place at least one sample with forward and reverse fastq file (-> resulting in 2 fastq files) in the input directory!\n\tSee Casava format for more information on requested FASTQ format.\n"
  exit 1
fi

#import fastq data
#results:
#    --output-path ${result_filename}"demux-paired-end.qza" : artifact containing imported fastq files 
echo "- starting import"
qiime tools import \
  --type 'SampleData[PairedEndSequencesWithQuality]' \
  --input-path ${dir} \
  --input-format CasavaOneEightSingleLanePerSampleDirFmt \
  --output-path ${result_filename}"demux-paired-end.qza"
echo "-- import done"

#create demux summary plot
echo "- starting demux summary"
qiime demux summarize \
  --i-data ${result_filename}"demux-paired-end.qza" \
  --o-visualization ${result_filename}"demux-summ.qzv"
echo "-- demux summary done"

#Quality Control
#results:
#    --o-representative-sequences ${result_filename}"sequences.qza" : The resulting feature sequences. Each feature in the feature table will be represented by exactly one sequence, and these sequences will be the joined paired-end sequences.
#    --o-table ${result_filename}"table.qza" : The feature table. Rows = features (sequences) and columns = samples. Cells = amount of times each feature was found in each sample
#    --o-denoising-stats ${result_filename}"stats.qza" : Denoising statistics
echo "- starting QC"
qiime dada2 denoise-paired \
  --i-demultiplexed-seqs ${result_filename}"demux-paired-end.qza" \
  --p-trunc-len-f $(yq .trunc_len_f $config_path) \
  --p-trunc-len-r $(yq .trunc_len_r $config_path) \
  --p-trim-left-f $(yq .trim_left_f $config_path) \
  --p-trim-left-r $(yq .trim_left_r $config_path) \
  --p-n-threads 12 \
  --p-min-fold-parent-over-abundance $(yq .p_min_fold_parent_over_abundance $config_path) \
  --o-representative-sequences ${result_filename}"sequences.qza" \
  --o-table ${result_filename}"table.qza" \
  --o-denoising-stats ${result_filename}"dada2-stats.qza"

#dada2 is producing ASVs already
echo "-- QC done"

echo "- starting phylogeny"
qiime phylogeny align-to-tree-mafft-fasttree \
  --i-sequences ${result_filename}"sequences.qza" \
  --o-alignment ${result_filename}"aligned-seqs.qza" \
  --o-masked-alignment ${result_filename}"masked-aligned-rep-seqs.qza" \
  --o-tree ${result_filename}"unrooted-tree.qza" \
  --o-rooted-tree ${result_filename}"rooted-tree.qza"
echo "-- phylogeny done"

#if more than 1 sample is located in the input directory 
if [[ ${#allfiles_array[@]} -gt 3 || ${#uniqueIDs[@]} -gt 1 ]]; then

  echo "- starting diversity assessment"
  #diversity is using metadata produced earlier in this script 
  qiime diversity core-metrics-phylogenetic \
    --i-phylogeny ${result_filename}"rooted-tree.qza" \
    --i-table ${result_filename}"table.qza" \
    --p-sampling-depth $(yq .sampling_depth $config_path)  \
    --m-metadata-file ${result_filename}"metadata.tsv" \
    --output-dir ${result_filename}"core-metrics-phylogenetic-results"
  echo "-- diversity assessment done"

  #PCOA
  echo "- starting emperor plot"
  qiime emperor plot \
    --i-pcoa ${result_filename}"core-metrics-phylogenetic-results/unweighted_unifrac_pcoa_results.qza" \
    --m-metadata-file ${result_filename}"metadata.tsv" \
    --o-visualization ${result_filename}"core-metrics-phylogenetic-results/unweighted-unifrac-emperor.qzv"
  echo "-- emperor plot done"

  qiime feature-table relative-frequency \
    --i-table ${result_filename}"core-metrics-phylogenetic-results/rarefied_table.qza" \
    --o-relative-frequency-table ${result_filename}"rel-freq-rarefied-table.qza"


  echo "- starting pcoa-biplot"
  qiime diversity pcoa-biplot \
    --i-pcoa ${result_filename}"core-metrics-phylogenetic-results/unweighted_unifrac_pcoa_results.qza" \
    --i-features ${result_filename}"rel-freq-rarefied-table.qza" \
    --o-biplot ${result_filename}"core-metrics-phylogenetic-results/unweighted-unifrac-pcoa.qza"

  qiime emperor biplot \
    --i-biplot ${result_filename}"core-metrics-phylogenetic-results/unweighted-unifrac-pcoa.qza" \
    --m-sample-metadata-file ${result_filename}"metadata.tsv" \
    --o-visualization ${result_filename}"core-metrics-phylogenetic-results/unweighted-unifrac-pcoa.qzv"
  echo "-- pcoa-biplot done"


fi

#starting taxonomy assignment using db defined in qiime2config.yml

echo "- starting feature-classifier"
qiime feature-classifier classify-sklearn \
  --i-classifier ${db_path} \
  --i-reads ${result_filename}"sequences.qza" \
  --o-classification ${result_filename}"taxonomy.qza"

qiime metadata tabulate \
  --m-input-file ${result_filename}"taxonomy.qza" \
  --o-visualization ${result_filename}"taxonomy.qzv"
echo "-- feature-classifier done"

#create taxa barplot 
echo "- starting taxa barplot"
qiime taxa barplot \
  --i-table ${result_filename}"table.qza" \
  --i-taxonomy ${result_filename}"taxonomy.qza" \
  --m-metadata-file ${result_filename}"metadata.tsv" \
  --o-visualization ${result_filename}"taxa-bar-plots.qzv"
echo "-- taxa barplot done"


#reset mode to default (not exit script if error occurs)
set +o pipefail +e