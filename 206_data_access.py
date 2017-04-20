###### INSTRUCTIONS ###### 

#### Follow the Option 2 instructions for the SI206 final project. 

#### You are required to define a class Movie. It should accept a dictionary that represents a movie and have 3 instance variables and 2 methods. You need to save the each movie by saving it in instance variable or a defining method that will compute these things: title, director, IMDB rating, list of actos, number of languages, and budget. 

#### You need to pick at least 3 movie title search terms for OMDB and make a request to OMDB on each of those 3 terms.

#### Then you need to invoate your Twitter fucntions to access the number of times the movie's Twitter account mentions the starring actor from the movie. You also need to access all the tweets from each of the statuses about the three movies that has over 500 retweets. 

#### You need to access data about Twitter users to get information about the users. And essentially create three database tables called "Tweets", "Users", and "Movies" and these tables should hold the according columns shown in the instructions. 

#### You will then load into your database and create an output file, which will be a text file with a nice summary of each movie with it's tweets over 500 retweets and how much the starring ator loves the director of the movie. 

######### END INSTRUCTIONS #########

# Put all import statements you need here.
import requests
import unittest
import itertools
from collections import Counter 
from collections import defaultdict
import tweepy
import twitter_info 
import json
import sqlite3


#####

##### TWEEPY SETUP CODE:
# Authentication information should be in a twitter_info file...
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

##### END TWEEPY SETUP CODE

#------------------------------------------------------------------------------

#### PART 1: CACHING TWITTER DATA

CACHE_FNAME = "SI206_final_cache.json"

try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}



def get_user_tweets(term): #FUNCTION TO CACHE TWITTER DATA
	unique_identifier = 'twitter_{}'.format(term)
	if unique_identifier in CACHE_DICTION:
		print('using cached data for', term)
		twitter_results = CACHE_DICTION[unique_identifier]
	else:
		print('getting data from internet for', term)
		twitter_results = api.search(q = term, count = 20)
		CACHE_DICTION[unique_identifier] = twitter_results
		f = open(CACHE_FNAME, 'w')
		f.write(json.dumps(CACHE_DICTION))
		f.close() 
	return twitter_results






#------------------------------------------------------------------------------

#### PART 2: CACHING IMDB DATA

def search_imdb_ID(title): # SEARCHING IMDB ID TO LOOK UP INFO AND FIGURE OUT THE PRIMARY KEY
	baseurl = "http://www.omdbapi.com/?"
	imdb_params = {"t":title}
	req = requests.get(baseurl, params = imdb_params)
	imdb_data = json.loads(req.text)
	imdb_id = imdb_data["imdbID"]
	return imdb_id


def get_imdb_data(search_ID):
	unique_identifier = 'imdb_{}.'.format(search_ID)
	if unique_identifier in CACHE_DICTION:
		print('using cached data for', search_ID)
		imdb_results = CACHE_DICTION[unique_identifier]
	else:
		print('getting data from internet for', search_ID)
		
		baseurl = "http://www.omdbapi.com/?"
		imdb_params = {"i":search_ID}
		req = requests.get(baseurl, params = imdb_params)

		imdb_results = req.text
		CACHE_DICTION[unique_identifier] = imdb_results

		f = open(CACHE_FNAME, 'w')
		f.write(json.dumps(CACHE_DICTION))
		f.close()
	return imdb_results



#------------------------------------------------------------------------------

#### PART 3: Invoking Functions

movies = ["Mean Girls", "Avengers", "Inception"]

imdb_ids = []
movie_tweets = []
for x in movies:

	ids = search_imdb_ID(x) #Calling search_imdb_ID function to look up imdb ids for each movie
	imdb_ids.append(ids)

	tweets = get_user_tweets(x) #Calling get_user_tweets function to gather twitter search results for each movie
	movie_tweets.append(tweets)

imdb_data = []

for x in imdb_ids:
	data = json.loads(get_imdb_data(x)) #Calling get_imdb_data
	imdb_data.append(data)


imdb = []

for movie in imdb_data:
	titles = movie["Title"]
	directors = movie["Director"]
	ratings = movie["imdbRating"]
	actorss =  movie["Actors"]
	languages = movie["Language"]
	boxoffices = movie["BoxOffice"]	

	imdb_info = [titles, directors, ratings, actorss, languages, boxoffices]
	imdb.append(imdb_info)
print (imdb)



class Movie():

	def __init__(self, title, director, rating, actors, language, boxoffice):
		self.title = title
		self.director = director
		self.rating = rating
		self.actors = actors
		self.language = len(language)
		self.boxoffice = boxoffice

	def __str__(self):
		return "\n The title of the movie is {}. The director of the movie is {}. Its rating is {} and starring actors are {}. It is translated in {} different languages, and its Box Office earning is {}.\n".format(self.title, self.director, self.rating, self.actors, self.language, self.boxoffice)


#### Calling class Movie

mg = imdb[0]
av = imdb[1]
ic = imdb[2]


Mean_Girls_info = Movie(mg[0], mg[1], mg[2], mg[3], mg[4], mg[5])
Avengers_info = Movie(av[0], av[1], av[2], av[3], av[4], av[5])
Inception_info = Movie(ic[0], ic[1], ic[2], ic[3], ic[4], ic[5])

