# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 16:53:33 2017

@author: Sarai
"""

import time, datetime, sqlite3
import tweepy
#import tokens

# Pass tokens to Tweepy's OAuthHandler.
#auth = tweepy.OAuthHandler(tokens.consumer_key, tokens.consumer_secret)
#auth.set_access_token(tokens.access_token, tokens.access_token_secret)
#api = tweepy.API(auth)

# Until Twitter app authentication is configured, place username here.
#username = "saraislet"
#my_id = api.get_user(username).id
date = datetime.datetime.now()

# Connect to followers.db
db = sqlite3.connect('followers.db')
cursor = db.cursor()


# In this example, the handler is time.sleep(15 * 60),
# but you can of course handle it in any way you want.
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)


def check_username(userdata):
    """
    Checks database for username, returns boolean.
    """
    cursor.execute(
            '''SELECT id FROM followers WHERE follower_id = ?''', (userdata.id,))
    if cursor.fetchone() is None:
        return False
    else:
        return True


def store_user(userdata):
    """
    Store user data in the users table on the first login.
    """
    cursor.execute(
        '''INSERT INTO users(
            twitter_id, screen_name, 
            date_of_first_login, date_last_checked, number_of_followers)
        VALUES(?,?,?,?,?)''', 
        (userdata.id, userdata.screen_name, 
             date, date, userdata.followers_count))  
    db.commit()


def update_user(userdata):
    """
    On subsequent logins, update users table data.
    """
    cursor.execute(
        '''UPDATE users SET date_last_checked = ?, number_of_followers = ?
        WHERE id = ?''', 
        (date, userdata.followers_count, userdata.id))
    db.commit()
    
 
def get_followers(userdata):
    """
    Construct a set of follower IDs and a dictionary of follower names.
    """
    follower_ids = set()
    for follower in limit_handled(tweepy.Cursor(api.followers, userdata.id, count=100).items()):
        followers[follower.id] = follower.screen_name
        follower_ids.add(follower.id)
    return follower_ids


def get_follower_ids(userdata):
    """
    Construct a set of follower IDs.
    """
    follower_ids = set(api.followers_ids(userdata.id))
    return follower_ids


def update_follower_db(userdata, follower_ids, follower_names = None):
    """
    Iterate through rows in the database, checking the list for each.
    """
    unfollowers = set()
    newFollowers = set()
    
    cursor.execute(
            '''SELECT id, follower_id, following, screen_name 
            FROM followers WHERE twitter_id = ?''', (userdata.id,))
    rows = cursor.fetchall()
    
    for row in rows:
        # If there is a follower, update the date checked, and set following to 1.
        if row[1] in follower_ids:
            if row[2] == 0:
                cursor.execute(
                    '''UPDATE followers SET following = 1 WHERE id = ?''', 
                    (row[0],))
                db.commit()
            # Remove follower from set.
            # When this completes, only new followers will remain in the set.
            follower_ids.remove(row[1])
        # If this row is not in followers, but is listed in the db as a follower,
        # then this is an unfollower.
        elif row[2] == 1:
            cursor.execute(
                '''UPDATE followers SET date_unfollowed = ?, following = 0 
                WHERE id = ? ''', 
                (date, row[0]))
            db.commit()
            unfollowers.add(row[3])
    
    # Iterate through remaining followers in the set, and add them to the database.
    # OLD: [user.screen_name for user in api.lookup_users(user_ids = follower_ids)]
    # Above code may be efficient, but must use limit_handled to paginate lookups.
    for follower_id in follower_ids:
        if follower_id in followers:
            screen_name = followers[follower_id]
        else:
            screen_name = api.get_user(follower_id).screen_name
        cursor.execute(
            '''INSERT INTO followers(twitter_id, follower_id, screen_name, date_added, following)
            VALUES(?,?,?,?,1)''', 
            (userdata.id, follower_id, screen_name, date))  
        db.commit()
        newFollowers.add(screen_name)
    
    # Print out number and list of new followers and unfollows.
    if len(newFollowers) == 0:
        print("No new followers.")
    else:
        print("New followers (" + str(len(newFollowers)) + "): " + str(newFollowers))
    if len(unfollowers) == 0:
        print("No new unfollows.")
    else:
        print("Unfollows (" + str(len(unfollowers)) + "): " + str(unfollowers))
    print("You have " + str(userdata.followers_count) + " followers.")


def main(userdata, twitter_api):
    """
    New users must be stored in the database.
    Get_followers pulls all follower data for new users.
    """
    global api
    api = twitter_api
    global followers
    followers = {}
    
    if check_username(userdata) is True:
        update_user(userdata)
        follower_list = get_follower_ids(userdata)
        update_follower_db(userdata, follower_list)
    else:
        store_user(userdata)
        follower_list = get_followers(userdata)
        update_follower_db(userdata, follower_list)

# Close the db connection.
db.close()

# TODO: Log to file instead of printing to console.

print("Done.")