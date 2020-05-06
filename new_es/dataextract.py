from elasticsearch import Elasticsearch


#Elastic Instance

es=Elasticsearch([{"host":"148.251.190.132","port":9200}])
term="india politics"
query_string="E commerce"
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


query_response=es.search(index="documents*",body=query)
print(query_response["hits"]["hits"][0]["_source"]["body"])