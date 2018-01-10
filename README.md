# TwitterFollowers
Twitter app to track followers

Private Twitter API tokens are currently stored locally in a file tokens.py

Uses Tweepy API to store follower data in sqlite3 database.

# TODO
* Build front-end
* Change sqlite3 to postgres
* Set up logging
* Handle errors
* Optimization:
  * On future checks, compare follower # to DB followers to evaluate optimal algorithm?