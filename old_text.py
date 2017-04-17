from helperfunctions import *
from nltk.corpus import brown
from nltk.corpus import webtext
from nltk.corpus import names
from nltk.corpus import state_union
from nltk.corpus import reuters
from nltk.corpus import twitter_samples
import string

def processOldTweets():
	
	# old Tweets from CIND 719. A corpus of English language
	# Tweets from 2010
	tweet_list = []
	with open('full_text.txt') as input:
		 tweet_list = (zip(*(line.strip().split('\t') for 
			line in input)))
	
	#Tweets are in 2 dimensional list. Top level list has 5 elements:
	#0 - user
	#1 - date/time
	#2 - latitude and longitude combined
	#3 - latitude
	#4 - longitude
	#5 - tweet text
		
	text_list = tweet_list[5] #only need the tweet text right now
	
	# Each token in the Tweet is checked to see if it's a valid word
	# a word can only have letters [a-z] and hyphens and
	# apostrophies in the words are ok. List of bad words and
	# 'other' words that may have slipped through the cracks are
	# are tracked but not used. 
	goodwords = [] 
	badwords = []
	other = []
	for tweet in text_list:
		tokenized = tokenizeTweet(tweet)
		output = cleanInputUnigram(tokenized)
		goodwords.append(output[0])
		badwords.append(output[1])
		other.append(output[2])
	
	# Final list of distinct, valid words
	goodwords = mergeListItems(goodwords, unique = True)
	badwords = mergeListItems(badwords, unique = True)
	other = mergeListItems(other, unique = True)
	
	# Serialize good word list and pickle it to load quicker
	# for many times the program is run	
	f = open('pickle/old_tweet_unigrams.pkl', 'wb')
	pickle.dump(goodwords, f)
	f.close()
	
	# Calculate the bigrams
	# Don't filter out any words first to preserve proper
	# relationship between words, nonsensical bigrams are filtered
	# out after.
	bigrams = []
	for tweet in text_list:
		tokenized = tweet.split()
		bigrams.append(list(nltk.ngrams(tokenized, 2)))
	
	cleaned_bigrams = []
	for tweet in bigrams:
		for bigram in tweet:
			if isWord(bigram[0]) and isWord(bigram[1]):
				cleaned_bigrams.append((bigram[0].lower(), 
					bigram[1].lower()))
	# Serialize good bigrams list and pickle it to load quicker
	# for many times the program is run				
	f = open('pickle/old_tweet_bigrams.pkl', 'wb')
	pickle.dump(cleaned_bigrams, f)
	f.close()

def processBrown():
	
	# The Brown University Standard Corpus of Present-Day 
	# American English was compiled in the 1960s
	# brown_words = list(set(list(brown.words()))) # set to make list 
	# unique print(brown_words)
	
	text_list = brown.words()
	
	goodwords = []
	badwords = []
	other = []
	for tweet in text_list:
		tokenized = tokenizeTweet(tweet)
		output = cleanInputUnigram(tokenized)
		goodwords.append(output[0])
		badwords.append(output[1])
		other.append(output[2])
	
	goodwords = mergeListItems(goodwords, unique = True)
	badwords = mergeListItems(badwords, unique = True)
	other = mergeListItems(other, unique = True)
	
	f = open('pickle/brown_unigrams.pkl', 'wb')
	pickle.dump(goodwords, f)
	f.close()
	
	bigrams = list(nltk.ngrams(text_list, 2))
	
	cleaned_bigrams = []
	for bigram in bigrams:
		bigram1 = bigram[0]
		bigram2 = bigram[1]
		bigram1 = bigram1.encode('utf-8')
		bigram2 = bigram2.encode('utf-8')
		bigram1 = bigram1.lower()
		bigram2 = bigram2.lower()
		if isWord(bigram1) and isWord(bigram2):
			cleaned_bigrams.append((bigram1, bigram2))
						
	f = open('pickle/brown_bigrams.pkl', 'wb')
	pickle.dump(cleaned_bigrams, f)
	f.close()

def processOverheard():
	
	# Webtext overheard.txt - Overheard in New York (partly censored) 
	# http://www.overheardinnewyork.com/ (2006)
	overheard = webtext.raw('overheard.txt')
	text_list = tokenizeTweet(overheard)
	output = cleanInputUnigram(text_list)
	goodwords = list(output[0])
	badwords = list(output[1])
	other = list(output[2])
	
	goodwords = list(set(goodwords))
	badwords = list(set(badwords))
	other = list(set(other))
	
	f = open('pickle/overheard_unigrams.pkl', 'wb')
	pickle.dump(goodwords, f)
	f.close()
	
	overheard = overheard.split()
	bigrams = list(nltk.ngrams(list(overheard), 2))
	
	cleaned_bigrams = []
	for bigram in bigrams:
		bigram1 = bigram[0]
		bigram2 = bigram[1]
		bigram1 = bigram1.encode('utf-8')
		bigram2 = bigram2.encode('utf-8')
		bigram1 = bigram1.lower()
		bigram2 = bigram2.lower()
		if isWord(bigram1) and isWord(bigram2):
			cleaned_bigrams.append((bigram1, bigram2))
			
	f = open('pickle/overheard_bigrams.pkl', 'wb')
	pickle.dump(cleaned_bigrams, f)
	f.close()
	
	
