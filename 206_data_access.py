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

movies = ["Zootopia", "Oldboy", "Inception"]

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
	imdbid = movie["imdbID"]

	imdb_info = [titles, directors, ratings, actorss, languages, boxoffices, imdbid]
	imdb.append(imdb_info)


###Class Movie

class Movie():

	def __init__(self, title, director, rating, actors, language, boxoffice):
		self.title = title
		self.director = director
		self.rating = rating
		self.actors = actors
		self.language = len(language.split(","))
		self.boxoffice = boxoffice

	def __str__(self):
		return "\n The title of the movie is {}. The director of the movie is {}. Its rating is {} and starring actors are {}. It is translated in {} different languages, and its Box Office earning is {}.\n".format(self.title, self.director, self.rating, self.actors, self.language, self.boxoffice)

	def good_movie(rating, title):		
		if float(rating) > 7:
			return "\n{} is a good movie.".format(title)
		elif float(rating) > 5:
			return "\n{} is an average movie.".format(title)
		else:
			return "\n{} is a low rated movie".format(title)
	# one more method

#### Calling class Movie

mg = imdb[0]
av = imdb[1]
ic = imdb[2]


Mean_Girls_info = Movie(mg[0], mg[1], mg[2], mg[3], mg[4], mg[5])
Avengers_info = Movie(av[0], av[1], av[2], av[3], av[4], av[5])
Inception_info = Movie(ic[0], ic[1], ic[2], ic[3], ic[4], ic[5])

MGnumber = Movie.good_movie(mg[2], mg[0])
AVnumber = Movie.good_movie(av[2], av[0])
ICnumber = Movie.good_movie(ic[2], ic[0])

print(MGnumber)
print(AVnumber)
print(ICnumber)

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
table_spec += 'text TEXT, screen_name TEXT, user_id INTEGER, Movie_Title TEXT, Favorites INTEGER, retweets INTEGER)'

cur.execute(table_spec)


## Setting up Users table
cur.execute('DROP TABLE IF EXISTS Users') 

