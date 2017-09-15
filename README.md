# TwitterFollowers
Twitter app to track followers

Private Twitter API tokens are currently stored locally in a file tokens.py

Uses Tweepy API to store follower data in sqlite3 database.

# TODO
* Set up Twitter sign-in 
  * https://dev.twitter.com/web/sign-in/implementing
* Build front-end
* Set up logging
* Deploy to Heroku
* Handle errors
* Optimization:
  * On future checks, compare follower # to DB followers to evaluate optimal algorithm?