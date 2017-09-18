# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 20:12:44 2017

@author: Sarai
"""

import os
from flask import Flask, request, render_template
import flask
import tweepy
#from tweepy.auth import OAuthHandler
#import twitter_followers as tf

app = Flask(__name__)
app.config.from_pyfile('config.cfg', silent=True)

consumer_key = os.environ['consumer_key']
consumer_secret = os.environ['consumer_secret']
#OAUTH_TOKEN = os.environ['TWITTER_OAUTH_TOKEN']
#OAUTH_TOKEN_SECRET = os.environ['TWITTER_OAUTH_TOKEN_SECRET']


callback_url = 'https://powerful-temple-76731.herokuapp.com/verify'
#callback_url = 'oob'
session = dict()
db = dict()


@app.route('/')
def send_token():
    redirect_url = ""
#    auth = tweepy.OAuthHandler("FdzGyeOjfYlhwq7FdaEkZP9PH", "J0Ldb1LpZZnwY7wlmbG2VES0fNHiKZCgUBmYIv6w70EdaJcB8T", callback_url)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)

#    redirect_url= auth.get_authorization_url()

    try: 
        #get the request tokens
        redirect_url= auth.get_authorization_url()
        session['request_token']= (auth.request_token['oauth_token'],
            auth.request_token['oauth_token_secret'])
#        session.set('request_token', auth.request_token)
    except tweepy.TweepError:
        print('Error! Failed to get request token')

    #this is twitter's url for authentication
#    return flask.redirect(redirect_url)
    return render_template('start.html', redirect_url = redirect_url)



@app.route("/verify")
def get_verification():

    #get the verifier key from the request url
    verifier = request.args['oauth_verifier']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    print("session dict object is: " + str(session))
    token = session['request_token']
    del session['request_token']

#    auth.request_token = token
    auth.set_request_token(token[0], token[1])
    auth.get_access_token(verifier)

#    try:
#            auth.get_access_token(verifier)
#    except tweepy.TweepError:
#            print('Error! Failed to get access token.')

    #now you have access!
    api = tweepy.API(auth)

    #store in a db
    db['api']=api
    db['access_token_key']=auth.access_token.key
    db['access_token_secret']=auth.access_token.secret
    return flask.redirect(flask.url_for('start'))


@app.route("/start")
def start():
    #auth done, app logic can begin
    api = db['api']
    userdata = api.me()
#    tf.main(userdata, api)

    #example, print your latest status posts
    return flask.render_template('followers.html', 
                                 name = userdata.name, 
                                 screen_name = userdata.screen_name, 
                                 bg_color = userdata.profile_background_color, 
                                 followers_count = userdata.followers_count, 
                                 created_at = userdata.created_at)


if __name__ == '__main__':
    app.run()