def processSingles():
	
	# singles.txt: Singles ads http://search.classifieds.news.com.au/ 

	singles = webtext.raw('singles.txt')
	text_list = tokenizeTweet(singles)
	output = cleanInputUnigram(text_list)
	goodwords = list(output[0])
	badwords = list(output[1])
	other = list(output[2])
	
	goodwords = list(set(goodwords))
	badwords = list(set(badwords))
	other = list(set(other))
	
	f = open('pickle/singles_unigrams.pkl', 'wb')
	pickle.dump(goodwords, f)
	f.close()
	
	singles = singles.split()
	bigrams = list(nltk.ngrams(list(singles), 2))
	
	cleaned_bigrams = []
	for bigram in bigrams:
		bigram1 = bigram[0]
		bigram2 = bigram[1]
		bigram1 = bigram1.encode('utf-8')
		bigram2 = bigram2.encode('utf-8')
		bigram1 = bigram1.lower()
		bigram2 = bigram2.lower()
		if isWord(bigram1) and isWord(bigram2):
			cleaned_bigrams.append((bigram1, bigram2))
			
	f = open('pickle/singles_bigrams.pkl', 'wb')
	pickle.dump(cleaned_bigrams, f)
	f.close()	
	
def processFirefox():
	
	# firefox.txt: Firefox support forum 
	firefox = webtext.raw('firefox.txt')
	text_list = tokenizeTweet(firefox)
	output = cleanInputUnigram(text_list)
	goodwords = list(output[0])
	badwords = list(output[1])
	other = list(output[2])
	
	goodwords = list(set(goodwords))
	badwords = list(set(badwords))
	other = list(set(other))
	
	f = open('pickle/firefox_unigrams.pkl', 'wb')
	pickle.dump(goodwords, f)
	f.close()
	
	firefox = firefox.split()
	bigrams = list(nltk.ngrams(list(firefox), 2))
	
	cleaned_bigrams = []
	for bigram in bigrams:
		bigram1 = bigram[0]
		bigram2 = bigram[1]
		bigram1 = bigram1.encode('utf-8')
		bigram2 = bigram2.encode('utf-8')
		bigram1 = bigram1.lower()
		bigram2 = bigram2.lower()
		if isWord(bigram1) and isWord(bigram2):
			cleaned_bigrams.append((bigram1, bigram2))
			
	f = open('pickle/firefox_bigrams.pkl', 'wb')
	pickle.dump(cleaned_bigrams, f)
	f.close()	
	
def processStateUnion():
	
	#C-Span State of the Union Address Corpus
	#Annual US presidential addresses 1945-2006
	#http://www.c-span.org/executive/stateoftheunion.asp
	
	text_list = state_union.words()
	
	goodwords = []
	badwords = []
	other = []
	for tweet in text_list:
		tokenized = tokenizeTweet(tweet)
		output = cleanInputUnigram(tokenized)
		goodwords.append(output[0])
		badwords.append(output[1])
		other.append(output[2])
	
	goodwords = mergeListItems(goodwords, unique = True)
	badwords = mergeListItems(badwords, unique = True)
	other = mergeListItems(other, unique = True)
	
	f = open('pickle/stateunion_unigrams.pkl', 'wb')
	pickle.dump(goodwords, f)
	f.close()
	
	bigrams = list(nltk.ngrams(text_list, 2))
	
	cleaned_bigrams = []
	for bigram in bigrams:
		bigram1 = bigram[0]
		bigram2 = bigram[1]
		bigram1 = bigram1.encode('utf-8')
		bigram2 = bigram2.encode('utf-8')
		bigram1 = bigram1.lower()
		bigram2 = bigram2.lower()
		if isWord(bigram1) and isWord(bigram2):
			cleaned_bigrams.append((bigram1, bigram2))
						
	f = open('pickle/stateunion_bigrams.pkl', 'wb')
	pickle.dump(cleaned_bigrams, f)
	f.close()
	
def processReuters():
	
    # Reuters-21578 is arguably the most commonly used collection 
    # for text classification during the last two decades
    # The collection consists of 21,578 documents
    # This dataset includes 9,603 documents for training and 3,299 
    # for testing. This split assigns documents from April 7, 1987 
    # and before to the training set, and documents from April 8, 1987 
	
	text_list = reuters.words()
	
	goodwords = []
	badwords = []
	other = []
	for tweet in text_list:
		tokenized = tokenizeTweet(tweet)
		output = cleanInputUnigram(tokenized)
		goodwords.append(output[0])
		badwords.append(output[1])
		other.append(output[2])
	
	goodwords = mergeListItems(goodwords, unique = True)
	badwords = mergeListItems(badwords, unique = True)
	other = mergeListItems(other, unique = True)
	
	f = open('pickle/reuters_unigrams.pkl', 'wb')
	pickle.dump(goodwords, f)
	f.close()
	
	bigrams = list(nltk.ngrams(text_list, 2))
	
	cleaned_bigrams = []
	for bigram in bigrams:
		bigram1 = bigram[0]
		bigram2 = bigram[1]
		bigram1 = bigram1.encode('utf-8')
		bigram2 = bigram2.encode('utf-8')
		bigram1 = bigram1.lower()
		bigram2 = bigram2.lower()
		if isWord(bigram1) and isWord(bigram2):
			cleaned_bigrams.append((bigram1, bigram2))
						
	f = open('pickle/reuters_bigrams.pkl', 'wb')
	pickle.dump(cleaned_bigrams, f)
	f.close()
	
