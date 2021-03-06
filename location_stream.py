import tweepy
from time import sleep, localtime
import sqlite3
import os.path


consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

class StreamListener(tweepy.StreamListener):

	def on_status(self, status):
		time = localtime()
		# Create a database file beforehand.
		fpath = '{}-{}-{}-{}.db'.format(time.tm_year, time.tm_mon, time.tm_mday, time.tm_hour)
		if not os.path.isfile(fpath):
			conn = sqlite3.connect(fpath)
			x = conn.cursor()
			create_table = '''CREATE TABLE tweeter (id INT,user VARCHAR,text VARCHAR,created_at DATETIME, coordinates VARCHAR,geo VARCHAR,retweeted_count INT,favorite_count INT,place VARCHAR) '''
			x.execute(create_table)
			conn.commit()
			conn.close()
		
		conn = sqlite3.connect(fpath)
		x = conn.cursor()
		x.execute("""INSERT INTO tweeter (id,user,text,created_at,coordinates,geo,retweeted_count,favorite_count,place ) VALUES(?,?,?,?,?,?,?,?,?)""",
          (status.id,str(status.user),str(status.text),str(status.created_at),str(status.coordinates),str(status.geo),str(status.retweet_count), str(status.favorite_count),str(status.place)))
		conn.commit()
		conn.close()
	
	def on_error(self, status_code):
		if status_code == 420:
			return False


def main():
	stream_listener = StreamListener()
	stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
	stream.filter(locations=[28.4476,40.7418,29.4776,41.3776])


while True:
	try:
		main()
	except:
		sleep(15*60)