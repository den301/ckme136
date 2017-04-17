from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
import json
import dataset

API_KEY = 'uj*******************************ex'
API_SECRET = 'nP**********************************************************03'
TOKEN_KEY = '23***********************************************************V1'
TOKEN_SECRET = 'Is*******************************************************gC'

class Listener(StreamListener):
	
	def on_status(self, status):
    # The tweet attributes of interest to be stored
		description = status.user.description
		text = status.text
		coords = status.coordinates
		loc = status.user.location
		created = status.created_at
		id_str = status.id_str
		name = status.user.screen_name
		lang = status.lang
		 
		if coords is not None:
      # Only store the Tweet if there are geo coords
			coords = json.dumps(coords)
			try:
				table.insert(dict(
					user_description=description,
					user_location=loc,
					coordinates=coords,
					text=text,
					user_name=name,
					id_str=id_str,
					created=created,
					#retweeted = retweeted_status,
					lang = lang,
				))
				print(text)
			except ProgrammingError as err:
				print(err)
			
	def on_error(self, status_code):
		if status_code == 420:
			return False
      
# Authorize user with Twitter		
auth = OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(TOKEN_KEY, TOKEN_SECRET)

# Store tweets in SQLite Database, table is called 'tweets'
db = dataset.connect('sqlite:///twitter_scrape.db')
table = db['tweets']

# Real time stream tweets and store in database.
# Geo coordinates are set to capture all of southern Canada
# Didn't bother with northern part of Canada where population is small
# Section of US that is north of Southern Ontario included as well
stream = Stream(auth, Listener())
stream.filter(locations=[-138,42.9,-47.4,58])
