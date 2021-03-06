###### INSTRUCTIONS ###### 

# An outline for preparing your final project assignment is in this file.

# Below, throughout this file, you should put comments that explain exactly what you should do for each step of your project. You should specify variable names and processes to use. For example, "Use dictionary accumulation with the list you just created to create a dictionary called tag_counts, where the keys represent tags on flickr photos and the values represent frequency of times those tags occur in the list."

# You can use second person ("You should...") or first person ("I will...") or whatever is comfortable for you, as long as you are clear about what should be done.

# Some parts of the code should already be filled in when you turn this in:
# - At least 1 function which gets and caches data from 1 of your data sources, and an invocation of each of those functions to show that they work 
# - Tests at the end of your file that accord with those instructions (will test that you completed those instructions correctly!)
# - Code that creates a database file and tables as your project plan explains, such that your program can be run over and over again without error and without duplicate rows in your tables.
# - At least enough code to load data into 1 of your dtabase tables (this should accord with your instructions/tests)

######### END INSTRUCTIONS #########

# Put all import statements you need here.

import unittest
import requests
import tweepy
import twitter_info # necessary keys for making twitter API requests
import json
import sqlite3
import re
import collections
from scipy.stats.stats import pearsonr

# Authentication for Twitter searches
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


# Begin filling in instructions....


##### PART 1: RETRIEVING AND ORGANIZING TWITTER API DATA #####


### Set up the caching pattern. The cache file name should be 206_final_project_cache.json: 


CACHE_FNAME = "206_final_project_cache.json"

try:
	cache_file_obj = open(CACHE_FNAME,'r')
	cache_contents = cache_file_obj.read()
	CACHE_DICTION = json.loads(cache_contents) # CACHE_DICTION is the whole contents of the file, in dictionary form
except:
	CACHE_DICTION = {}


### Define a function to get and cache data from Twitter based on a search term. Call the function get_keyword_tweets. The function should return a list of dictionaries, each of which holds information about one tweet. Keys should correspond to the info you'll be loading into the Tweets table:

def get_keyword_tweets(kword):

	unique_identifier = "twitter_keyword_{}".format(kword) 

	if unique_identifier in CACHE_DICTION: 
		print("Using cached data for", kword)
		results = CACHE_DICTION[unique_identifier]

	else: 
		print("Getting data from the web for", kword)

		api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
		results = api.search(q=kword, lang="en")

		# cache the data
		CACHE_DICTION[unique_identifier] = results

		f = open(CACHE_FNAME,'w') 
		f.write(json.dumps(CACHE_DICTION))
		f.close() 	

		
	list_of_dicts = []

	for diction in results['statuses']:

		new_dict = {}
		new_dict['tweet_id'] = diction['id']
		new_dict['tweet_text'] = diction['text']
		new_dict['user_id'] = diction['user']['id']
		new_dict['screen_name'] = diction['user']['screen_name']
		new_dict['movie_title'] = kword
		new_dict['num_faves'] = diction['favorite_count']
		new_dict['num_retweets'] = diction['retweet_count']

		list_of_dicts.append(new_dict)

	return list_of_dicts


#test1 = get_keyword_tweets("hidden figures")
#for x in test1: 
#	print(x)

#print(get_keyword_tweets("titanic")[0].keys())
#print(get_keyword_tweets("mountain bikes"))
#print(get_keyword_tweets("deadpool"))


# test = get_keyword_tweets("michigan")
# print(type(test))

# print(test.keys())  # ['search_metadata', 'statuses']

# print(type(test['search_metadata'])) # dict
# print(type(test['statuses'])) # list

# print(test['search_metadata'].keys()) # ['completed_in', 'since_id_str', 'max_id_str', 'since_id', 'count', 'refresh_url', 'max_id', 'query']
# # ^^ don't care about any of that

# print(test['statuses'][0]) # big dictionary that has info about the tweet

# print(len(test['statuses']))
#print(test['statuses'][0].keys()) # ['entities', 'retweeted_status', 'id_str', 'retweeted', 'geo', 'truncated', 'favorited', 'in_reply_to_screen_name', 'in_reply_to_status_id', 'lang', 'source', 'id', 'text', 'in_reply_to_user_id_str', 'retweet_count', 'coordinates', 'place', 'in_reply_to_user_id', 'metadata', 'in_reply_to_status_id_str', 'created_at', 'is_quote_status', 'user', 'contributors', 'favorite_count']

# # tweet id: 
# print(test['statuses'][0]['id']) # good

