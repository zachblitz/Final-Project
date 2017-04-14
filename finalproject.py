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

############################################# omdb #######################################

omdb_cached_data = 'omdb_cache.json'

try:
	omdb_cache_file = open(omdb_cached_data)
	omdb_cache_contents = omdb_cache_file.read()
	omdb_cache_diction = json.loads(omdb_cache_contents)
	omdb_cache_file.close()

except:
	omdb_cache_diction = {}

movie_titles = [] #list of movie titles

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

movies = [] #list of movie dictionaries

first_movie = get_and_cache_omdb_data(movie_titles[0])
second_movie = get_and_cache_omdb_data(movie_titles[1])
third_movie = get_and_cache_omdb_data(movie_titles[2])

movies.append(first_movie)
movies.append(second_movie)
movies.append(third_movie)

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
		return self.omdb_data['Actors']

	def get_id(self):
		return self.omdb_data['imdbID']

	def get_rating(self):
		return self.omdb_data['imdbRating']

movie_instances = [] #list of movie instances

movie_1 = Movie(movies[0])
movie_2 = Movie(movies[1])
movie_3 = Movie(movies[2])

movie_instances.append(movie_1)
movie_instances.append(movie_2)
movie_instances.append(movie_3)

movie_1_tuple = (movie_1.get_id(), movie_1.title, movie_1.director, movie_1.get_plot(), movie_1.get_year(), movie_1.get_actors(), movie_1.get_rating())
movie_2_tuple = (movie_2.get_id(), movie_2.title, movie_2.director, movie_2.get_plot(), movie_2.get_year(), movie_2.get_actors(), movie_2.get_rating())
movie_3_tuple = (movie_3.get_id(), movie_3.title, movie_3.director, movie_3.get_plot(), movie_3.get_year(), movie_3.get_actors(), movie_3.get_rating())

movie_tuples = [movie_1_tuple, movie_2_tuple, movie_3_tuple]

######################################## now twitter ########################### 

twitter_cache_data = 'twitter_cache.json'

try:
	twitter_cache_file = open(twitter_cache_data, 'r')
	twitter_cache_contents = twitter_cache_file.read()
	twitter_cache_diction = json.loads(twitter_cache_contents)

except:
	twitter_cache_diction = {}

twitter_search_1 = movie_1.title
twitter_search_2 = movie_2.title
twitter_search_3 = movie_3.title

def get_and_cache_twitter_data(search):
	if search in twitter_cache_diction:
		results = twitter_cache_diction[search]
	else:
		results = api.search(q = search)
		twitter_cache_diction[search] = results
		twitter_cache_file = open(twitter_cache_data, 'w')
		twitter_cache_file.write(json.dumps(twitter_cache_diction))
		twitter_cache_file.close()

	return results['statuses']

twitter_results_1 = get_and_cache_twitter_data(twitter_search_1)
twitter_results_2 = get_and_cache_twitter_data(twitter_search_2)
twitter_results_3 = get_and_cache_twitter_data(twitter_search_3)

movie_tweets_data = []

for tweet in twitter_results_1:
	text = tweet['text']
	tweet_id = tweet['id_str']
	user_id = tweet['user']['id_str']
	favorites = tweet['favorite_count']
	retweets = tweet['retweet_count']

	tweet_tuple = (text, tweet_id, user_id, movie_1.get_id(), favorites, retweets)
	movie_tweets_data.append(tweet_tuple)

for tweet in twitter_results_2:
	text = tweet['text']
	tweet_id = tweet['id_str']
	user_id = tweet['user']['id_str']
	favorites = tweet['favorite_count']
	retweets = tweet['retweet_count']

	tweet_tuple = (text, tweet_id, user_id, movie_2.get_id(), favorites, retweets)
	movie_tweets_data.append(tweet_tuple)

for tweet in twitter_results_3:
	text = tweet['text']
	tweet_id = tweet['id_str']
	user_id = tweet['user']['id_str']
	favorites = tweet['favorite_count']
	retweets = tweet['retweet_count']

	tweet_tuple = (text, tweet_id, user_id, movie_3.get_id(), favorites, retweets)
	movie_tweets_data.append(tweet_tuple)

####################################### users#################################

def unique(x,y):
	for tuples in y:
		if x[0] == tuples[0]:
			return False
	return True


twitter_data_users = 'user_cache.json'

try:
	user_cache_file = open(twitter_data_users, 'r')
	user_cache_contents = user_cache_file.read()
	user_cache_diction = json.loads(user_cache_contents)

except:
	user_cache_diction = {}


twitter_user_data = []

