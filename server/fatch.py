from bs4 import BeautifulSoup
import requests
import json
import pymongo
import time as tmm



myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["newsdata"]
mycol = mydb["news"]





while True:
	URL = 'https://www.gadgets360.com/news'
	page = requests.get( URL )
	soup = BeautifulSoup( page.content , 'html.parser')
	ul_tag = soup.find('div', class_='story_list row margin_b30').find("ul")
	all_news = []
	for li in ul_tag.findAll('li',class_=None):
		photo = li.find('div',class_='thumb').find('a').find('img')
		photo1= len(str(photo).split('data-original='))
		main_photo = ''
		if photo1 == 2:
			main_photo = (str(photo).split('data-original=\"')[1].split('"')[0]).split('?')[0]
		elif photo1 == 1:
			main_photo = photo['src']
		else:
			pass
		headline = li.find('div',class_='caption_box').find('a').find('span',class_='news_listing').text
		writer_date = (li.find('div',class_='caption_box').find('div',class_='dateline')).text
		writer = (writer_date.split('by ')[1]).split(', ')[0]
		date_of_posting = (writer_date.split('by ')[1]).split(', ')[1]
		industri = li.find('div',class_='caption_box').find('a',class_='catname').text
		link = (li.find('div',class_='caption_box').find('a'))['href']
		json_n_data = {
		"headline":str(headline),
		"date":str(date_of_posting),
		"writer":str(writer),
		"industri":str(industri),
		"photo":str(main_photo),
		"link":str(link)
		}
		all_news.append(json_n_data)
	
	full_json = []
	for x in all_news:
		link = x['link']
		page1 = requests.get(link)
		soup1 = BeautifulSoup( page1.content , 'html.parser')
		
		main_h1 = ((((soup1.find('div', class_='lead_heading header_wrap').find('h1').text).replace('\u201d',"'")).replace('\u201c',"'")).replace('\u2019','’')).replace('\u2013','–')
		h2 = ((((soup1.find('div', class_='content_block').find('h2').text).replace('\u201d',"'")).replace('\u201c',"'")).replace('\u2019','’')).replace('\u2013','–')
		date_time = ((soup1.find('div', class_='dateline').text).split(': ')[1]).replace('\n','')
		date = ' '.join(date_time.split(' ')[0:3])
		time = ' '.join(date_time.split(' ')[3:5])
		photo_main = ((soup1.find('div', class_='heroimg').find('img'))['src']).split('?')[0]
		all_disc = soup1.find('div', class_='content_text row description')
		merge_text = []
		for disc in all_disc.findAll('p'):
			merge_text.append(disc.text)
	
		merge_text_all = ((((((((((('\n'.join(merge_text)).replace('“',"'")).replace('”',"'")).replace('\"',"'")).replace('\u2019','’')).replace('\u00a0',' ')).replace('\u2014','-')).replace("\u2026","...")).replace('\u201d',"'")).replace('\u201c',"'")).replace('\u2019','’')).replace('\u2013','–')
		text_ana = (((((((str((((('\n'.join(merge_text)).replace('“',"'")).replace('”',"'")).replace('\"',"'")).replace('\n','')).replace('\u2019','’')).replace('\u00a0',' ')).replace('\u2014','-')).replace("\u2026","...")).replace('\u201d',"'")).replace('\u201c',"'")).replace('\u2019','’')).replace('\u2013','–')
		json_main={
			"short":{
				"headline":(((x["headline"].replace('\u201d',"'")).replace('\u201c',"'")).replace('\u2019','’')).replace('\u2013','–'),
				"date":x["date"],
				"writer":x["writer"],
				"industri":x["industri"],
				"photo":x["photo"],
				"link":x["link"],
			},
			"details":{
				"h1": main_h1,
				"h2" : h2,
				"date" : date,
				"time" : time,
				"photo" : photo_main,
				"text" : merge_text_all
			},
			"ana_text":text_ana,
			"show" : 0,
			"analysis" : {}
		}
		# print(json.dumps(json_main, indent=4))
		full_json.append(json_main)
	
	for check in full_json:
		h_line = check['details']['h1']
		flg=0
		for x in mycol.find():
			if h_line == x['details']['h1']:
				flg=flg+1
		if flg == 0:
			mycol.insert_one(check)
	tmm.sleep(120)