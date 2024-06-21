import json
import sys
import csv
import requests

datascape_actors = json.load(open('data/actors.json'))
SPARQL_ENDPOINT = 'https://query.semlab.io/proxy/wdqs/bigdata/namespace/wdq/sparql'
total_created=0
total_recon = 0
for d in datascape_actors:


	qid = datascape_actors[d]['BaseQidCheck']




	sparql = f"""
	    SELECT ?project 
	    WHERE 
	    {{
	      wd:{qid} wdt:P11 ?project. 
	    }}


	"""
	headers = {
	    'Accept': 'application/sparql-results+json',
	}
	params = {
	    'query' : sparql
	}

	response = requests.get(
	    SPARQL_ENDPOINT,
	    params=params,
	    headers=headers,
	)
	
	has_datascape_project =  False
	has_eat_project =  False
	if 'Q27735' in response.text:
		has_datascape_project =  True
	if 'Q19104' in response.text:
		has_eat_project =  True


	if has_datascape_project == False:
		total_recon=total_recon+1

	elif has_datascape_project == True and has_eat_project == True:
		total_created=total_created+1
	else:
		print(qid, 'some thing werid')

	print('total_recon',total_recon,'total_created',total_created)

	# # get the labels for everything
	# sparql = f"""
	# 	select * where{{
	# 	  ?item wdt:P245 "actor/{d}".
		  
	# 	 }}
	# """
	# headers = {
	#     'Accept': 'application/sparql-results+json',
	# }
	# params = {
	#     'query' : sparql
	# }
	# response = requests.get(
	#     SPARQL_ENDPOINT,
	#     params=params,
	#     headers=headers,
	# )
	# data = response.json()
	
	# print(f"actor/{d}", len(data['results']['bindings']))

	# if len(data['results']['bindings']) == 1:

	# 	qid = data['results']['bindings'][0]['item']['value'].split('/')[-1]
	# 	if qid in usedQids:
	# 		print("Qid used twice", datascape_actors[d], qid)

	# 	usedQids.append(qid)

	# 	datascape_actors[d]['BaseQidCheck'] = qid


	# elif len(data['results']['bindings']) > 1:
	# 	print('Multiple Datascape Id Found:')
	# 	print(datascape_actors[d])		

	# else:
	# 	print('DATASCAPE Id Not Found:')
	# 	print(datascape_actors[d])


# json.dump(datascape_actors,open('data/actors.json','w'),indent=2)

