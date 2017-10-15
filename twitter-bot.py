import tweepy
import yweather
import simplejson as json

from config import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

print("Connected to twitter......")

def getWoeidOfLocation(location):
    client = yweather.Client()
    return client.fetch_woeid(location)

#Get last tweet from specified username
def getLastTweetFromUser( username="monicbhanushali" , nTweets=1, retweets = False):
        last_tweet = json.loads(getTweetsFromUser(username, 1, True))
        result = last_tweet['tweets'][0]['text']
        #print("Last tweet from " + username + ": " + last_tweet[0] )
        return json.dumps(result);

#Get tweets from given username
def getTweetsFromUser(username="monicbhanushali", nTweets=10, retweets=False):
    all_tweets = api.user_timeline(screen_name = username, count = nTweets, include_rts = retweets)
    result = []
    json_response = []
    for tweet in all_tweets:
        result.append(tweet.text)
        tweet_url = "https://twitter.com/"+username+"/status/"+tweet.id_str
        json_response.append({"text":tweet.text,"url":tweet_url})
    #print(json.dumps({"tweets":json_response}))
    return json.dumps({"tweets":json_response})

json_msg = getTweetsFromUser("monicbhanushali")
print(json_msg)

