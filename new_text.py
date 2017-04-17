from helperfunctions import *
import string
import pickle



def getNewTweets():
	f = open('pickle/new_tweets_english.pkl', 'rb')
	return pickle.load(f)

def processNewTweets():

	new = getNewTweets()
	tweets = []
	for tweet in new:
		tweets.append(tweet[0])
	
	goodwords = []
	badwords = []
	other = []
	for tweet in tweets:
		tokenized = tokenizeTweet(tweet)
		output = cleanInputUnigram(tokenized)
		goodwords.append(output[0])
		badwords.append(output[1])
		other.append(output[2])
	
	goodwords = mergeListItems(goodwords, unique = False)
	badwords = mergeListItems(badwords, unique = True)
	other = mergeListItems(other, unique = True)
			
	f = open('pickle/new_tweet_unigrams.pkl', 'wb')
	pickle.dump(goodwords, f)
	f.close()

	bigrams = []
	for tweet in tweets:
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
				
	f = open('pickle/new_tweet_bigrams.pkl', 'wb')
	pickle.dump(cleaned_bigrams, f)
	f.close()
	
def getNewUnigrams():
	f = open('pickle/new_tweet_unigrams.pkl', 'rb')
	new_uni = pickle.load(f)
	return new_uni


def getNewBigrams():	
	f = open('pickle/new_tweet_bigrams.pkl', 'rb')
	return pickle.load(f)
