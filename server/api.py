import os
import json
from operator import itemgetter

# from wordcloud import WordCloud, STOPWORDS
# import matplotlib.pyplot as plt
from datetime import datetime

from ibm_watson import NaturalLanguageUnderstandingV1
# from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, SyntaxOptions, SyntaxOptionsTokens, CategoriesOptions, ConceptsOptions

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["newsdata"]
mycol = mydb["news"]



while True:
	
	for xyz in mycol.find():
		text = xyz['ana_text']
		
		if xyz['show'] == 0:
			print(xyz['_id'])
			print(xyz['details']['h1'])

			apikey = ''
			url = 'https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com'
			
			# Natural Language Understanding
			authenticator = IAMAuthenticator(apikey)
			natural_language_understanding =  NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
		
			natural_language_understanding.set_service_url(url)
			
			
			myJsonDict = {}
			
			''' Extract Category with NLU '''
			
			try:
				response = natural_language_understanding.analyze(
					language='en',
					text=text,
					features=Features(categories=CategoriesOptions(limit=1))).get_result()
			
				category = response['categories'][0]
			
				myJsonDict.update({"category": category})
			
			except:
				myJsonDict.update({"category": "Text too small to extract category"})
			
			
			try:
				response = natural_language_understanding.analyze(
					language='en',
					text=text,
					features=Features(concepts=ConceptsOptions(limit=3))).get_result()
			
				concepts = sorted(response['concepts'], key=itemgetter('relevance'), reverse=True)
			
				myJsonDict.update({"concepts": concepts})
			
			except:
				myJsonDict.update({"concepts": "Text too small to extract concepts"})
			
			
			try:
				response = natural_language_understanding.analyze(
					language='en',
					text=text,
					features=Features(entities=EntitiesOptions(limit=1))).get_result()
			
				entity = sorted(response['entities'], key=itemgetter('relevance'), reverse=True)
			
				myJsonDict.update({"entity": entity[0]})
			
			except:
				myJsonDict.update({"entity": []})
			
			
			try:
				response = natural_language_understanding.analyze(
					language='en',
					text=text,
					features=Features(keywords=KeywordsOptions(sentiment=True, emotion=True, limit=10))).get_result()
			
				keywords = sorted(response['keywords'], key=itemgetter('relevance'), reverse=True)
			
				keywords_sentiments_emotions = []
				
				for i in keywords:
				
					keywords_sentiments_emotions_buffer = {'keyword': i['text'],'sentiment': i['sentiment']['label'],'emotion': ''}
					maximum = i['emotion']['sadness']
					keywords_sentiments_emotions_buffer['emotion'] = 'sadness'
				
					if i['emotion']['joy'] > maximum:
						maximum = i['emotion']['joy']
						keywords_sentiments_emotions_buffer['emotion'] = 'joy'
					
					elif i['emotion']['fear'] > maximum:
						maximum = i['emotion']['fear']
						keywords_sentiments_emotions_buffer['emotion'] = 'fear'
					
					elif i['emotion']['disgust'] > maximum:
						maximum = i['emotion']['disgust']
						keywords_sentiments_emotions_buffer['emotion'] = 'disgust'
					
					elif i['emotion']['anger'] > maximum:
						maximum = i['emotion']['anger']
						keywords_sentiments_emotions_buffer['emotion'] = 'anger'
				
					keywords_sentiments_emotions.append(keywords_sentiments_emotions_buffer)
			
				myJsonDict.update({"sentiments": keywords_sentiments_emotions})
			
			except:
				myJsonDict.update({"sentiments": []})
			
			
			try:
				response = natural_language_understanding.analyze(
					language='en',
					text=text,
					features=Features(keywords=KeywordsOptions(sentiment=True, emotion=True))).get_result()
			
				keywords = sorted(response['keywords'], key=itemgetter('relevance'), reverse=True)
			
				keywords_sentim_pos = []
				keywords_sentim_neg = []
				
				for i in keywords:
			
					keywords_sentiments = {'keyword': i['text'],'sentiment': i['sentiment']['label']}
			
					if i['sentiment']['label']=='positive':
						keywords_sentiments['sentiment'] = 'positive'
						keywords_sentim_pos.append(keywords_sentiments)
			
					if i['sentiment']['label']=='negative':
						keywords_sentiments['sentiment'] = 'negative'
						keywords_sentim_neg.append(keywords_sentiments)
			
				myJsonDict.update({"positive_sentiments": keywords_sentim_pos})
				myJsonDict.update({"negative_sentiments": keywords_sentim_neg})
			
			except:
				myJsonDict.update({"positive_sentiments": []},{"negative_sentiments": []})
			
		
		
			myquery = { "_id": xyz['_id'] }
			newvalues = { "$set": { "analysis": myJsonDict,"show":1 } }
			mycol.update_many(myquery, newvalues)
			print('\n')