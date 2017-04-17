import sqlite3 as sql
from langdetect import detect
import pickle
import ast
from helperfunctions import *

def getNewTweets():
	# Load in all of the scraped Tweets from the database
	# twitter_scrape.py is used to scrape the tweets and
	# place in the database
	con = sql.connect('twitter_scrape.db')
	c = con.cursor()
	con.row_factory = sql.Row

	c.execute("SELECT * FROM tweets")

	component = c.fetchall()

	text_list = []
	for row in component:
		(id, lang, created, text, user_description, user_location, \
			coordinates, id_str, user_name) = tuple(row)
		coord_dict = ast.literal_eval(coordinates)
		coord_list = coord_dict.get('coordinates')
		text_list.append([text,coord_list])
	return text_list
	
		
def isEnglish(input):
	# Google language detection library
	# want to know if Tweet is english
	try:
		lang = detect(input)
		if lang == 'en':
			return True
		else:
			return False
	except:
		return False

tweets = getNewTweets()

tweet_list = []
# Clean the Tweet up so there's just valid words and then
# try to detect if the words are English
# This takes about an hour to run
# Do it once and pickle the result
for tweet in tweets[:10]:
	tweet_text = tweet[0]
	tweet_text = tweet_text.encode('utf-8')
	text_words = tweet_text.split()
	cleaned_text = ''
	for word in text_words:
		if word.isalpha():
			cleaned_text = cleaned_text + ' ' + word
	cleaned_text = cleaned_text.strip()
	tweet = [tweet[0], tweet[1], isEnglish(cleaned_text)] 
	tweet_list.append(tweet)

f = open('pickle/new_tweets_english.pkl', 'wb')
pickle.dump(tweet_list, f)
f.close()
