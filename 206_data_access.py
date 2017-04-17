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

# Keys we want: 
	### tweet ID (primary key) 
	### tweet text
	### user ID of the person who posted the tweet (this should connect to the user ID column of the Users table) 
	### title of the movie search that this tweet came from (this should connect to the title column of the Movies table)
	### number of favorites
	### number of retweets





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

# keys we need: 
	### user ID (primary key -- this connects to the user ID column of the Tweets table)
	### user screen name
	### number of favorites the user has ever made
	### number of friends the user has


### Define a function to get and cache data from the OMDb API based on a movie title search. Call the function get_movie_data. The function should return a dictionary that contains information about the movie that you'll be loading into the Movies table (example keys: "title", "director", etc.):

def get_movie_data(movie):

	unique_identifier = "movie_.{}".format(movie)

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


### Create a list of strings called movie_searches. It should contain the 3+ movie titles for which you'll be requesting/handling data:


### Create a list called movie_dicts. Each element of the list should be a dictionary that contains OMDb information about that movie. Use the get_movie_data function to accomplish this: 


### From movie_dicts, create a list called movie_objects. Each element of movie_objects should be an instance of the Movie class. Use those dictionaries to create the instances! 


### Using the get_keyword_tweets function, make an API request to get Twitter data about the star actor from each movie. Each time the get_keyword_function is invoked, it returns a list of dictionaries; concatonate those lists together to create one big list of dictionaries, with each dictionary containing information about one tweet. Save that list as all_tweet_dicts: 


### Write code to extract every Twitter username in all_tweet_dicts (all users who posted the tweets, and all users mentioned in the tweets). Make sure there are no repeats. Save that list as all_usernames: 


### Using the get_twitter_user function, make an API request to get data about each of the usernames in all_usernames. Save all those dictionaries together in a list called all_user_dicts: 



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
	### title
	### director
	### number of languages
	### IMDB rating
	### highest-paid actor in the movie (first in the self.actors list)
	### total number of awards & nominations the movie recieved


### Write code to load data from all_tweet_dicts into the Tweets table:


### Write code to load data from all_user_dicts into the Users table:


### Write code to load data from movie_objects into the Movies table: 



##### PART 3: PROCESSING DATA #####


## QUERY 1: USER POPULARITY ##

### Write a query to do the following: 
### For every user in the Users table who has posted a tweet (ie: is present in the UserID column of the Tweets table) grab the following info: 
	### user ID
	### number of followers the user has
	### number of times their tweet was favorited
	### number of times their tweet was retweeted


### From the collections library, create a named tuple with the data you just grabbed. The field names should be: user_ID, num_followers, num_favs, num_retweets (https://docs.python.org/3.3/library/collections.html#collections.namedtuple). Accumulate the named tuples into a list. Save that list as user_popularity: 



## QUERY 2: MOVIE FEEDBACK ##

### For each of the movies that were searched for, write a query to grab and save the following data: 
	### movie title
	### movie IMDb rating
	### number of favorites for each tweet about that movie

### Write code to find the mean number of favorites that each movie recieved in its tweets: 

### Create a dictionary called movie_feedback. Each movie should be a key in the dictionary, with the associated value being a list. The first element of the list should be the movie's IMDb rating, and the second element of the list should be the average number of favorites that movie recieves in its tweets: 

### Sort movie_feedback based on IMDb rating in descending order. Save that list as movies_imdb_sorted:

### Sort movie_feedback based on average favorites in descending order. Save that list as movies_favorites_sorted:  



## QUERY 3: BEST MOVIES ##

### Write a query to grab and save the following data from the Movies table: 
	### title
	### IMDb rating

### Use a list comprehension to create a new list of only movies with IMDb ratings higher than 7. Save this new list as best_movies: 



##### PART 4: SAVING THE PROCESSED DATA #####

### Write the processed data into a file called final_project_processed_data.txt. The top of the file should have a heading that says "Processed Data for {movie 1, movie 2, movie 3} as of {current date}":

### Next, there should be a heading called "Twitter users' popularity" followed by the corresponding data from user_popularity: 

### Next, there should be a heading called "Movie feedback" followed by the corresponding data from movies_imdb_sorted and movies_favorites_sorted: 

### Finally, there should be a heading called "High-rated movies" followed by the corresponding data from best_movies: 





############# TEST CASES ################	


# Put your tests here, with any edits you now need from when you turned them in with your project plan.

# Cache file name: final_project_cache.json
# List of movie dictionaries: movie_dicts

# Write your test cases here.

# Function to get and cache Twitter data based on a search term
# function name: get_keyword_tweets

class get_keyword_tweets_tests(unittest.TestCase):
	def test_return_type(self):
		result = get_keyword_tweets("deadpool")
		self.assertEqual(type(result[0]), type({}), "Testing that the get_keyword_tweets function returns a list of dictionaries.")
	def test_caching(self):
		result = get_keyword_tweets("mountain bikes")
		dict_1 = result[0]
		self.assertEqual(sorted(dict_1.keys()), sorted(['tweet_id', 'num_faves', 'user_id', 'num_retweets', 'movie_title', 'tweet_text']), "Testing that the get_keyword_tweets function returns a dictionary with the correct keys.")


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



# Function to get and cache data from an API request to OMDb
# function name: get_movie_data

class get_movie_data_tests(unittest.TestCase):
	def test_return_content(self):
		moviedata = get_movie_data("Titanic")
		self.assertTrue(len(moviedata.keys()) > 0, "Testing that the API request returns content.")
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