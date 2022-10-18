import os
import secrets
import pandas as pd
import tweepy

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

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
    # The number of tweets we want to retrieve from the search
    tweets = api.search_tweets(q=search_query, count=no_of_tweets)

    # Pulling Some attributes from the tweet
    attributes_container = [[tweet.user.name, tweet.user.screen_name,tweet.user.location,tweet.user.description,tweet.user.profile_image_url_https,tweet.user.friends_count,tweet.user.followers_count, tweet.user.url, tweet.created_at,tweet.retweet_count, tweet.favorite_count, tweet.source, tweet.text,tweet.truncated, tweet.entities['hashtags'], tweet.in_reply_to_user_id, tweet.is_quote_status] for
                            tweet in tweets]

    # Creation of column list to rename the columns in the dataframe
    columns = ["User","Screen Name","Location","Profile Description","Profile Image", "Following","Followers", "Url", "Date Created", "Number of Retweets","Number of Likes", "Source of Tweet", "Tweet", "Truncated Flag", "Tweet Hashtags", "Reply to Status", "Quote Flag"]

    # Creation of Dataframe
    tweets_df = pd.DataFrame(attributes_container, columns=columns)
except BaseException as e:
    print('Status Failed On,', str(e))

tweets_df.to_csv('SportsVizSunday_Data.csv', encoding='utf-8', index=False)
