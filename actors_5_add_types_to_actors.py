import json
import sys
import csv

datascape_actors = json.load(open('data/actors.json'))
actors_good_match_file = open('data/types_recon_reviewed.csv')
csv_reader = csv.DictReader(actors_good_match_file)

for row in csv_reader:

	
	if row['BASE QID'] == '':



		for d in datascape_actors:

			if d == row['id']:
				datascape_actors[d]['instanceOf'] = row['instanceOf']
				if row['occupationP44'] != '':
					datascape_actors[d]['occupationP44'] = row['occupationP44'].split("|")
				else:
					datascape_actors[d]['occupationP44'] = None

				print(datascape_actors[d])
				print(row)
				print("----")


json.dump(datascape_actors,open('data/actors.json','w'),indent=2)
actors_good_match_file.close()

