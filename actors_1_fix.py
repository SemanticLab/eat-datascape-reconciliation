from bs4 import BeautifulSoup
import requests
import json

data = json.load(open('data/actors.json'))

for idx in range(0,1000):

	# if str(idx) in data:
	# 	print('skipp',idx)
	# 	continue
	
		

	
	url = f"https://eat_datascape.medialab.sciences-po.fr/actor/{idx}"
	print(url)
	req = requests.get(url)

	if req.status_code == 500:
		print("500 err, skipp")
		continue

	html = req.text

	soup = BeautifulSoup(html)

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



	data[str(idx)]['saved_tags'] = saved_tags


	json.dump(data,open('data/actors.json','w'),indent=2)

