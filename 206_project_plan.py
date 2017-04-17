## Your name: Haley Yaremych
## The option you've chosen: Option 2

# Put import statements you expect to need here!

import unittest
import requests
import tweepy
import twitter_info # necessary keys for making twitter API requests
import json
import sqlite3
import re


# Cache file name: final_project_cache.json
# List of movie dictionaries: movie_dicts

# Write your test cases here.

# Function to get and cache Twitter data based on a search term
# function name: get_keyword_tweets

class get_keyword_tweets_tests(unittest.TestCase):
	def test_return_type(self):
		result = get_keyword_tweets("mountain bikes")
		self.assertEqual(type(result), type({}), "Testing that the get_keyword_tweets function returns a dictionary.")
	def test_caching(self):
		result = get_keyword_tweets("mountain bikes")
		self.assertEqual(sorted(result.keys()), ['search_metadata', 'statuses'], "Testing that the get_keyword_tweets function returns a dictionary with the correct keys.")


# Function to get and cache Twitter data based on a username
# function name: get_twitter_user

class get_twitter_user_tests(unittest.TestCase):
	def test_return_type(self):
		userinfo = get_twitter_user("UmichAthletics")
		self.assertEqual(type(userinfo), type({}), "Testing that the get_twitter_user function returns a dictionary.")
	def test_return_type_2(self):
		userinfo = get_twitter_user("UmichAthletics")
		self.assertEqual(type(userinfo.keys()[0]), type("str"), "Testing that the keys of the return dictionary are strings.")
	def test_caching(self):
		userinfo = get_twitter_user("UmichAthletics")
		cachefile = open("final_project_cache.json", "r")
		cachefile_str = cachefile.read()
		self.assertTrue("UmichAthletics" in cachefile_str, "Testing that the cache file contains a unique identifier from each query.")



# Function to get and cache data from an API request to OMDb
# function name: get_movie_data

class get_movie_data_tests(unittest.TestCase):
	def test_return_content(self):
		moviedata = get_movie_data("Titanic")
		self.assertTrue(len(moviedata.keys()) > 0, "Testing that the API request returns content.")
	def test_return_content_2(self):
		moviedata = get_movie_data("Titanic")
		self.assertTrue("Writer" in moviedata.keys(), "Testing that the correct information is retrieved from the API request.")




# List of dicionaries, each containing movie info from an API request

class movie_dicts_tests(unittest.TestCase):
	def test_element_type(self):
		self.assertEqual(type(movie_dicts[1]), type({}), "Testing that the elements of movie_dicts are dictionaries.")
	def test_dict_keys(self):
		self.assertTrue("title" in movie_dicts[0].keys(), "Testing that the correct information is in the movie dictionaries.")



## Remember to invoke all your tests...

unittest.main(verbosity=2)