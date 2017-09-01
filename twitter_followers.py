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
followers = set()

# In this example, the handler is time.sleep(15 * 60),
# but you can of course handle it in any way you want.

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)

# Construct a set of followers.
followers = set(api.followers_ids(user))

# Connect to followers.db
db = sqlite3.connect('followers.db')
cursor = db.cursor()

# Iterate through rows in the database, checking the list for each.
cursor.execute('''SELECT id, follower_id, following, screen_name FROM followers WHERE twitter_id = ?''', (my_id,))
rows = cursor.fetchall()

for row in rows:
    # If there is a follower, update the date checked, and set following to 1.
    if row[1] in followers:
        if row[2] == 0:
            cursor.execute('''UPDATE followers SET following = 1 WHERE id = ?''', (row[0],))
            print("Updated: " + str(row[3]))
            db.commit()
        # Remove follower from set. When this completes, only new followers will remain in the set.
        followers.remove(row[1])
    # If this row is not in the followers, but is listed in the database as a follower, this is an unfollower.
    elif row[2] == 1:
        cursor.execute('''UPDATE followers SET date_unfollowed = ?, following = 0 WHERE id = ? ''', (date, row[0]))
        print("Unfollower: " + row[3])
        db.commit()

# Iterate through remaining followers in the set, and add them to the database.
for follower in followers:
    screen_name = api.get_user(follower).screen_name
    cursor.execute('''INSERT INTO followers(twitter_id, follower_id, screen_name, date_added, following)
                  VALUES(?,?,?,?,1)''', (my_id, follower, screen_name, date))  
    print("Inserted: " + str(follower) + ", " + screen_name + ", " + str(date))
    db.commit()


# Commit the above changes to the db, and close the db connection.
db.close()

# TODO: Log to file instead of printing to console.

print("Done.")