# # tweet text: 
# print(test['statuses'][0]['text']) # good

# # user id of person who posted the tweet: 
# print(test['statuses'][0]['user']) #dictionary
# print(test['statuses'][0]['user']['id']) # good

# # title of the movie the tweet is about = keyword

# # number of retweets: 
# print(test['statuses'][0]['retweet_count']) # good

# Keys we want: tweet ID (primary key), tweet text, user ID of the person who posted the tweet (this should connect to the user ID column of the Users table), title of the movie search that this tweet came from (this should connect to the title column of the Movies table), number of favorites, number of retweets




### Define a function to get and cache data from Twitter about a Twitter user. Call the function get_twitter_user. The function should return a dictionary that contains information about the user. Keys should correspond to the info you'll be loading into the Users table: 

def get_twitter_user(username):
	unique_identifier = "twitter_username_{}".format(username)

	if unique_identifier in CACHE_DICTION: 
		print("Using cached data for", username)
		results = CACHE_DICTION[unique_identifier]

	else: 
		print("Getting data from the web for", username)

		api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
		results = api.get_user(username)

		# cache the data
		CACHE_DICTION[unique_identifier] = results

		f = open(CACHE_FNAME,'w') 
		f.write(json.dumps(CACHE_DICTION))
		f.close() 	

	return_dict = {}
	return_dict['user_id'] = results['id']
	return_dict['screen_name'] = results['screen_name']
	return_dict['num_faves'] = results['favourites_count']
	return_dict['num_followers'] = results['followers_count']


	return return_dict


#print(get_twitter_user("UMich"))
#print(get_twitter_user("UMichFootball"))
#print(get_twitter_user("haleybaley24"))

# keys we need: user ID (primary key -- this connects to the user ID column of the Tweets table), user screen name, number of favorites the user has ever made, number of friends the user has


### Define a function to get and cache data from the OMDb API based on a movie title search. Call the function get_movie_data. The function should return a dictionary that contains information about the movie that you'll be loading into the Movies table (example keys: "title", "director", etc.):

def get_movie_data(movie):

	unique_identifier = "movie_{}".format(movie)

	if unique_identifier in CACHE_DICTION:
		print("Using cached data for", movie)
		results = CACHE_DICTION[unique_identifier]

	else:
		print("Getting data from the web for", movie)

		baseurl = "http://www.omdbapi.com/?"
		params = {'t': movie}

		resp = requests.get(baseurl, params=params)
		results = resp.text

		# cache the data
		CACHE_DICTION[unique_identifier] = results

		f = open(CACHE_FNAME,'w') 
		f.write(json.dumps(CACHE_DICTION))
		f.close() 	

	resp_dict = json.loads(results)

	return_dict = {}

	return_dict['title'] = resp_dict['Title']
	return_dict['director'] = resp_dict['Director']
	return_dict['imdb_rating'] = resp_dict['Ratings'][0]['Value']
	return_dict['actors'] = resp_dict['Actors']
	return_dict['langs'] = resp_dict['Language']

	return return_dict

# keys we need: title, director, imdb rating, actors, num langs

#print(get_movie_data("la la land"))
#print(get_movie_data("moonlight"))


### Define the Movie class. One instance will represent one movie.
### The constructor should accept a dictionary that represents a movie.

### The instance variables should be: 
	### self.title (string)
	### self.director (string)
	### self.IMDB_rating (floating point number)
	### self.actors (list of strings)
	### self.num_langs (integer)


### The methods should be: 
	### ___init___ constructor
	### __str___ for a printed representation. Each new line should display one piece of information about the movie (ex: Title: Titanic)
	### get_rating should alter the OMDb request data from a string to a floating point number, and set that floating point number equal to self.IMDB_rating
	### get_actors should alter the OMDb request data from one string to a list of strings, and set that list equal to self.actors
	### get_num_langs should alter the OMDb request data from a string into an integer, and set that integer equal to self.num_langs



class Movie():

	def __init__(self, input_dict):
		self.title = input_dict['title']
		self.director = input_dict['director']
		self.imdb_rating = input_dict['imdb_rating']
		self.actors = input_dict['actors']
		self.num_langs = input_dict['langs']

	def get_rating(self):
		str1 = self.imdb_rating

		# use regular expression to pull out just the number
		rating = re.findall('([0-9]*\.[0-9]*)/', str1)
		rating_str = rating[0]
		rating_float = float(rating_str)
		self.imdb_rating = rating_float


	def get_actors(self):
		str1 = self.actors
		l1 = str1.split(',')
		l2 = [x.strip() for x in l1]
		self.actors = l2



	def get_num_langs(self):
		str1 = self.num_langs

		l1 = str1.split(',')
		self.num_langs = len(l1)

	def __str__(self):
		return "Movie Title: {} \nDirector: {} \nIMDb Rating: {} \nHighest Paid Actor: {} \nNumber of Languages Produced: {}".format(self.title, self.director, str(self.imdb_rating), self.actors[0], str(self.num_langs))