for tweet in twitter_results_1: #getting info on user who tweeted it
	user_id = tweet['user']['id_str']
	screen_name = tweet['user']['screen_name']
	favorites = tweet['user']['favourites_count']
	followers = tweet['user']['followers_count']
	tweets = tweet['user']['statuses_count']
	following = tweet['user']['friends_count']
	location = tweet['user']['location']

	user_tuple = (user_id, screen_name, favorites, movie_1.get_id(), followers, tweets, following, location)
	if unique(user_tuple, twitter_user_data) == True:
			twitter_user_data.append(user_tuple)

for tweet in twitter_results_1: #getting info on user's mentioned in tweets
	mentions = tweet["entities"]["user_mentions"]
	for name in mentions:
		user = api.get_user(name["screen_name"])



		if name["screen_name"] not in user_cache_diction:
			user_cache_diction[name["screen_name"]] = user
			user_cache_file = open(twitter_data_users, 'w')
			user_cache_file.write(json.dumps(user_cache_diction))
			user_cache_file.close()

		user_id = user['id_str']
		screen_name = user['screen_name']
		favorites = user['favourites_count']
		followers = user['followers_count']
		tweets = user['statuses_count']
		following = user['friends_count']
		location = user['location']

		user_tuple = (user_id, screen_name, favorites, movie_1.get_id(), followers, tweets, following, location)
		if unique(user_tuple, twitter_user_data) == True:
			twitter_user_data.append(user_tuple)

for tweet in twitter_results_2: #getting info on user who tweeted it
	user_id = tweet['user']['id_str']
	screen_name = tweet['user']['screen_name']
	favorites = tweet['user']['favourites_count']
	followers = tweet['user']['followers_count']
	tweets = tweet['user']['statuses_count']
	following = tweet['user']['friends_count']
	location = tweet['user']['location']

	user_tuple = (user_id, screen_name, favorites, movie_2.get_id(), followers, tweets, following, location)
	if unique(user_tuple, twitter_user_data) == True:
			twitter_user_data.append(user_tuple)

for tweet in twitter_results_2: #getting info on user's mentioned in tweets
	mentions = tweet["entities"]["user_mentions"]
	for name in mentions:
		user = api.get_user(name["screen_name"])

		if name["screen_name"] not in user_cache_diction:
			user_cache_diction[name["screen_name"]] = user
			user_cache_file = open(twitter_data_users, 'w')
			user_cache_file.write(json.dumps(user_cache_diction))
			user_cache_file.close()

		user_id = user['id_str']
		screen_name = user['screen_name']
		favorites = user['favourites_count']
		followers = user['followers_count']
		tweets = user['statuses_count']
		following = user['friends_count']
		location = user['location']

		user_tuple = (user_id, screen_name, favorites, movie_2.get_id(), followers, tweets, following, location)
		if unique(user_tuple, twitter_user_data) == True:
			twitter_user_data.append(user_tuple)

for tweet in twitter_results_3: #getting info on user who tweeted it
	user_id = tweet['user']['id_str']
	screen_name = tweet['user']['screen_name']
	favorites = tweet['user']['favourites_count']
	followers = tweet['user']['followers_count']
	tweets = tweet['user']['statuses_count']
	following = tweet['user']['friends_count']
	location = tweet['user']['location']

	user_tuple = (user_id, screen_name, favorites, movie_3.get_id(), followers, tweets, following, location)
	if unique(user_tuple, twitter_user_data) == True:
		twitter_user_data.append(user_tuple)

for tweet in twitter_results_3: #getting info on user's mentioned in tweets
	mentions = tweet["entities"]["user_mentions"]
	for name in mentions:
		user = api.get_user(name["screen_name"])

		if name["screen_name"] not in user_cache_diction:
			user_cache_diction[name["screen_name"]] = user
			user_cache_file = open(twitter_data_users, 'w')
			user_cache_file.write(json.dumps(user_cache_diction))
			user_cache_file.close()

		user_id = user['id_str']
		screen_name = user['screen_name']
		favorites = user['favourites_count']
		followers = user['followers_count']
		tweets = user['statuses_count']
		following = user['friends_count']
		location = user['location']

		user_tuple = (user_id, screen_name, favorites, movie_3.get_id(), followers, tweets, following, location)
		if unique(user_tuple, twitter_user_data) == True:
			twitter_user_data.append(user_tuple)
		


# #pprint(movie_tuples)
# #pprint(movie_tweets_data)
# print(twitter_user_data)


#################################### sql ######################################################

conn = sqlite3.connect('final_project_omdb_twitter.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Movies')
cur.execute('DROP TABLE IF EXISTS Tweets')
cur.execute('DROP TABLE IF EXISTS Users')

table_spec = 'CREATE TABLE IF NOT EXISTS Movies(Movie_ID TEXT PRIMARY KEY, Title TEXT, Director TEXT, Plot TEXT, Year TEXT, Actors TEXT, Rating TEXT)'
cur.execute(table_spec)
conn.commit()