# call_class_Movie = {"Mean_Girls_info": Mean_Girls_info, "Avengers_info" : Avengers_info, "Inception_info": Inception_info}
print (Mean_Girls_info)
print (Avengers_info)
print (Inception_info)

#------------------------------------------------------------------------------

#### PART 4: Setting up database file
conn = sqlite3.connect('206_final_data.db')
cur = conn.cursor()



#------------------------------------------------------------------------------

#### PART 5: Setting up database tables

## Setting up Tweets table
cur.execute('DROP TABLE IF EXISTS Tweets') 

table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Tweets (tweet_id INTEGER PRIMARY KEY, '
table_spec += 'text TEXT, screen_name TEXT, Movie_Title TEXT, Favorites INTEGER, retweets INTEGER)'

cur.execute(table_spec)


## Setting up Users table
table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Users (user_id INTEGER PRIMARY KEY, '
table_spec += 'screen_name TEXT, num_favs INTEGER, description TEXT)'

cur.execute(table_spec)

statement = 'DELETE FROM Tweets'
cur.execute(statement)


## Setting up Movies table
table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Movies (movie_id INTEGER PRIMARY KEY, '
table_spec += 'Movie_Title TEXT, Director TEXT, Rating TEXT, Top Billed Actor TEXT, Box Office TEXT)'

cur.execute(table_spec)

statement = 'DELETE FROM Users'
cur.execute(statement)



#------------------------------------------------------------------------------

#### PART 6: Loading information into tables

## Load to Tweets table
lst = []
for x in movie_tweets:
	w = x["statuses"]
	for y in w:
		z  = (y["id"], y["text"], y["user"]["screen_name"], x["search_metadata"]["query"], y["favorite_count"], y["retweet_count"])
		lst.append(z)


statement = 'INSERT INTO Tweets VALUES (?, ?, ?, ?, ?, ?)'

for x in lst:
	cur.execute(statement, x)



## Load to Users table

# user_lst = []
# for x in movie_tweets:
# 	for single_tweet in x:
# 		y = single_tweet
# 		t = y["entities"]["user_mentions"]
# 		for n in t:
# 			j = (n["id_str"], n["screen_name"], api.get_user(n["id_str"])["favourites_count"], api.get_user(n["id_str"])["description"])
# 			user_lst.append(j)

# # print(user_lst)
# statement = 'INSERT OR IGNORE INTO Users VALUES (?, ?, ?, ?)'

# for x in user_lst:
# 	cur.execute(statement, x)




## Load to Movies table

conn.commit()




#------------------------------------------------------------------------------


#### PART 7: Making queries

# I want to make a query that accesses the number of times the movie Twitter mentions a specific starring actor from the movie.

# I want to make a query that accesses all the tweets from each of the movie Twitter accounts with over 500 favorites. 




#------------------------------------------------------------------------------

#### PART 8: Create an output file

# Make a text file with a nice summary of each movie with it's tweets over 500 retweets and how much the starring ator loves the director of the movie. 




#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

class Testing(unittest.TestCase):
    def test_1(self):
        self.assertEqual(type(tweets), type({}), "testing Twitter cached data is a dictionary")

    def test_2(self):
        self.assertEqual(type(imdb_data[0]), type({}), "testing IMDb cached data is a list of dictionary")

    def test_3(self):
    	conn = sqlite3.connect('206_final_data.db')
    	cur = conn.cursor()
    	cur.execute('SELECT * FROM Tweets');
    	result = cur.fetchall()
    	self.assertTrue(len(result[1])==6,"Testing that there are 6 columns in the Tweets table")
    	conn.close()

    def test_4(self):
    	conn = sqlite3.connect('206_final_data.db')
    	cur = conn.cursor()
    	cur.execute('SELECT * FROM Users');
    	result = cur.fetchall()
    	self.assertTrue(len(result[1])==4,"Testing that there are 4 columns in the Users table")
    	conn.close()

    def test_5(self):
    	conn = sqlite3.connect('206_final_data.db')
    	cur = conn.cursor()
    	cur.execute('SELECT * FROM Movies');
    	result = cur.fetchall()
    	self.assertTrue(len(result[1])==7,"Testing that there are 7 columns in the Users table")
    	conn.close()

    def test_6(self):
        self.assertEqual(type(actor_and_director), type({"hi":"hi"}))


    def test_7(self):
        self.assertEqual(type(popular_tweets),type({"hi":3}))


    def test_8(self):
        self.assertEqual(type(list(actor_and_director.keys())[0]),type(""),"Testing that a key of the dictionary is a string")

    def test_9(self):
        self.assertEqual(type(list(actor_and_director.values())[0]),type(1),"Testing that a key of the dictionary is an integer")

    def test_10(self):
        self.assertEqual(type(list(popular_tweets.keys())[0]),type(1),"Testing that a value in the dictionary is an integer")

    def test_10(self):
        self.assertEqual(type(list(popular_tweets.keys())[0]),type(""),"Testing that a value in the dictionary is a string")

unittest.main(verbosity=2)


# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)