# sample_dict = get_movie_data('la la land')
# m1 = Movie(sample_dict)

# m1.get_rating()
# m1.get_actors()
# m1.get_num_langs()
# print(m1)


# {'imdb_rating': '8.4/10', 'actors': 'Ryan Gosling, Emma Stone, Amiée Conn, Terry Walters', 'director': 'Damien Chazelle', 'langs': 'English', 'title': 'La La Land'}

# {'imdb_rating': '7.6/10', 'actors': 'Mahershala Ali, Shariff Earp, Duan Sanderson, Alex R. Hibbert', 'director': 'Barry Jenkins', 'langs': 'English', 'title': 'Moonlight'}

# str1 = 'English'

# str2 = "English, Swedish"

# l1 = str1.split(',')
# print(l1)

# l2 = str2.split(',')
# print(l2)


## ^^ get_num_langs works on both types of strings ------ write this into a test case


### Create a list of strings called movie_searches. It should contain the 3+ movie titles for which you'll be requesting/handling data:

movie_searches = ['casablanca', 'pulp fiction', 'la la land']


### Create a list called movie_dicts. Each element of the list should be a dictionary that contains OMDb information about that movie. Use the get_movie_data function to accomplish this: 

movie_dicts = []

for movie in movie_searches:
	d = get_movie_data(movie)
	movie_dicts.append(d)


### From movie_dicts, create a list called movie_objects. Each element of movie_objects should be an instance of the Movie class. Use those dictionaries to create the instances! 

movie_objects = []

for d in movie_dicts:
	m1 = Movie(d)
	m1.get_rating()
	m1.get_actors()
	m1.get_num_langs()
	movie_objects.append(m1)

# for obj in movie_objects:
# 	print(type(obj))
# 	print(obj)



### Using the get_keyword_tweets function, make an API request to get Twitter data about the title of each movie. Each time the get_keyword_function is invoked, it returns a list of dictionaries; concatonate those lists together to create one big list of dictionaries, with each dictionary containing information about one tweet. Save that list as all_tweet_dicts: 

all_tweet_dicts = []

for movie in movie_objects:
	resp = get_keyword_tweets(movie.title)
	for d in resp: 
		all_tweet_dicts.append(d)


# print(all_tweet_dicts[0])
# print(all_tweet_dicts[0].keys())
# print(type(all_tweet_dicts[0]['tweet_id']))


### Write code to extract every Twitter username in all_tweet_dicts (all users who posted the tweets, and all users mentioned in the tweets). Make sure there are no repeats. Save that list as all_usernames: 

all_usernames = []

# first we can extract all screen names from all_tweet_dicts

for d in all_tweet_dicts:
	if d['screen_name'] not in all_usernames:
		all_usernames.append(d['screen_name'])

# then use regular expression to find screen names mentioned in the tweet texts

for d in all_tweet_dicts:
	string = d['tweet_text']

	usernames = re.findall('@([A-z0-9_]+)', string)

	for name in usernames: 
		if name not in all_usernames:
			all_usernames.append(name)

#print(all_usernames)

### Using the get_twitter_user function, make an API request to get data about each of the usernames in all_usernames. Save all those dictionaries together in a list called all_user_dicts: 

all_user_dicts = []

for name in all_usernames:
	try:
		user_dict = get_twitter_user(name)
		all_user_dicts.append(user_dict)
	except:
		pass
	# to deal with "user not found" errors

#print(all_user_dicts)



##### PART 2: CREATING THE DATABASE #####


### Create a database called final_project.db that contains the following: 

### A Tweets table, with the following rows: 
	### tweet ID (primary key) 
	### tweet text
	### user ID of the person who posted the tweet (this should connect to the user ID column of the Users table) 
	### title of the movie search that this tweet came from (this should connect to the title column of the Movies table)
	### number of favorites
	### number of retweets


### A Users table, with the following rows: 
	### user ID (primary key -- this connects to the user ID column of the Tweets table)
	### user screen name
	### number of favorites the user has ever made
	### number of followers the user has


