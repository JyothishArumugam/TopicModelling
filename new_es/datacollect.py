import argparse
from elasticsearch import helpers,Elasticsearch
import os
import io
import re
from nltk.corpus import stopwords


path="data/"

cachedStopWords = stopwords.words("english")



#create the index through elastic search
def elastic_output(search,number_of_documents):
    es=Elasticsearch([{'host':'148.251.190.132','port':9200}])
    query_string=search
    search_op="or"
    query = {
            "_source": ["pubdate", "keywords", "organizations",
                        "people", "path", "yscore", "domain", "id",
                        "summary", "title", "doc_type","body"],
            "query":
                {"bool":
                    {"must": [
                        {"multi_match": {
                         "query": query_string,
                         "type": "best_fields",
                         "tie_breaker": 0.3,
                         "fields": [ "keywords", "title","body"],
                         "operator": search_op
                         },
                         },
                     ],
                     "must_not": [],
                     "should": [
                         {"match":
                          {
                              "body": query_string
                              },
                          },
                          
                          {"term":
                           {
                               "keywords": query_string
                           },
                          },
                          {"match":
                           {
                               "title": query_string,
                               }
                           }],

                     },
                 },
            "sort": [
                {"_score": "desc"},
                {"yscore": {
                    "order": "desc",
                    "unmapped_type": "long"
                }
                },
                {"publisher.keyword": "asc"},
                {"pubdate.keyword": "desc"},
                {"price": "asc"},
            ]
        } 

    res=es.search(index="documents*",body=query)
    return res


def file_formater(inputs):
	"""
	This function will output the files that are to written 
	into the training file

	"""
	regex=re.compile('[^a-zA-Z]')
	inputs=regex.sub(' ',inputs)
	inputs=stop_removal(inputs.lower())
	return str(inputs)

def stop_removal(text):
	"""
	This method will take the documents and remove the stopwords
	"""
	text = ' '.join([word for word in text.split() if word not in cachedStopWords])
	return text

    
def create_directory(search):
    """will create the directory to store the search results"""
    os.mkdir("models"+"/"+search)

def output_writer(res):
    paths=[]
    texts=[]
    names=[]
    for every in res['hits']['hits']:
        texts.append(every['_source']['body'])
        paths.append(every['_source']['path'])
        names.append(every['_source']['title'])
        # creating the dictionary and rev dictionary
    #dictionary=Dictionary(array(texts))
    rev_dict={}
    #data=pd.DataFrame({"result":texts,"path":paths,"name":names})

    with open("models"+"/"+search+"/"+search+'.dat','a') as wrt:
        wrt.write(str(len(texts)))
        wrt.write("\r\n")
        
    for i in paths:
        with open("models"+"/"+search+"/"+search+'.urls','a')as wrt:
            wrt.write(str(i))
            wrt.write("\r\n")



    for i in texts:
        with open("models"+"/"+search+"/"+search+'.dat','a')as wrt:
            wrt.write(str(file_formater(i)))
            wrt.write("\r\n")




if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("search",help="decide the search term")
    parser.add_argument("search_across",help="total number of documents needed to search")
    args=parser.parse_args()
    search=args.search
    number_of_documents=args.search_across
    print(number_of_documents)
    res=elastic_output(search,number_of_documents)
    create_directory(search)
    output_writer(res)