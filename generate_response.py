"""
This will be getting the topic probabiility of the files
"""
from collections import Counter
import argparse
### this will be the document to topic mapping
import io
import json
import os

path="models"

def response_generator(search):
	"""
	This function will generate the json response needed to plot the d3 plots and when provided with the serach and the required files """
	input_file=open("models/"+search+'/'+'model-final.tassign').readlines()
	every_document_list=[]
	for every_document in input_file:
		every_document_list.append(every_document.split())

	every_document_count=[]
	document_topic_maps=[]
	for every in every_document_list:
		out_p=[k.split(':')[1] for k in every]
		counter=Counter(out_p)
		topics=list(counter.keys())
		total_words=sum(list(counter.values()))
		dic={}
		for i in topics:
			dic.update({i:counter[i]/total_words})
		document_topic_maps.append(dic)
		#all_functions=[dic.update({i:counter[i]/sum(counter.values())}) for i in topics]
		#every_document_count.append(all_functions)


	### generate the document topic links
	document_topic_links=[]

	for index,k in enumerate(document_topic_maps):
		for targets in k.keys():
			document_topic_links.append((index,int(targets)))

	#print(document_topic_links)
	### document and topic relationships were plotted next we are to plot the names for the topics
	## hereon we are following the topic naming

	topic_words=open(path+'/'+search+'/'+'model-final.twords').readlines()
	num_topics=20
	urls=open(path+'/'+search+'/'+search+'.urls').readlines()
	
	number_documents=len(urls)

	final=[]
	test=[]
	"""
	This block will save the topics partition element, if we get elements b/w top_separator[0] & top_separator[1] we ge the words for
	topic 0
	"""
	top_separator=[]
	for nu_id,top in enumerate(topic_words):
		if top.split()[0]=='Topic':
			top_separator.append(nu_id)


	"""
	Make an list of list that will have the words appended to it, list of list of length =number of topics
	"""
	topic_maps=[]

	topic_words=[i.split()[0] for i in topic_words]
	for index,i in enumerate(top_separator):
		if index < len(top_separator)-1:
			topic_maps.append(topic_words[i+1:top_separator[index+1]])
		else:
			topic_maps.append(topic_words[i+1:])

	"""
	This will be the creation of the topic_names what the topic names are the highest proability  word
	"""
	topic_names=[]
	for i in topic_maps:
		counter=0
		for identifier,every in enumerate(i):
			if every not in topic_names:
				topic_names.append(i[counter])
				break
			else:
				counter+=1
	print(topic_names)
	## topic maps will have the number of topics=20 and its related (20)words in the list
	word_list=[]
	for maps in topic_maps:
		word_list.extend(maps)
	word_list=list(set(word_list))
	word_topic_links=[]

	for index,k in enumerate(topic_maps):
		for word in k:
			word_topic_links.append((index,word_list.index(word)))
	### donw the words and topic things
	## finally make everything into the dictionary and then json
	## topics first -topic numbers unchanged
	##documents_Second-DOCUMnets number plus number of topics
	##words_last=words_number=words number+topic number+document_numbers
	document_topic_links_modified = [(k+num_topics,h) for k,h in document_topic_links]
	word_topic_links_modified = [(k,h+num_topics+number_documents) for k,h in word_topic_links]
	## make the json file ready
	doc_topic_data={
		"links":[{"source":k,"target":l} for k ,l in document_topic_links_modified],
		"nodes":[{"size":60,"score":0.5,"id":top,"type":"circle"}for top in topic_names],
		}
	#new_list_2=[{"size":30,"score":0.9,"id":top,"type":"circle"}for top in range(1,number_documents+1)]#nodes for document
	new_list_2=[{"size":40,"score":0.01,"id":top,"type":"circle","urls":urlz}for top,urlz in enumerate(urls)]
	new_list_3=[{"source":k,"target":l} for k ,l in word_topic_links_modified]#links for words
	new_list_4=[{"size":10,"score":0.9,"id":top,"type":"circle"}for top in word_list]#node element
	doc_topic_data["nodes"].extend(new_list_2)
	doc_topic_data["nodes"].extend(new_list_4)
	doc_topic_data["links"].extend(new_list_3)
	writer_function(search+".json",doc_topic_data)
	return doc_topic_data


def writer_function(filename,data2w):
	try:
		to_unicode = unicode
	except NameError:
		to_unicode = str
	with io.open('response'+'/'+filename, 'a', encoding='utf8') as outfile:
		str_ = json.dumps(data2w,indent=4, sort_keys=True,separators=(',', ': '), ensure_ascii=False)
		outfile.write(to_unicode(str_))

def create_dir():
	if "response" not in os.listdir('.'):
		os.mkdir('response')
	else:
		pass
def responseGen(search):
	create_dir()
	finalresponse=response_generator(search)
	return finalresponse

