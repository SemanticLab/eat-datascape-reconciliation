import json
import sys
import csv
import requests

datascape_actors = json.load(open('data/actors.json'))

for d in datascape_actors:

	d = datascape_actors[d]

	paylaod = {
		'action': 'wbsearchentities',
		'search': d['name'],
		'format':'json',
		'errorformat':'plaintext',
		'uselang':'en',
		'language':'en',
		'type':'item',
	}

	url = f"https://base.semlab.io/w/api.php"

	req = requests.get(url,params=paylaod)
	data = req.json()
	if 'search' in data:
		hits = len(data['search'])

		if hits > 1:
			print(d['name'])
			for h in data['search']:

				s = "\n\t-- " + h['label']
				if 'description' in h:

					s = s + f' ({h["description"]})'
				print(s)

