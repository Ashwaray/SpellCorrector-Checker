import csv
import urllib2
import requests
from elasticsearch import Elasticsearch
import json
import os
import sys

def search(queryText):
	print 'q= ', queryText

	INDEX_NAME = 'words'
	TYPE_NAME = 'spelling'

	ID_FIELD = 'spellingid'


	ES_HOST = {"host":"localhost", "port":9200}
	es = Elasticsearch(hosts = [ES_HOST])


	res = es.search( index=INDEX_NAME, body={
	                                              "query":{
                                                            	"fuzzy" : {
							        									"name" : { 
																		   	"value" : queryText,
																			"fuzziness" : 2,
																			"boost" :         1.0,
																			"prefix_length" : 0,
							            									"max_expansions": 100
																		  }
                                             	              	   }
	                                         	       		}
											}
	                )


	                                              
	                                   
	print res

	relatedSearchedTags = []
	for hit in res['hits']['hits']:
		data = {}
		data = hit["_source"]
	        print (hit["_source"])
		relatedSearchedTags.append(data['name'].replace("\n", ""))	
		print 'data = ',data['name']

	returnString = ""
	for s in relatedSearchedTags:
		returnString = returnString + s + "\n"

	return returnString

if __name__ == "__main__":
	print search(str(sys.argv[1]))