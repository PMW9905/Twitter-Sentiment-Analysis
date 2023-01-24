import tweepy
import configparser
import threading
from TweetHandler import TWTHandler

#Thread for handling tweets every 30 seconds
class thread(threading.Thread):
        def __init__(self, handler):
            threading.Thread.__init__(self)
            self.handler = handler
        def run(self):
            handle_tweets(self.handler)

#function for handling tweets
def handle_tweets(handler):
    handler.handleTweets()

#function for serializing tweets
def tweet_serializer(tweet):
    return tweet.encode("utf-8")

#read config into local vars
print("Reading config...")
config = configparser.ConfigParser()
config.read('config.ini')
print("Copying over tkns...")
api_key = config['keys']['api']
api_key_secret = config['keys']['api_secret']
access_tkn = config['keys']['access']
access_tkn_secret = config['keys']['access_secret']

#prompting user for hashtag to scrape
hashtag = input("Please provide a hashtag: ")
keywords = [hashtag]

#creating thread & tweethandle object
tweet_handler = TWTHandler()
tweet_handler_thread = thread(tweet_handler)
tweet_handler_thread.start()

#Handling the stream of tweets
class Listener(tweepy.Stream):
    def on_status(self, status):
        print("New tweet added from user " + status.user.screen_name)
        tweet_handler.pushNewTweet(status.text)

print("Connecting tweepy stream to twitter...")
stream_tweet = Listener(api_key,api_key_secret,
    access_tkn,access_tkn_secret)

print("Opening stream...")
stream_tweet.filter(track=keywords)