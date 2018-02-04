import requests
import telebot
import simplejson as json
from flask import Flask

app = Flask(__name__)

from app_constants import *
  
bot = telebot.TeleBot('YOUR TELEGRAM BOT KEY')

list_of_commands = ""
for command in commands:
    list_of_commands = list_of_commands + command + "\n"

@bot.message_handler(commands=['start', 'help'], regexp="")
def send_welcome(message):
    print(message.text)
    bot.reply_to(message, welcome_msg+list_of_commands)

@bot.message_handler(commands=['lasttweet'])
def getLastTweet(message):
    msg_data = message.text.split()
    if(len(msg_data)==1):
        url_string = tweet_restpoint+"getlasttweet/monicbhanushali"
    else:
        url_string = tweet_restpoint+"getlasttweet/" + msg_data[1]
    json_response = requests.get(url_string)

    if(json_response.status_code != 200):
        bot.reply_to(message,"Sorry :( \nI didnt find any appropriate match")
    else:
        response = json.loads(json_response.text)
        print(json_response.json())
        bot.reply_to(message,response['url']) 
    


@bot.message_handler(commands=['locationtrend'])
def getLastTweet(message):
    msg_data = message.text.split()
    if(len(msg_data)==1):
        url_string = tweet_restpoint+"getlocationtrends/world"
    else:
        url_string = tweet_restpoint+"getlocationtrends/" + msg_data[1]
    json_response = requests.get(url_string)

    if(json_response.status_code != 200):
        bot.reply_to(message,"Sorry :( \nI didnt find any appropriate match")
    else:
        response = json.loads(json_response.text)
        trends = response['trends']
        reply_msg = ""

        for trend in trends:
            reply_msg = reply_msg + "<a href=\"" + trend['url'] + "\">" + trend['name'] + "</a> \n"
    
        bot.send_message(message.chat.id, reply_msg, parse_mode="HTML")

@bot.message_handler(func=lambda message:True)
def default_handler(message):
    bot.reply_to(message, welcome_msg+list_of_commands)
    
bot.set_webhook()
bot.polling()