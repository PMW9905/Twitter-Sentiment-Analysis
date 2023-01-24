import tweepy
import configparser
from kafka import KafkaProducer

def tweet_serializer(tweet):
    return tweet.encode("utf-8")

print("Reading config...")
config = configparser.ConfigParser()
config.read('config.ini')

print("Copying over tkns...")
api_key = config['keys']['api']
api_key_secret = config['keys']['api_secret']
access_tkn = config['keys']['access']
access_tkn_secret = config['keys']['access_secret']

print("Copying over zookeeper/kafka info")
kafka_addr = config['kafka']['addr']

hashtag = input("Please provide a hashtag: ")
keywords = [hashtag]

#Handling the stream of tweets
class Listener(tweepy.Stream):
    def on_status(self, status):
        print("Sending tweet to producer:")
        producer.send("tweets", status.text)
        print(status.text)
        

print("Connecting to Kafka server via producer...")
producer = KafkaProducer(bootstrap_servers=[kafka_addr], value_serializer=tweet_serializer)

print("Connecting tweepy stream to twitter...")
stream_tweet = Listener(api_key,api_key_secret,
    access_tkn,access_tkn_secret)

print("Opening stream...")
stream_tweet.filter(track=keywords)



