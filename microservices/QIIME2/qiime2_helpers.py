#!/usr/bin/python3

from qiime2 import Visualization
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import re
import os

def df_column_names_unique(df):
    df_cols = df.columns
    new_cols = []
    for c in df_cols:
        i = 0
        newc = c
        while newc in new_cols:
            i += 1
            newc = "{}_{}".format(c, i)
        new_cols.append(newc)
    df.columns = new_cols
    return df


def createBarplotFromQIIME2qzv(import_path, export_path, level = 0):
	Visualization.load(import_path).export_data(export_path) #unzip visualization
	
	if level == 0:
		level = [1,2,3,4,5,6]
	else:
		level=[level]	

	#read metadata for columns removal 
	metadatadir = os.path.dirname(f'{import_path}')
	metadata = pd.read_csv(f'{metadatadir}/metadata.tsv', index_col=0, sep='\t')
	ncolstoremove = len(metadata.columns)
	
	for l in level:

		df = pd.read_csv(f'{export_path}level-{l}.csv', index_col=0)

		#shorten the column names to last element in taxonomic tree
		for c in df.columns:
			ctmp = re.sub(';[a-z]__$', '', c)
			df.columns.values[df.columns.get_loc(c)] = ctmp
				
		renamed_colnames = [c.replace(";__", "") for c in df.columns]
		renamed_colnames = [c.split(";")[-1] for c in renamed_colnames]
		renamed_colnames = [re.sub("[a-z]__", "", c) for c in renamed_colnames]
		df.columns = renamed_colnames

		#rename duplicates
		df = df_column_names_unique(df)

		#remove metadata columns
		if ncolstoremove > 0:
			#remove the last ncolstoremove columns which store metadata information
			df.drop(columns=df.columns[-ncolstoremove:], axis=1,  inplace=True)

		for sampleID in df.index:
			print('plotting bargraph for sample ' + str(sampleID) + ' and level ' + str(l))
			df_tmp = df.loc[[sampleID]]

			#calculate frequencies
			sum_row = df_tmp.sum(axis=1)
			for c in df_tmp:
				df_tmp[c] = df_tmp[c] / sum_row * 100

			#transpose table 
			df_tmp = df_tmp.transpose()
			
			#round the values to 2 digits 
			df_tmp[df_tmp.columns[0]] = [round(i, 2) for i in df_tmp[df_tmp.columns[0]].values]

			df_tmp.to_csv(f'{export_path}sample-{sampleID}-level-{l}.csv')

			#create plot 
			fig, ax = plt.subplots()
			p = ax.barh(df_tmp.index, df_tmp[df_tmp.columns[0]].values, align='center', height=0.7)
			ax.bar_label(p, label_type='edge')
			
			plt.gca().invert_yaxis()
			plt.gcf().set_size_inches(10, len(df_tmp[df_tmp.columns[0]]) / 2)
			plt.savefig(f'{export_path}barplot-{sampleID}-level-{l}.png', dpi=300, bbox_inches = "tight")
			plt.show()
