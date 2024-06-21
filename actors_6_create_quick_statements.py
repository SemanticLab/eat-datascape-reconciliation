import json
import sys
import csv

datascape_actors = json.load(open('data/actors.json'))
qs_reconcile = open("data/qs_reconcile.txt",'w')
qs_create = open("data/qs_create.txt",'w')

types_lookup = {
    "architect": "Q23416",
    "art critic": "Q20540",
    "art critic journalist": "Q20540",
    "artist": "Q19157",
    "artist engineer": "Q19081|Q19157",
    "consultant chemist": "Q19081",
    "curator": "Q24406",
    "curator manager": "Q24406",
    "engineer": "Q19081",
    "photographer": "Q20538",
    "professor": "Q23889",
    "researcher": "Q24692",
    "researcher engineer": "Q24692|Q19081",
    "researcher physicist": "Q19081",
    "researcher professor": "Q24692|Q23889",
    "researcher professor engineer": "Q19081|Q24692|Q23889"
}

types=[]
for d in datascape_actors:

	if 'baseQid' in datascape_actors[d]:



		print(datascape_actors[d])
		types.append(datascape_actors[d]['type'])
		qs = f'{datascape_actors[d]["baseQid"]}|P245|"actor/{d}"\n'

		if datascape_actors[d]['type'] in types_lookup:
			t = types_lookup[datascape_actors[d]['type']]
			qs = qs + f'{datascape_actors[d]["baseQid"]}|P44|{t}|S114|"https://eat_datascape.medialab.sciences-po.fr/actor/{d}"\n'

		qs_reconcile.write(qs)
	else:
		qs = "CREATE\n"
		qs = qs + f'LAST|Len|"{datascape_actors[d]["name"]}"\n'
		qs = qs + f'LAST|P1|{datascape_actors[d]["instanceOf"]}\n'


		if datascape_actors[d]['type'] != None:
			qs = qs + f'LAST|Den|"{datascape_actors[d]["type"]}"\n'


		qs = qs +f'LAST|P11|Q27735\n'
		qs = qs +f'LAST|P11|Q19104\n'

		

		if datascape_actors[d]["occupationP44"] != None:
			for occ in datascape_actors[d]["occupationP44"]:
				qs = qs + f'LAST|P44|{occ}|S114|"https://eat_datascape.medialab.sciences-po.fr/actor/{d}"\n'

		qs = qs + f'LAST|P2|"https://eat_datascape.medialab.sciences-po.fr/actor/{d}"\n'
		qs = qs + f'LAST|P245|"actor/{d}"\n'
		qs_create.write(qs)
			



qs_reconcile.close()
qs_create.close()