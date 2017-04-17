from nltk.tokenize import TweetTokenizer
import string
from nltk.corpus import stopwords
import itertools
from collections import Counter
from langdetect import detect
from geotext import GeoText
import nltk
import re
import csv
import pickle


def isWord(input):
	input = input.lower()
	pattern = re.compile(r"^'?[a-z]+([-'][a-z]+)*'?$")
	if pattern.match(input):
		return True
	else:
		return False

def isEnglish(input):
	try:
		lang = detect(input)
		if lang == 'en':
			return True
		else:
			return False
	except:
		return False

def tokenizeTweet(tweet):
	# Web Scraping with Python, Ch. 7
	try:
		tknzr = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
		return tknzr.tokenize(tweet)
	except:
		return []
	
	
def cleanInputUnigram(input):
	cleanInput = []
	rejectInput = []
	other = []
	punctuation = list(string.punctuation)
	for item in input:
		item = item.encode('utf-8')
		item = item.lower()
		if item not in punctuation and isWord(item):
			cleanInput.append(item)
		elif item not in punctuation and not isWord(item):
			rejectInput.append(item)
		else:
			other.append(item)
	return [cleanInput, rejectInput, other]

	
def cleanInputNgram(input):
	cleanInput = []
	punctuation = list(string.punctuation)
	stop = punctuation + ['rt', 'via']
	for item in input:
		item = item.encode('utf-8')
		if item not in stop:
			cleanInput.append(item)
		else:
			pass
	return cleanInput
		
def mergeListItems(items, unique):
	if unique:
		return list(set(list(itertools.chain.from_iterable(items))))
	else:	
		return list(itertools.chain.from_iterable(items))

def countItems(itemList):
	counted = dict(Counter(itemList))
	items = [(v, k) for k, v in counted.items()]
	items.sort()
	return [(k, v) for v, k in items]
	
def Places(itemList):
	place_list = []
	for item in itemList:
		places = GeoText(item.title())
		if len(places.cities) > 0:
			place_list.append(places.cities[0].lower())
	return place_list
	
def tupleToCsv(itemList, filepath):
	with open(filepath,'wb') as out:
	    csv_out=csv.writer(out)
	    for row in itemList:
	        csv_out.writerow(row)
