import requests
import json
import jellyfish
import sys
import csv

def get_closest_match(x, list_random):
    best_match = None
    highest_compare_score = 0
    for current_string in list_random:
        current_score = jellyfish.jaro_winkler_similarity(x, current_string)
        if(current_score > highest_compare_score):
            highest_compare_score = current_score
            best_match = current_string

    return { 'match': best_match, 'score': highest_compare_score}


SPARQL_ENDPOINT = 'https://query.semlab.io/proxy/wdqs/bigdata/namespace/wdq/sparql'

# get the labels for everything
sparql = """
    SELECT ?item ?itemLabel 
    WHERE 
    {

		VALUES ?value
		{
			wd:Q19049
			wd:Q1
			wd:Q24537
			wd:Q19103
			wd:Q1804
			wd:Q20618
			wd:Q19072
		}


		?item wdt:P1 ?value. 

		SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } # Helps get the label in your language, if not, then en language
    }
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
data = response.json()
labelLookup={}
base_labels_only = []
for result in data['results']['bindings']:
    labelLookup[result['item']['value'].split('/')[-1]] = result['itemLabel']['value']
    base_labels_only.append(result['itemLabel']['value'])

datascape_actors = json.load(open('data/actors.json'))
print(datascape_actors)

actors_good_match_file = open('data/actors_good_matchs.csv','w')
csv_writer = csv.writer(actors_good_match_file)


for datascape_id in datascape_actors:

	datascape_name = datascape_actors[datascape_id]['name']

	# print(datascape_name, get_closest_match(datascape_name,base_labels_only))
	best_match = get_closest_match(datascape_name,base_labels_only)

	if best_match['score'] >= 0.9:


		qid = []
		for q in labelLookup:
			if labelLookup[q] == best_match['match']:
				qid.append(q)

		if len(qid) > 1:
			print("ERRROR", qid, best_match)
			#sys.exit()


		sparql = f"""
		    SELECT ?project ?projectLabel 
		    WHERE 
		    {{
		      wd:{qid[0]} wdt:P11 ?project. 
		      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }} 
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
		data = response.json()

		projects = []
		for result in data['results']['bindings']:
			if 'projectLabel' in result:
				projects.append(result['projectLabel']['value'])


		csv_writer.writerow([datascape_id,datascape_name,best_match['match'], qid[0],best_match['score'],",".join(projects)])
		print(datascape_name, best_match)



actors_good_match_file.close()

