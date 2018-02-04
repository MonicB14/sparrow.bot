import tweepy
import yweather
import simplejson as json

from flask import Flask
from config import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

app = Flask(__name__)

def getWoeidOfLocation(location):
    client = yweather.Client()
    return client.fetch_woeid(location)

@app.route('/')
def sayHello():
        return "Hi There";
	
#Get last tweet from specified username
@app.route('/getlasttweet', defaults={'username':'monicbhanushali'})
@app.route('/getlasttweet/<username>')
def getLastTweetFromUser( username="monicbhanushali" , nTweets=1, retweets = False):
        last_tweet = json.loads(getTweetsFromUser(username, 1, True))
        result = last_tweet['tweets'][0]
        return json.dumps(result);

#Get tweets from given username
@app.route('/gettweets')
def getTweetsFromUser(username="monicbhanushali", nTweets=10, retweets=False):
    all_tweets = api.user_timeline(screen_name = username, count = nTweets, include_rts = retweets)
    result = []
    json_response = []
    for tweet in all_tweets:
        result.append(tweet.text)
        tweet_url = "https://twitter.com/"+username+"/status/"+tweet.id_str
        json_response.append({"text":tweet.text,"url":tweet_url})
    return json.dumps({"tweets":json_response})

#Get trends of a particular location
@app.route('/getlocationtrends', defaults={'location':'world'})
@app.route('/getlocationtrends/<location>')
def getLocationTrends(location="world", nTrend=10):
    response=0
    woeid = 1
    json_response = []
    if( location == "world"):
        response = api.trends_place(woeid)
    else:
        response =  api.trends_place(getWoeidOfLocation(location))
    data = response[0]
    trends = data['trends']
    trends = trends[0:10]
    for trend in trends:
        json_response.append({"name":trend['name'],"url":trend['url']})
    trending_topics = [trend['name'] for trend in trends]
    print(json_response)
    return json.dumps({"trends":json_response})

if __name__ == '__main__':
   app.run(port=8080)


