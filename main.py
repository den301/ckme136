from helperfunctions import *
from old_text import *
from new_text import *
from place_names import *
from bigrams import *
from unigrams import *

# Assemble a corpus of unigrams and bigrams from various NLTK 
# corpora where the text is from 2015 and earlier
processAllOld()

# Take scraped tweets from 2017 and compute the unigrams and bigrams
processNewTweets()

# Need a list of geographical place names. This is used to help
# eliminate unigrams and bigrams from scraped tweets that aren't new
makePlaceList()

# Find new bigrams
# output is in 'output/bigram.csv'
findNewBigrams()

# Find new unigrams
# output is in 'output/unigram.csv'
findNewUnigrams()