statement = 'INSERT INTO Movies VALUES (?,?,?,?,?,?,?)' 
for movie in movie_tuples:
	cur.execute(statement, movie)
conn.commit()

table_spec = 'CREATE TABLE IF NOT EXISTS Tweets(Message TEXT, Tweet_ID TEXT PRIMARY KEY, User_ID TEXT, Movie_ID TEXT, Favorites INTEGER, Retweets INTEGER)'
cur.execute(table_spec)
conn.commit()

statement2 = 'INSERT INTO Tweets VALUES (?,?,?,?,?,?)'
for tweet in movie_tweets_data:
	cur.execute(statement2, tweet)
conn.commit()

table_spec = 'CREATE TABLE IF NOT EXISTS Users(User_ID TEXT PRIMARY KEY, Screen_Name TEXT, Favorites INTEGER, Movie_ID TEXT, Followers INTEGER, Tweets INTEGER, Following INTEGER, Location TEXT)'
cur.execute(table_spec)
conn.commit()

statement3 = 'INSERT INTO Users VALUES (?,?,?,?,?,?,?,?)'
for user in twitter_user_data:
	cur.execute(statement3, user)
conn.commit()



################################## data processing techniques ###########################


##################################### test cases ########################################

class TestCases(unittest.TestCase):
	def test_omdb_caching(self):
		self.assertEqual(type(omdb_cache_diction), type({})) #tests if caching is type dictionary
	def test_twitter_caching(self):
		self.assertEqual(type(twitter_cache_diction), type({})) #tests if caching is type dictionary
	def test_movie_titles(self):
		self.assertEqual(len(movie_titles), 3) #tests if there are 3 movie titles
	def test_get_omdb_data(self):
		self.assertEqual(type(first_movie), type({})) #test if the first_movie results is a dictionary
	def test_get_omdb_data_2(self):
		self.assertEqual(len(first_movie.keys()), 25) #tests if the first movie dictionary has 25 keys 
	def test_class_1(self):
		self.assertEqual(type(movie_1.get_plot()), type("")) #tests if the year is a type string
	def test_class_2(self):
		self.assertEqual(type(movie_1.get_id()), type("")) #tests if the id of the movie is a type string
	def test_class_3(self):
		self.assertEqual(type(movie_1.get_rating()), type("")) #tests if the type of the movie rating is type string
	def test_class_4(self):
		self.assertEqual(type(movie_1.get_actors()), type("")) #tests if the type of the actors in the movie is type string
	def test_class_5(self):
		self.assertEqual(type(movie_1.get_year()), type("")) #tests if the type of the year in the movie is type string
	def test_class_6(self): # tests the plot of shrek
		shrek_data = get_and_cache_omdb_data("Shrek")
		shrek = Movie(shrek_data)
		self.assertEqual(shrek.get_plot(), "After his swamp is filled with magical creatures, Shrek agrees to rescue Princess Fiona for a villainous lord in order to get his land back.")
	def test_class_7(self): #tests the id of shrek
		shrek_data = get_and_cache_omdb_data("Shrek")
		shrek = Movie(shrek_data)
		self.assertEqual(shrek.get_id(), "tt0126029")
	def test_class_8(self): #tests the rating of shrek
		shrek_data = get_and_cache_omdb_data("Shrek")
		shrek = Movie(shrek_data)
		self.assertEqual(shrek.get_rating(), "7.9")
	def test_class_9(self): #tests the actors of shrek
		shrek_data = get_and_cache_omdb_data("Shrek")
		shrek = Movie(shrek_data)
		self.assertEqual(shrek.get_actors(), "Mike Myers, Eddie Murphy, Cameron Diaz, John Lithgow")
	def test_class_10(self): #tests the year of shrek
		shrek_data = get_and_cache_omdb_data("Shrek")
		shrek = Movie(shrek_data)
		self.assertEqual(shrek.get_year(), "2001")
	def test_get_twitter_data_1(self):
		self.assertEqual(type(twitter_results_1), type([])) #tests if twitter_results_1 is a type list
	def test_get_twitter_data_2(self):
		self.assertEqual(type(twitter_results_1[0]), type({})) #tests if the first result in twitter_results_1 is a dictionary
	def test_unique_1(self): #testing if the function returns false when the first element of a tuple is not in any of the first elements of tuples existing in a list
		x = ('hi', 3)
		y = [('hi', True, 2), ('bye', 'yellow', 100)]
		test = unique(x,y)
		self.assertEqual(test, False)
	def test_unique_2(self):
		x = (45,'turtle') #testing if the function returns true when the first element of a tuple is any of the first elements of tuples existing in a list
		y = [(46, 23, False), (85, 'taco')]
		test = unique(x,y)
		self.assertEqual(test, True)


if __name__ == "__main__":
	unittest.main(verbosity =2)




	


