### A Movies table, with the following rows: 
	### ID (primary key)
	### title (this should connect to the movie_title column of the Tweets table)
	### director
	### number of languages
	### IMDB rating
	### highest-paid actor in the movie (first in the self.actors list)

conn = sqlite3.connect('final_project.db')
cur = conn.cursor()

statement = 'DROP TABLE IF EXISTS Tweets'
cur.execute(statement)
statement = 'DROP TABLE IF EXISTS Users'
cur.execute(statement)
statement = 'DROP TABLE IF EXISTS Movies'
cur.execute(statement)

table_spec = 'CREATE TABLE IF NOT EXISTS Tweets (tweet_id INTEGER PRIMARY KEY, tweet_text TEXT, user_id INTEGER, movie_title TEXT, favorites INTEGER, retweets INTEGER)'
cur.execute(table_spec)


table_spec = 'CREATE TABLE IF NOT EXISTS Users (user_id INTEGER PRIMARY KEY, screen_name TEXT, num_faves INTEGER, num_followers INTEGER, FOREIGN KEY (user_id) REFERENCES Tweets (user_id) ON UPDATE SET NULL)'
cur.execute(table_spec)


table_spec = 'CREATE TABLE IF NOT EXISTS Movies (id INTEGER PRIMARY KEY, title TEXT, director TEXT, languages INTEGER, imdb_rating NUMERIC(1,1), best_actor TEXT,  FOREIGN KEY (title) REFERENCES Tweets (movie_title) ON UPDATE SET NULL)'
cur.execute(table_spec)

### Write code to load data from all_tweet_dicts into the Tweets table:

# first we need the tweet data to be in tuple form
list_of_tuples = []
unique_ids = []

# dictionary keys: dict_keys(['tweet_text', 'num_faves', 'movie_title', 'tweet_id', 'user_id', 'screen_name', 'num_retweets'])

for td in all_tweet_dicts:
	# tweet id number 
	id_num = td['tweet_id']
	tup = (td['tweet_id'], td['tweet_text'], td['user_id'], td['movie_title'], td['num_faves'], td['num_retweets'])

	# if we have not yet seen this tweet id number in unique_ids, add it to unique_ids and also append the whole tuple
	if id_num not in unique_ids: 
		unique_ids.append(id_num)
		list_of_tuples.append(tup)

# print(len(list_of_tuples))

# print(list_of_tuples)
# for t in list_of_tuples:
# 	print(t[0])

# ids = []
# for t in list_of_tuples:
# 	if t[0] not in ids: 
# 		ids.append(t[0])

# print(len(list_of_tuples)) # 44
# print(len(ids)) # 43
# # there is one tweet in here twice

statement = 'INSERT INTO Tweets VALUES (?, ?, ?, ?, ?, ?)'
for t in list_of_tuples: 
	cur.execute(statement, t)

conn.commit()



### Write code to load data from all_user_dicts into the Users table:

# print(all_user_dicts[0].keys()) # ['num_faves', 'num_followers', 'user_id', 'screen_name']

# get into tuple form
user_tuples =  []
unique_user_ids = []

for ud in all_user_dicts: 

	user_id = ud['user_id']
	tup = (ud['user_id'], ud['screen_name'], ud['num_faves'], ud['num_followers'])

	if user_id not in unique_user_ids: 
		unique_user_ids.append(user_id)
		user_tuples.append(tup)

statement = 'INSERT INTO Users VALUES (?, ?, ?, ?)'
for t in user_tuples: 
	cur.execute(statement, t)

conn.commit()



### Write code to load data from movie_objects into the Movies table: 

movie_tuples = []

for m in movie_objects: 
	tup = (None, m.title, m.director, m.num_langs, m.imdb_rating, m.actors[0])
	movie_tuples.append(tup)


statement = 'INSERT INTO Movies VALUES (?, ?, ?, ?, ?, ?)'
for t in movie_tuples: 
	cur.execute(statement, t)

conn.commit()



##### PART 3: PROCESSING DATA #####


## QUERY 1: USER POPULARITY ##

### Write a query to do the following: 
### For every user in the Users table who has posted a tweet (ie: is present in the UserID column of the Tweets table) grab the following info: 
	### the user's screen name
	### number of followers the user has
	### number of times their tweet was favorited
	### number of times their tweet was retweeted

query = 'SELECT Users.screen_name, Users.num_followers, Tweets.favorites, Tweets.retweets FROM Users INNER JOIN Tweets on Users.user_id = Tweets.user_id'
cur.execute(query)



