#!/usr/bin/python3

from fpdf import FPDF
import pandas as pd
import os 
from hugchat import hugchat
from hugchat.login import Login
import textwrap

def extract_perc_as_string(sampleID, result_path):
	filename = f'{result_path}python_barplots/sample-{sampleID}-level-2.csv'
	microbiome_perc_st = ""
	if os.path.exists(filename):
		print(sampleID)
		#read frequency csv, which was previously produced
		df = pd.read_csv(filename, index_col=0)
		counter = 1
		#create String from percentages for LLM input 
		for elem in df.index:
			microbiome_perc_st = microbiome_perc_st + elem + ': ' + str(df[df.columns[0]][elem]) + "%"
			if counter <= len(df.index)-1:
				microbiome_perc_st = microbiome_perc_st + ", "
			counter = counter + 1	
	return microbiome_perc_st

def extract_patient_information(metadata_for_sampleID, result_path):
	patient_information_st = ""
	counter = 1
	for elem in metadata_for_sampleID.index:
		patient_information_st = patient_information_st + str(elem) + ": " + str(metadata_for_sampleID[elem])
		if counter <= len(metadata_for_sampleID.index)-1:
			patient_information_st = patient_information_st + ", "
		counter = counter + 1
	return patient_information_st


def read_expert_knowledge():
	file = open(f'/script/qiime2_expert_knowledge.txt', mode='r')
	knowledge = file.read()
	file.close()
	return knowledge

def call_LLM(expert_knowledge, microbiome_perc_st, information):
	# log in 
	sign = Login('laura.glau@studium.fernuni-hagen.de', 'HugPassword123')
	cookies = sign.login()

	# create chatbot
	chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
	
	#default LLM is meta-llama/Llama-2-70b-chat-hf
	#chatbot.switch_llm(2) # switch to the Falcon-180B-Chat model

	prompt = "Du bist Arzt in einem medizinischen Diagnostiklabor und erstellst einen detaillierten medizinischen Diagnostikbericht für einen Patienten. "
	prompt = prompt + "Der Patient hat eine Stuhlprobe abgegeben und mittels 16S rRNA Sequenzierung wurde die Zusammensetzung des intestinalen Mikrobioms untersucht. "
	prompt = prompt + "Die Mikrobiomzusammensetzung ist wie folgt: " + microbiome_perc_st + ". "
	prompt = prompt + "Die Mikrobiomzusammensetzung soll bitte als Tabelle in dem Brief dargestellt werden. "
	if information != "":
		prompt = prompt + "Bitte berücksichtige auch diese weiteren Informationen über den Patienten in dem Bericht: " + information + ". "
		prompt = prompt + "Die Informationen über den Patienten sollen bitte auch einmal über dem Text, also im Briefkopf tabellarisch dargestellt werden. "
	if expert_knowledge != "":
		prompt = prompt + "Zusätzlich stelle ich dir folgendes Expertenwissen zur Verfügung: " + expert_knowledge + ". "
		prompt = prompt + "Nutze dieses Expertenwissen aber bitte nur, wenn die entsprechenden Bakterien auch in der Mikrobiomzusammensetzung erwähnt werden. "
		prompt = prompt + "Wenn ein Bakterium in der Mikrobiomzusammensetzung nicht gelistet ist, heißt das nicht, dass es nicht vorhanden ist. "
		prompt = prompt + "Wenn es nicht gelistet ist, kann man keine Aussage über dieses Bakterium treffen. "
		prompt = prompt + "Liste das Expertenwissen bitte nicht extra in dem Brief auf. Dieses dient nur dir als Hintergrundwissen.  "
	prompt = prompt + "Und bitte schreibe einen Absatz über die Analyse und den Vergleich zu gesunden Donoren und einen Absatz mit Handlungsempfehlungen, "
	prompt = prompt + "um eventuelle Defizte in der Mikrobiomzusammensetzung  zu addressieren. "
	prompt = prompt + "Der Brief soll außerdem direkt den Patienten addressieren und professionell klingen. "
	prompt = prompt + "Schreibe den Brief bitte auf Deutsch. Vielen Dank! "

	query_result = ""

	#send prompt to LLM	
	query_result = chatbot.query(prompt, 
		retry_count = 5, web_search = False)

	#translate to german
	query_result = chatbot.query("Übersetze den Text bitte in die deutsche Sprache: " + query_result, 
		retry_count = 5, web_search = False)
	
	return str(query_result)


def create_LLM_report(result_path, pdf, width_text, a4_width_mm):

	metadata = pd.read_csv(f'{result_path}metadata.tsv', index_col=0, sep='\t')

	expert_knowledge = read_expert_knowledge()		

	for sampleID in metadata.index:

		microbiome_perc_st = extract_perc_as_string(sampleID, result_path)

		#skip this sampleID, because microbiome composition info was not found in results folder 
		if microbiome_perc_st == "":
			continue

		pdf.set_font(family='Courier', size=20, style='B')
		pdf.cell(0, 15, "Report über die Mikrobiomzusammensetzung", ln=1, align="C")

		information = extract_patient_information(metadata.loc[sampleID], result_path)

		LLM_result = call_LLM(expert_knowledge, microbiome_perc_st, information)
		#make sure the LLM result has the correct encoding for pasting it to pdf
		LLM_result = LLM_result.encode('latin-1', 'ignore').decode('latin-1')

		#save LLM result to txt file
		with open(f'{result_path}LLM_result_'+ str(sampleID) + '.txt', 'w') as f:
			f.writelines(LLM_result)

		#add sampleID to PDF
		sampleIDtext = "SampleID: " + str(sampleID)
		print(sampleIDtext)
		pdf.set_font(family='Helvetica', size=12)
		pdf.cell(0, 12, "", ln=1)
		pdf.cell(0, 12, sampleIDtext, ln=1)

		#add report to PDF
		pdf.set_font(family='Helvetica', size=10)
		pdf.multi_cell(0, 10, LLM_result)
		
		#add bar graph to PDF
		pdf.add_page()
		pdf.set_font(family='Helvetica', size=12)
		pdf.cell(0, 12, sampleIDtext, ln=1)
		pdf.image(f'{result_path}/python_barplots/barplot-{sampleID}-level-2.png', w = a4_width_mm-20)

		#add new page
		pdf.add_page()

	return pdf
