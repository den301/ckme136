import nltk
from nltk.corpus import stopwords
import csv
from helperfunctions import *
from old_text import *
from new_text import *
import itertools
from place_names import *

def findNewUnigrams():
	# Get unigrams from scraped Tweets
	# count the occurence of each distinct unigram and place in dictionary
	# key is the unigram and value is the number of occurences
	new_unigrams = getNewUnigrams()
	new_unigrams_dict = dict(Counter(new_unigrams))
	
	# Get unigrams from NLTK corpora
	# count the occurence of each distinct unigram and place in dictionary
	# key is the unigram and value is the number of occurences
	old_unigrams = getOldUnigrams()
	old_unigrams_dict = dict(Counter(old_unigrams))
	
	# if a unigram is in the NLTK corpora from 2015 and earlier it
	# can't be a 'new word'. Find the unigrams from the scraped tweets
	# that aren't in the older corpora, assume these are 'new words'
	dict_diff = { k : new_unigrams_dict[k] for k in set(new_unigrams_dict) - set(old_unigrams_dict) }
	
	# assume that a 'new word' will be mentioned more than 5 times
	# otherwise it's either not a word, a typo, etc
	items = [(v, k) for k, v in dict_diff.items()]
	items.sort()
	more_than = [(k, v) for v, k in items if v > 5]
	
	# get list of unigrams that are just places, probably
	# not a new phrase
	geo_clean = []
	places = set(getPlaces())
	for unigram in more_than:
		if unigram[0] not in places:
			geo_clean.append(unigram)
	
	# get rid of unigrams where one or both words are stop words		
	stop_word_clean = []
	stop_words = set(stopwords.words('english'))
	for unigram in geo_clean:
		if unigram[0] not in stop_words:
			stop_word_clean.append(unigram)
	
	# get rid of unigrams where one or both words is only two letters
	two_letter_clean = []
	for unigram in stop_word_clean:
		if len(unigram[0]) > 2:
			two_letter_clean.append(unigram)
	
	# a lot of the scraped Tweets are for job postings
	# this results in a lot of the unigrams being job titles. Remove these.
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
	for unigram in two_letter_clean:
		if unigram[0] not in job_words:
			job_word_clean.append(unigram)
				

	print('unigram Summary')
	print('')
	print('New unigrams undistinct: ', len(new_unigrams))
	print('New unigrams distinct: ', len(new_unigrams_dict))
	print('')
	print('Old unigrams undistinct: ', len(old_unigrams))
	print('Old unigrams distinct: ', len(old_unigrams_dict))
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
	
	tupleToCsv(job_word_clean, 'output/unigram.csv')
