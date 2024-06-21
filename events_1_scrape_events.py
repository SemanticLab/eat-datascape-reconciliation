from bs4 import BeautifulSoup
import requests
import json

data = json.load(open('data/events.json'))

for idx in range(0,300):

	if str(idx) in data:
		print('skipp',idx)
		continue
	
		

	
	url = f"https://eat_datascape.medialab.sciences-po.fr/project/{idx}"
	print(url)
	req = requests.get(url)

	if req.status_code == 500:
		print("500 err, skipp")
		continue

	html = req.text

	soup = BeautifulSoup(html)

	h1 = soup.find("h1")

	name = list(h1.children)[0].text.strip()
	name_type = list(h1.children)[1].text.strip()
	
	if name_type == '':
		name_type = None

	saved_tags = {
		'techno':[],
		'art':[]
	}
	for t in ['techno','art']:

		tag = soup.find('div',attrs={'class':t})

		if tag != None:
			tags = tag.find_all('span',attrs={'class':'tag'})
			for a_tag in tags:
				saved_tags[t].append(a_tag.text)

	print(saved_tags)

	

	sources = []
	phases = []
	actors_phases=[]
	for script in soup.find_all("script"):

		for line in script.text.split("\n"):
			print(line)
			if 'var sources =  {' in line:
				line = line.replace("var sources =  ",'')
				line = line[0:-1]
				sources = json.loads(line)
			if 'var phases =  [{' in line:
				line = line.replace("var phases =  ",'')
				line = line[0:-1]
				phases = json.loads(line)
			if 'var actors_phases =  {' in line:
				line = line.replace("var actors_phases =  ",'')
				line = line[0:-1]
				actors_phases = json.loads(line)

	print(sources)
	print(phases)
	print(actors_phases)

	data[idx] = {
		'id': idx,
		'name': name,
		'type': name_type,
		'sources': sources,
		'phases': phases,
		'evenactors_phasests': actors_phases,
		'saved_tags':saved_tags
	}
	json.dump(data,open('data/events.json','w'),indent=2)