### From the collections library, create a named tuple with the data you just grabbed. The field names should be: screen_name, num_followers, num_favs, num_retweets (https://docs.python.org/3.3/library/collections.html#collections.namedtuple). Accumulate the named tuples into a list. Save that list as user_popularity: 

pop_tuples = cur.fetchall()
user_popularity = []
PopData = collections.namedtuple('PopData', ['screen_name', 'num_followers', 'num_favs', 'num_retweets'])

for t in pop_tuples:
	named_tup = PopData(screen_name=t[0], num_followers=t[1], num_favs=t[2], num_retweets=t[3])
	user_popularity.append(named_tup)

#print(user_popularity)
#print(user_popularity[0].screen_name) -- each tuple has attributes now!! 


### Compute the correlation between number of followers and number of retweets. Are they related? 

followers = [t.num_followers for t in user_popularity]
retweets = [t.num_retweets for t in user_popularity]
corr = pearsonr(followers, retweets)

print("\n\nThe correlation between number of followers and number of retweets for the tweets in this dataset is {}, with a p-value of {}\n\n".format(corr[0], corr[1]))


## QUERY 2: MOVIE FEEDBACK ##

### For each of the movies that were searched for, write a query to grab and save the following data: 
	### movie title
	### movie IMDb rating
	### number of retweetss for each tweet about that movie


query = 'SELECT Movies.title, Movies.imdb_rating, Tweets.retweets FROM Movies INNER JOIN Tweets on Movies.title = Tweets.movie_title'
cur.execute(query)

movie_tups = cur.fetchall()


### Write code to find the mean number of retweets that each movie recieved in its tweets: 

casablanca_tups = [tup for tup in movie_tups if tup[0] == 'Casablanca']
pulp_tups = [tup for tup in movie_tups if tup[0] == 'Pulp Fiction']
land_tups = [tup for tup in movie_tups if tup[0] == 'La La Land']


casablanca_tot = 0
for tup in casablanca_tups: 
	casablanca_tot += tup[2]
casablanca_mean = casablanca_tot / len(casablanca_tups)

pulp_tot = 0
for tup in pulp_tups: 
	pulp_tot += tup[2]
pulp_mean = pulp_tot / len(pulp_tups)

land_tot = 0
for tup in land_tups: 
	land_tot += tup[2]
land_mean = land_tot / len(land_tups)

#print(casablanca_mean)
#print(pulp_mean)
#print(land_mean)




### Create a dictionary called movie_feedback. Each movie should be a key in the dictionary, with the associated value being a list. The first element of the list should be the movie's IMDb rating, and the second element of the list should be the average number of retweets that movie recieves in its tweets: 

movie_feedback = {}
movie_feedback['Casablanca'] = [casablanca_tups[0][1], casablanca_mean]
movie_feedback['Pulp Fiction'] = [pulp_tups[0][1], pulp_mean]
movie_feedback['La La Land'] = [land_tups[0][1], land_mean]


#print(movie_feedback)


### Sort movie_feedback based on IMDb rating in descending order. Save that list as movies_imdb_sorted:

movies_imdb_sorted = sorted(movie_feedback.keys(), reverse=True, key=lambda x: movie_feedback[x][0])
#print(movies_imdb_sorted)

### Sort movie_feedback based on average retweets in descending order. Save that list as movies_retweets_sorted:  

movies_retweets_sorted = sorted(movie_feedback.keys(), reverse=True, key=lambda x: movie_feedback[x][1])
#print(movies_retweets_sorted)



### Compute the correlation between IMDB rating and number of retweets. Are they related? 

ratings = [movie_feedback[k][0] for k in movie_feedback.keys()]
rtws = [movie_feedback[k][1] for k in movie_feedback.keys()]

corr2 = pearsonr(ratings, rtws)

print("\n\nThe correlation between IMDB rating and average number of retweets for the movies in this dataset is {}, with a p-value of {}\n\n".format(corr2[0], corr2[1]))





## QUERY 3: BEST MOVIES ##

### Write a query to grab and save the following data from the Movies table: 
	### title
	### IMDb rating

query = 'SELECT title, imdb_rating FROM Movies'
cur.execute(query)

### Use a list comprehension to create a new list of only movie titles with IMDb ratings higher than 7. Save this new list as best_movies: 

all_tups = cur.fetchall()

best_movies = [tup[0] for tup in all_tups if tup[1] > 7]
#print(best_movies)



##### PART 4: SAVING THE PROCESSED DATA #####