def processNLTKtweets():
	
	# NLTK's Twitter corpus currently contains a sample of 20k Tweets 
	# (named 'twitter_samples') retrieved from the Twitter 
	# Streaming API, together with another 10k which are divided 
	# according to sentiment into negative and positive.
	
	text_list = []
	strings = twitter_samples.strings('tweets.20150430-223406.json')
	for string in strings:
		text_list.append(string)
	strings = twitter_samples.strings('negative_tweets.json')
	for string in strings:
		text_list.append(string)
	strings = twitter_samples.strings('positive_tweets.json')
	for string in strings:
		text_list.append(string)
	
	goodwords = []
	badwords = []
	other = []
	for tweet in text_list:
		tokenized = tokenizeTweet(tweet)
		output = cleanInputUnigram(tokenized)
		goodwords.append(output[0])
		badwords.append(output[1])
		other.append(output[2])
	
	goodwords = mergeListItems(goodwords, unique = True)
	badwords = mergeListItems(badwords, unique = True)
	other = mergeListItems(other, unique = True)
			
	f = open('pickle/nltk_tweet_unigrams.pkl', 'wb')
	pickle.dump(goodwords, f)
	f.close()
	
	bigrams = []
	for tweet in text_list:
		tokenized = tweet.split()
		bigrams.append(list(nltk.ngrams(tokenized, 2)))
	
	cleaned_bigrams = []
	for tweet in bigrams:
		for bigram in tweet:
			bigram1 = bigram[0]
			bigram2 = bigram[1]
			bigram1 = bigram1.encode('utf-8')
			bigram2 = bigram2.encode('utf-8')
			bigram1 = bigram1.lower()
			bigram2 = bigram2.lower()
			if isWord(bigram1) and isWord(bigram2):
				cleaned_bigrams.append((bigram1, bigram2))
				
	f = open('pickle/nltk_tweet_bigrams.pkl', 'wb')
	pickle.dump(cleaned_bigrams, f)
	f.close()

def processAllOld():
	processOldTweets()
	processBrown()
	processOverheard()
	processSingles()
	processFirefox()
	processStateUnion()
	processReuters()
	

def getOldUnigrams():
	
	f = open('pickle/old_tweet_unigrams.pkl', 'rb')
	old_tweet = pickle.load(f)
	
	f = open('pickle/brown_unigrams.pkl', 'rb')
	brown = pickle.load(f)
	
	f = open('pickle/overheard_unigrams.pkl', 'rb')
	overheard = pickle.load(f)
	
	f = open('pickle/singles_unigrams.pkl', 'rb')
	singles = pickle.load(f)
	
	f = open('pickle/firefox_unigrams.pkl', 'rb')
	firefox = pickle.load(f)
	
	f = open('pickle/stateunion_unigrams.pkl', 'rb')
	stateunion = pickle.load(f)
	
	f = open('pickle/reuters_unigrams.pkl', 'rb')
	reuters = pickle.load(f)
	
	f = open('pickle/nltk_tweet_unigrams.pkl', 'rb')
	nltk_tweet = pickle.load(f)
	
	return list(set(old_tweet + brown + overheard + singles \
		+ firefox + stateunion + reuters + nltk_tweet))
	
	
def getOldBigrams():
	
	f = open('pickle/old_tweet_bigrams.pkl', 'rb')
	old_tweet = pickle.load(f)
	
	f = open('pickle/brown_bigrams.pkl', 'rb')
	brown = pickle.load(f)
	
	f = open('pickle/overheard_bigrams.pkl', 'rb')
	overheard = pickle.load(f)
	
	f = open('pickle/singles_bigrams.pkl', 'rb')
	singles = pickle.load(f)
	
	f = open('pickle/firefox_bigrams.pkl', 'rb')
	firefox = pickle.load(f)

	f = open('pickle/stateunion_bigrams.pkl', 'rb')
	stateunion = pickle.load(f)
	
	f = open('pickle/reuters_bigrams.pkl', 'rb')
	reuters = pickle.load(f)
	
	f = open('pickle/nltk_tweet_bigrams.pkl', 'rb')
	nltk_tweet = pickle.load(f)
	
	return old_tweet + brown + overheard + singles + firefox \
		+ stateunion + reuters + nltk_tweet
