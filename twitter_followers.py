# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 16:53:33 2017

@author: Sarai
"""

import tweepy, time, datetime, sqlite3
import tokens

auth = tweepy.OAuthHandler(tokens.consumer_key, tokens.consumer_secret)
auth.set_access_token(tokens.access_token, tokens.access_token_secret)

api = tweepy.API(auth)

date = datetime.datetime.now()
user = "techieslikeus"
my_id = api.get_user(user).id
followers = []

# In this example, the handler is time.sleep(15 * 60),
# but you can of course handle it in any way you want.

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)

# OLD: Constructs a list of followers.
#for follower in limit_handled(tweepy.Cursor(api.followers).items()):
#    followers.append(follower)



for follower in limit_handled(tweepy.Cursor(api.followers, user, count=100).items()):
    followers.append(follower)

# Connect to followers.db
db = sqlite3.connect('followers.db')
cursor = db.cursor()

# Build a list of followers from db.
#followers = []
#db.execute('''SELECT id, follower_id FROM followers WHERE twitter_id = my_id''')
#for row in db:
#    followers.append(row)


# Iterate through followers.
userList = []
for user in followers:
    try:
        # Try to update the follower for my_id matching user.id
        cursor.execute('''UPDATE followers SET date_checked = ? WHERE twitter_id = ? AND follower_id = ?''', (date, my_id, user.id))
        print("Updated: " + str(my_id) + ", " + str(user.id) + ", " + user.screen_name + ", " + str(date))
        db.commit()
    except Exception as e:
        # If that user.id does not exist, create a new row in followers.
        cursor.execute('''INSERT INTO followers(twitter_id, follower_id, screen_name, date_added)
                  VALUES(?,?,?,?)''', (my_id, user.id, user.screen_name, date))  
        print("Inserted " + str(my_id) + ", " + str(user.id) + ", " + user.screen_name + ", " + str(date))
        db.commit()

# Check for followers in the db with null date_unfollowed not listed in the retrieved followers.
# These are unfollowers.
cursor.execute('''SELECT id, follower_id, screen_name FROM followers WHERE twitter_id = ? AND follower_id = ? AND date_unfollowed IS NULL''', (my_id, user.id))
rows = cursor.fetchall()
for row in rows:
    cursor.execute('''UPDATE followers SET date_unfollowed = ? WHERE id = ? ''', (date, row[0]))
    print("Unfollower: " + row[2])

# Commit the above changes to the db, and close the db connection.
db.commit()
db.close()

# Quick function to grab a list of IDs.
# followers = tweepy.API.followers_ids("saraislet")

# Print followers to file followers.txt, 
# encoding the list as a string with utf-8 characters

# fh = open('followers.txt', 'w')
# fh.write(str(str(followers).encode('utf-8')))
# fh.close()


#print(followers)
#print(userList)
print("Done.")