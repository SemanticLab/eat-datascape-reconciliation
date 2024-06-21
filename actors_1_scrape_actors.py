from bs4 import BeautifulSoup
import requests
import json

data = json.load(open('data/actors.json'))

for idx in range(0,1000):

	if str(idx) in data:
		print('skipp',idx)
		continue
	
		

	
	url = f"https://eat_datascape.medialab.sciences-po.fr/actor/{idx}"
	print(url)
	req = requests.get(url)

	if req.status_code == 500:
		print("500 err, skipp")
		continue

	html = req.text

	soup = BeautifulSoup(html)

	collabs_el = soup.find(id="sources-list")

	colabs = collabs_el.find_all("div",attrs={'class':'source-link'})

	colabs_list = []
	for c in colabs:
		a = c.find("a")
		colabs_list.append(int(a['href']))



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


	h1 = soup.find("h1")

	name = list(h1.children)[0].text.strip()
	name_type = list(h1.children)[1].text.strip()
	
	if name_type == '':
		name_type = None

	line_data = []
	for script in soup.find_all("script"):

		for line in script.text.split("\n"):
			if 'var phases =  [{' in line:
				line = line.replace("var phases =  ",'')
				line = line[0:-1]
				line_data = json.loads(line)




	data[idx] = {
		'id': idx,
		'name': name,
		'type': name_type,
		'collabs': colabs_list,
		'events': line_data,
		'saved_tags':saved_tags
	}
	json.dump(data,open('data/actors.json','w'),indent=2)

