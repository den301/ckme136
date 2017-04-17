from helperfunctions import *
from new_text import *
import pickle

def makePlaceList():

	potential_places = list(set(getNewUnigrams()))
	
	places = Places(potential_places)
	
	f = open('pickle/places.pkl', 'wb')
	pickle.dump(places, f)
	f.close()
	
def getPlaces():
	f = open('pickle/places.pkl', 'rb')
	places = pickle.load(f)
	return places
