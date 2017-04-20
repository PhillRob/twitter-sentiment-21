#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import json
import logging
import re
# import request

import tweepy
import yaml
import flask
from flask import request
from textblob import TextBlob
from tweepy import OAuthHandler
from two1.wallet.two1_wallet import Wallet
from two1.bitserv.flask import Payment

app = flask.Flask(__name__)
payment = Payment(app, Wallet())

# app = Flask(__name__)

# setup wallet
wallet = Wallet()

# hide logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/manifest')
def manifest():
    """Provide the app manifest to the 21 crawler.
    """
    with open('./manifest.yaml', 'r') as f:
        manifest = yaml.load(f)
    return json.dumps(manifest)


class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = ''
        consumer_secret = ''
        access_token = ''
        access_token_secret = ''

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


@app.route('/', methods=['GET', 'POST'])
@payment.required(6000)
def main():
    # creating object of TwitterClient Class
    api = TwitterClient()

    # get args
    sst = request.args.get('sst','bitcoin', type=str)
    cct = request.args.get('cct', 212, type=int)

    # calling function to get tweets
    try:
        tweets = api.get_tweets(query=sst, count=cct)
    except (IOError, ValueError):
        return ("Search string empty or tweet count is not a number or no tweets found for {}", sst)

    # total tweets
    tt = ("Total Number of tweets {}:".format(len(tweets)))

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    ptp = ("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))

    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    ntp = ("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))

    # percentage of neutral tweets
    netp=("Neutral tweets percentage: {} %".format(100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)))

    # printing first 5 positive tweets
    print ("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print (tweet['text'])
    try:
        return '{}\n{}\n{}\n{}\n\nPositive tweets \n{}\n{}\n{}\n{}\n{}\n\n\nNegative tweets \n{}\n{}\n{}\n{}\n{}'.format(tt, ptp, netp, ntp, ptweets[1]['text'],ptweets[2]['text'],ptweets[3]['text'],ptweets[4]['text'],ptweets[5]['text'],ntweets[1]['text'],ntweets[2]['text'],ntweets[3]['text'],ntweets[4]['text'],ntweets[5]['text'])
    except IndexError:
        try:
            return '{}\n{}\n{}\n{}\n\nPositive tweets \n{}\n{}\n{}\n\n\nNegative tweets \n{}\n{}\n{}'.format(tt, ptp, netp, ntp, ptweets[1]['text'], ptweets[2]['text'], ptweets[3]['text'], ntweets[1]['text'], ntweets[2]['text'], ntweets[3]['text'])
        except IndexError:
            try:
                return '{}\n{}\n{}\n{}\n\nPositive tweets \n{}\n\n\nNegative tweets \n{}'.format(tt, ptp, netp, ntp, ptweets[1]['text'], ntweets[1]['text'])
            except IndexError:
                return '{}\n{}\n{}\n{}\n\n'.format(tt, ptp, netp, ntp)

if __name__ == "__main__":
    print("Server running...")
    app.run(host='::', port=6033, debug=True)
