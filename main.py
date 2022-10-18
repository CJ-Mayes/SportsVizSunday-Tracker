import logging
import logging.handlers
import os
import pandas as pd
import tweepy

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"
    #logger.info("Token not available!")
    #raise


if __name__ == "__main__":
    logger.info(f"Token value: {SOME_SECRET}")

    consumer_key = 'MOERB99Edk1BWw2dAmGiE27JZ'  # Your API/Consumer key
    consumer_secret = 'xvsPYwQOdb8VNZiFRQl7xa2m2fM7kwle6S5YbAjKQPVaMbjdvn'  # Your API/Consumer Secret Key
    access_token = '1134539278506180608-pGyf6BlvEOMHbaCzb5yFSlspjap1hS'  # Your Access token key
    access_token_secret = 'zvNZqj0sXWhfjQcmZpF6D3sRWHTasTg9mQtxS1OIPvWHr'  # Your Access token Secret key

    # Pass in our twitter API authentication key
    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret,
        access_token, access_token_secret
    )

    # Instantiate the tweepy API
    api = tweepy.API(auth, wait_on_rate_limit=True)

    search_query = "SportsVizSunday"
    no_of_tweets = 99999

    try:
        # The number of tweets we want to retrieved from the search
        tweets = api.search_tweets(q=search_query, count=no_of_tweets)

        # Pulling Some attributes from the tweet
        attributes_container = [[tweet.user.name, tweet.user.screen_name, tweet.user.location, tweet.user.description,
                                 tweet.user.profile_image_url_https, tweet.user.friends_count,
                                 tweet.user.followers_count, tweet.user.url, tweet.created_at, tweet.retweet_count,
                                 tweet.favorite_count, tweet.source, tweet.text, tweet.truncated,
                                 tweet.entities['hashtags'], tweet.in_reply_to_user_id, tweet.is_quote_status] for
                                tweet in tweets]

        # Creation of column list to rename the columns in the dataframe
        columns = ["User", "Screen Name", "Location", "Profile Description", "Profile Image", "Following", "Followers",
                   "Url", "Date Created", "Number of Retweets", "Number of Likes", "Source of Tweet", "Tweet",
                   "Truncated Flag", "Tweet Hashtags", "Reply to Status", "Quote Flag"]

        # Creation of Dataframe
        tweets_df = pd.DataFrame(attributes_container, columns=columns)
    except BaseException as e:
        print('Status Failed On,', str(e))

    print(tweets_df)
    tweets_df.to_csv('SportsVizSunday_Data.csv', encoding='utf-8', index=False)
