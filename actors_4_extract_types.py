import json
import sys
import csv

datascape_actors = json.load(open('data/actors.json'))
types_reconfile = open('data/types_recon.csv','w')
csv_writer = csv.writer(types_reconfile)


for d in datascape_actors:
	if 'baseQid' not in datascape_actors[d]:
		csv_writer.writerow([datascape_actors[d]['id'],datascape_actors[d]['name'],datascape_actors[d]['type']])


# for row in csv_reader:

	
# 	if row['Manual Review'] != 'X':
# 		for d in datascape_actors:
# 			if d == row['Datascape ID']:
# 				print(datascape_actors[d])
# 				print(row)
# 				datascape_actors[d]['baseQid'] = row['BASE QID']



types_reconfile.close()