table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Users (user_id INTEGER PRIMARY KEY, '
table_spec += 'screen_name TEXT, num_favs INTEGER, description TEXT)' #add number of followers

cur.execute(table_spec)

statement = 'DELETE FROM Tweets'
cur.execute(statement)


## Setting up Movies table

cur.execute('DROP TABLE IF EXISTS Movies') 

table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Movies (movie_id TEXT PRIMARY KEY, '
table_spec += 'Movie_Title TEXT, Director TEXT, Rating TEXT, Top_Billed_Actor TEXT, Languages TEXT, Box_Office TEXT)'

cur.execute(table_spec)

statement = 'DELETE FROM Users'
cur.execute(statement)



#------------------------------------------------------------------------------

#### PART 6: Loading information into tables

## Load to Tweets table
list_of_tweets = []
for x in movie_tweets:
	w = x["statuses"]
	for y in w:
		z  = (y["id"], y["text"], y["user"]["screen_name"], y["user"]["id"], x["search_metadata"]["query"], y["favorite_count"], y["retweet_count"])
		list_of_tweets.append(z)


statement = 'INSERT INTO Tweets VALUES (?, ?, ?, ?, ?, ?, ?)'

for x in list_of_tweets:
	cur.execute(statement, x)




## Load to Users table
list_of_users = []
for x in movie_tweets:
	w = x["statuses"]
	for y in w:
		n = y["user"]
		j = (n["id"], n["screen_name"], api.get_user(n["id"])["favourites_count"], api.get_user(n["id"])["description"])
		list_of_users.append(j)


statement = 'INSERT OR IGNORE INTO Users VALUES (?, ?, ?, ?)'

for x in list_of_users:
	cur.execute(statement, x)




## Load to Movies table
list_of_movies = []
for x in imdb:

	z = (x[6], x[0], x[1], x[2], x[3], x[4], x[5])
	list_of_movies.append(z)

# print (list_of_movies)


statement = 'INSERT OR IGNORE INTO Movies VALUES (?, ?, ?, ?, ?, ?, ?)'

for x in list_of_movies:
	cur.execute(statement, x)

conn.commit()




#------------------------------------------------------------------------------



# You must process the data you gather and store and extract from the database in at least four of the following ways:

# Set / dictionary comprehensions, and/or list comprehensions
# Using new containers from the collections library
# Using iteration methods from the itertools library
# Accumulation in dictionaries and processing of the data (e.g. counts, lists associated with keys… like umsi_titles, but of course something different)
# Using generator expressions and/or generator functions (recall HW6)
# Sorting with a key parameter
# Using the builtins: map or filter (which each return iterators) in order to filter a sequence or transform a sequence of data
# Using regular expressions

# At least 2 test methods pertaining to each function and to each class method you define. Basically, you must have a test suite for your code! It should cover edge cases, just like we've focused on and/or looked at all semester. You should write your tests first, and, following that, use the iterative process of tests and code that we've discussed in class… Writing tests initially part of one of these upcoming assignments! See more below.

# You must ultimately provide a complete README file in a clear, readable outline structure, which should be a .PDF or a .txt file. Like Project 1, you must provide a complete set of documentation for your code. It should not be essay-format (we're a little more strict now that you have more experience writing and using documentation), but rather documentation outline format. We'll show some examples! It must contain all of the information listed in the README REQUIREMENTS.

#### PART 7: Making queries



# how many total retweets are there per movie out of the tweets gathered (join movie titles)
q1 = "SELECT Movies.Movie_Title, Tweets.retweets from Movies LEFT JOIN Tweets on Movies.Movie_Title = Tweets.Movie_Title"

cur.execute(q1)
retweet_100 = cur.fetchall()


d = defaultdict(list)
for k, v in retweet_100:
	if v is not None:
		d[k].append(v)

twitter_info_diction = dict(d)


total = []
acc = 0
for value in twitter_info_diction.values():
	for rtnum in value:
		acc += rtnum
	total.append(acc)


movie_names = []
for key in twitter_info_diction.keys():
	movie_names.append(key)

total_RTs = list(zip(movie_names,total))


for x in total_RTs:
	sent = "The total number of retweets for the movie "+str(x[0])+" is " + str(x[1])+" retweets."
	print (sent)



# see if the movie title is in the user's description
# q3 = "SELECT description from Users WHERE Movies.Top_Billed_Actor is "

#use regular expression

q2 = "SELECT description from Users"
cur.execute(q2)
all_text = [''.join(x) for x in cur.fetchall()]



description_words = [x.split() for x in all_text]

all_words = [item for sublist in description_words for item in sublist]

cnt = 0
for word in all_words:
	if "movie" == word:
		cnt += 1
	elif "Movie" == word:
		cnt += 1


print ("\n The word 'Movie' is mentioned " + str(cnt)+ " times in Twitter user descriptions.")


#Most popular word from popular tweets (tweets retweeted more than 10 times)


q3 = "SELECT text FROM Tweets WHERE retweets > 10"
cur.execute(q3)

popular_tweets = [''.join(x) for x in cur.fetchall()]

popular_words = {tuple(x.split()) for x in popular_tweets}

count = Counter()
for words in popular_words:
	for word in words:
		count[word] += 1

x = count.most_common(1)
most_common_word = x[0][0]
number_of_times = x[0][1]

print('\n Most popular word used in tweets over 10 retweets is ' +str(most_common_word) + ' and it is mentioned ' + str(number_of_times) + ' times.')


#### PART 8: Create an output file

# Make a text file with a nice summary of each movie with its total number of retweets, how many times the word "movie" is mentioned in user's description, and what the most popular word used in tweets over 10 retweets is.

result_fname = "206_final_project_result_summary"



f = open(result_fname, 'w')
f.write(str(Mean_Girls_info))
f.write(MGnumber)
f.write("\n\n\n")
f.write(str(Avengers_info))
f.write(AVnumber)
f.write("\n\n\n")
f.write(str(Inception_info))
f.write(ICnumber)
f.write("\n\n\n\n\n")

for x in total_RTs:
	sent = "\nThe total number of retweets for the movie "+str(x[0])+" is " + str(x[1])+" retweets.\n\n"
	f.write (sent)

f.write("\n The word 'Movie' is mentioned " + str(cnt)+ " times in Twitter user descriptions.\n\n")

f.write('\n Most popular word used in tweets over 10 retweets is ' +str(most_common_word) + ' and it is mentioned ' + str(number_of_times) + ' times.\n\n')

f.close() 


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

class Testing(unittest.TestCase):
    def test_cache_Twitter(self):
        self.assertEqual(type(tweets), type({}), "testing Twitter cached data is a dictionary")

    def test_imdb_id(self):
    	testid = search_imdb_ID("Zootopia")
    	self.assertEqual(str(testid), "tt2948356")

    def test_cache_IMDB(self):
        self.assertEqual(type(imdb_data[0]), type({}), "testing IMDb cached data is a list of dictionary")

    def test_class_Movie(self):
    	self.assertEqual("\n The title of the movie is Zootopia. The director of the movie is Byron Howard, Rich Moore, Jared Bush. Its rating is 8.1 and starring actors are Ginnifer Goodwin, Jason Bateman, Idris Elba, Jenny Slate. It is translated in 1 different languages, and its Box Office earning is $341,264,012.00.\n", str(Mean_Girls_info))


    def test_rating(self):
    	self.assertEqual("Zootopia is a good movie.", str(MGnumber))

    def test_Tweets_table(self):
    	conn = sqlite3.connect('206_final_data.db')
    	cur = conn.cursor()
    	cur.execute('SELECT * FROM Tweets');
    	result = cur.fetchall()
    	self.assertTrue(len(result[1])==7,"Testing that there are 7 columns in the Tweets table")
    	conn.close()

    def test_Users_table(self):
    	conn = sqlite3.connect('206_final_data.db')
    	cur = conn.cursor()
    	cur.execute('SELECT * FROM Users');
    	result = cur.fetchall()
    	self.assertTrue(len(result[1])==4,"Testing that there are 4 columns in the Users table")
    	conn.close()

    def test_Movies_table(self):
    	conn = sqlite3.connect('206_final_data.db')
    	cur = conn.cursor()
    	cur.execute('SELECT * FROM Movies');
    	result = cur.fetchall()
    	self.assertTrue(len(result[1])==7,"Testing that there are 7 columns in the Movies table")
    	conn.close()

    def test_description_words(self):
    	self.assertEqual(type(all_words), type([]))

    def test_total_RTS(self):
    	self.assertEqual(type(total_RTs), type([]))

    def test_most_common_word(self):
    	self.assertEqual(type(most_common_word, type("hi")))

    def test_number_of_times(self):
    	self.assertEqual(type(number_of_times, type(1)))
 

unittest.main(verbosity=2)


# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)