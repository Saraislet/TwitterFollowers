# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 13:01:01 2017

@author: Sarai
"""

#from flask import Flask
from flask import Flask, request
import flask
import tweepy
import tokens


app = Flask(__name__)


@app.route('/')
def index():
	return "Hi, Sarai! You look good today."


if __name__ == "__main__":
	app.run()