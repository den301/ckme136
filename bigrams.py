import nltk
from nltk.corpus import stopwords
import csv
from helperfunctions import *
from old_text import *
from new_text import *
import itertools
from place_names import *

def findNewBigrams():
	# Get bigrams from scraped Tweets
	# count the occurence of each distinct bigram and place in dictionary
	# key is the bigram and value is the number of occurences
	new_bigrams = getNewBigrams()
	new_bigrams_dict = dict(Counter(new_bigrams))
	
	# Get bigrams from NLTK corpora
	# count the occurence of each distinct bigram and place in dictionary
	# key is the bigram and value is the number of occurences
	old_bigrams = getOldBigrams()
	old_bigrams_dict = dict(Counter(old_bigrams))
	
	# if a bigram is in the NLTK corpora from 2015 and earlier it
	# can't be a 'new phrase'. Find the bigrams from the scraped tweets
	# that aren't in the older corpora, assume these are 'new phrases'
	dict_diff = { k : new_bigrams_dict[k] for k in set(new_bigrams_dict) - set(old_bigrams_dict) }
	
	# assume that a 'new phrase' will be mentioned more than 5 times
	# otherwise it's either not a phrase, a typo, etc
	items = [(v, k) for k, v in dict_diff.items()]
	items.sort()
	more_than = [(k, v) for v, k in items if v > 5]
	
	# get list of bigrams that are just places, probably
	# not a new phrase
	geo_clean = []
	places = set(getPlaces())
	for bigram in more_than:
		if bigram[0][0] not in places and bigram[0][1] not in places:
			geo_clean.append(bigram)
	
	# get rid of bigrams where one or both words are stop words		
	stop_word_clean = []
	stop_words = set(stopwords.words('english'))
	for bigram in geo_clean:
		if bigram[0][0] not in stop_words and bigram[0][1] not in stop_words:
			stop_word_clean.append(bigram)
	
	# get rid of bigrams where one or both words is only two letters
	two_letter_clean = []
	for bigram in stop_word_clean:
		if len(bigram[0][0]) > 2 and len(bigram[0][1]) > 2:
			two_letter_clean.append(bigram)
	
	# a lot of the scraped Tweets are for job postings
	# this results in a lot of the bigrams being job titles. Remove these.
	# open dataset that is list of occupations is available at
	# http://data.okfn.org/data/johnlsheridan/occupations in csv format
	job_terms = []
	with open('occupations.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			job_terms.append(row)
	job_words = []
	for job in job_terms:
		words = job[0].split()
		job_words.append(words)
	job_words = mergeListItems(job_words, unique = True)
	job_words = [x.lower() for x in job_words]
	job_word_clean = []
	for bigram in two_letter_clean:
		if bigram[0][0] not in job_words and bigram[0][1] not in job_words:
			job_word_clean.append(bigram)
				

	print('Bigram Summary')
	print('')
	print('New bigrams undistinct: ', len(new_bigrams))
	print('New bigrams distinct: ', len(new_bigrams_dict))
	print('')
	print('Old bigrams undistinct: ', len(old_bigrams))
	print('Old bigrams distinct: ', len(old_bigrams_dict))
	print('')
	print('Exclusively new distinct: ', len(items))
	print('')
	print('Exclusively new distinct, more than 5: ', len(more_than))
	print('')
	print('Geo-cleaned: ', len(geo_clean))
	print('')
	print('Stop word cleaned: ', len(stop_word_clean))
	print('')
	print('Two letter cleaned: ', len(two_letter_clean))
	print('')
	print('Job word cleaned: ', len(job_word_clean))
	
	tupleToCsv(job_word_clean, 'output/bigram.csv')
