# Zachary Blitz's Final Project for SI 206
# Option 2
import unittest
import requests
import tweepy
import twitter_info
import json
import sqlite3
from pprint import pprint
import itertools
import collections

consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

omdb_cached_data = 'omdb_cache.json'

try:
	omdb_cache_file = open(omdb_cached_data)
	omdb_cache_contents = omdb_cache_file.read()
	omdb_cache_diction = json.loads(omdb_cache_contents)
	omdb_cache_file.close()

except:
	omdb_cache_diction = {}

movie_titles = []

movie_title_1 = input("Please enter in your favorite movie: ")
movie_title_2 = input("Please enter in your second favorite movie: ")
movie_title_3 = input("Please enter in your third favorite movie: ")

movie_titles.append(movie_title_1)
movie_titles.append(movie_title_2)
movie_titles.append(movie_title_3)


def get_and_cache_omdb_data(movie_title):
	movie_data = requests.get('http://www.omdbapi.com?', params = {'t': movie_title})
	
	if movie_title in omdb_cache_diction:
		omdb_response_text = omdb_cache_diction[movie_title]
	else:
		omdb_cache_diction[movie_title] = movie_data.text
		omdb_response_text = movie_data.text

		omdb_cache_file = open(omdb_cached_data, 'w')
		omdb_cache_file.write(json.dumps(omdb_cache_diction))
		omdb_cache_file.close()

	return(json.loads(omdb_response_text))


first_movie = get_and_cache_omdb_data(movie_titles[0])
second_movie = get_and_cache_omdb_data(movie_titles[1])
third_movie = get_and_cache_omdb_data(movie_titles[2])

class Movie:
	def __init__(self,omdb_data):
		self.omdb_data = omdb_data
		self.title = self.omdb_data['Title']
		self.director = self.omdb_data['Director']

	def get_plot(self):
		return self.omdb_data['Plot']

	def get_year(self):
		return self.omdb_data['Year']

	def get_actors(self):
		return self.omdb_data['Actors'].split(",")

	def get_id(self):
		return self.omdb_data['imdbID']

	def get_rating(self):
		return self.omdb_data['imdbRating']

movie_instances = []

movie_1 = Movie(first_movie)
movie_2 = Movie(second_movie)
movie_3 = Movie(third_movie)

movie_instances.append(movie_1)
movie_instances.append(movie_2)
movie_instances.append(movie_3)

	


















