import json
import sys
import csv

datascape_actors = json.load(open('data/actors.json'))
actors_good_match_file = open('data/actors_good_matches_reviewed.csv')
csv_reader = csv.DictReader(actors_good_match_file)

for row in csv_reader:

	
	if row['Manual Review'] != 'X':
		for d in datascape_actors:
			if d == row['Datascape ID']:
				print(datascape_actors[d])
				print(row)
				datascape_actors[d]['baseQid'] = row['BASE QID']


json.dump(datascape_actors,open('data/actors.json','w'),indent=2)
actors_good_match_file.close()

