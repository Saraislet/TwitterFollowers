# TwitterFollowers
Twitter app to track followers

Private Twitter API tokens are currently stored locally in a file tokens.py

Uses Tweepy API to store follower data in sqlite3 database.

# TODO
* Break code into basic, maintainable, single-purpose functions.
* Set up logging
* Handle errors
* Build users table
  * On first check, pull full followers JSON.
  * On future checks, compare follower # to DB followers to evaluate optimal algorithm?
* Set up Twitter OAuth 
  * https://dev.twitter.com/web/sign-in/implementing
* Deploy to Heroku
* Build front-end