### Write the processed data into a file called final_project_processed_data.txt. The top of the file should have a heading that says "Processed Data for {movie 1, movie 2, movie 3} as of {current date}":

f = open('final_project_processed_data.txt','w') 
f.write('Processed Data for Casablanca, Pulp Fiction, and La La Land as of 4/20/2017:\n\n\n')
	
### Next, there should be a heading called "Twitter users' popularity" followed by the corresponding data from user_popularity: 

f.write("Twitter Users' Popularity:\n\n")
for t in user_popularity:
	f.write("Username: {}\nFollowers: {}\nTweet Favorites: {}\nTweet Retweets: {}\n\n".format(t.screen_name, t.num_followers, t.num_favs, t.num_retweets))


### Next, there should be a heading called "Movie feedback" followed by the corresponding data from movies_imdb_sorted and movies_retweets_sorted: 

f.write("Movie Feedback:\n\n")

f.write("Movies sorted by IMDB rating:\n\n")
for m in movies_imdb_sorted:
	f.write("{}, {}\n\n".format(m, movie_feedback[m][0]))

f.write("Movies sorted by average number of retweets:\n\n")
for m in movies_retweets_sorted:
	f.write("{}, {}\n\n".format(m, movie_feedback[m][1]))


### Finally, there should be a heading called "Movies with IMDB ratings higher than 7" followed by the corresponding data from best_movies: 

f.write("Movies with IMDB ratings higher than 7:\n\n")

for m in best_movies:
	f.write("{}\n".format(m))



f.close() 

############# TEST CASES ################	
print("\n\n*** OUTPUT OF TESTS BELOW THIS LINE ***\n\n")


# Function to get and cache Twitter data based on a search term
# function name: get_keyword_tweets

class get_keyword_tweets_tests(unittest.TestCase):
	def test_return_type(self):
		result = get_keyword_tweets("deadpool")
		self.assertEqual(type(result[0]['num_faves']), type(2), "Testing that num_faves is an integer.")
	def test_caching(self):
		result = get_keyword_tweets("footloose")
		dict_1 = result[0]
		self.assertEqual(sorted(dict_1.keys()), sorted(['tweet_id', 'num_faves', 'user_id', 'num_retweets', 'movie_title', 'tweet_text', 'screen_name']), "Testing that the get_keyword_tweets function returns dictionaries with the correct keys.")


# Function to get and cache Twitter data based on a username
# function name: get_twitter_user

class get_twitter_user_tests(unittest.TestCase):
	def test_return_type(self):
		userinfo = get_twitter_user("UmichAthletics")
		self.assertEqual(type(userinfo), type({}), "Testing that the get_twitter_user function returns a dictionary.")
	def test_return_type_2(self):
		userinfo = get_twitter_user("UmichAthletics")
		self.assertEqual(len(userinfo.keys()), 4, "Testing that the return dictionary has the correct number of elements.")
	def test_caching(self):
		userinfo = get_twitter_user("UmichAthletics")
		cachefile = open("206_final_project_cache.json", "r")
		cachefile_str = cachefile.read()
		self.assertTrue("twitter_username_UmichAthletics" in cachefile_str, "Testing that the cache file contains a unique identifier from each query.")
		cachefile.close()



# Function to get and cache data from an API request to OMDb
# function name: get_movie_data

class get_movie_data_tests(unittest.TestCase):
	def test_return_content(self):
		moviedata = get_movie_data("Titanic")
		self.assertTrue(len(moviedata.keys()) > 0, "Testing that the API request returns content.")

# when the above test runs, it gives me the following warning: //anaconda/lib/python3.5/json/encoder.py:256: ResourceWarning: unclosed <socket.socket fd=18, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=6, laddr=('192.168.1.146', 50838), raddr=('104.244.42.66', 443)> return _iterencode(o, 0)
# is this a problem? 

	def test_return_content_2(self):
		moviedata = get_movie_data("Titanic")
		self.assertTrue("director" in moviedata.keys(), "Testing that the correct information is retrieved from the API request.")




# List of dicionaries, each containing movie info from an API request

class movie_dicts_tests(unittest.TestCase):
	def test_element_type(self):
		self.assertEqual(type(movie_dicts[1]), type({}), "Testing that the elements of movie_dicts are dictionaries.")
	def test_dict_keys(self):
		self.assertTrue("title" in movie_dicts[0].keys(), "Testing that the correct information is in the movie dictionaries.")



## Remember to invoke all your tests...

unittest.main(verbosity=2)


# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)