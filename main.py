import pandas as pd
import datetime as dt
import time
import tweepy

consumer_key = "1OOdhYWmbmhSOcp9PRuf3XZmo"
consumer_secret = "XlIraBHaTI4JCPJKlMbObWdL29iQ50bZyWd79III4Bq7dTrKZ8"

access_token = "1160107833167364137-rQ1XhXN9AfSsOV3tPna9dqexi64IRD"
access_token_secret = "fwYgmlTYPejzgA9YJT0CuW34DtciSQmyvZiZrtwmQexgV"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

""" 
    Parameters to check for the tweets
    parameter_name: from_date, type: datetime
    parameter_name: to_date, type: datetime
    parameter_name: username, type: string
"""

from_date = dt.datetime(2019, 8, 1, 0, 0, 0)
to_date = dt.datetime(2019, 9, 1, 0, 0, 0)
username = "@AmazonTeamOrg"

""" 
    Columns name:   Column value in twitter status
    text: status.full_text
    created_at: status.created_at
    tweet_id: status.id_str
    retweet_count: status.retweet_count
    favorite_count: status.favorite_count
    user_name: status.user.name
    user_screen_name: status.user.screen_name
    user_description: status.user.description
"""
# Comparing if tweet date is between the threshold date
def compare_date(created_date, from_date, to_date):
    return created_date >= from_date and created_date <= to_date

# handeling the rate limit
def limit(cursor):
    while True:
        try:
            yield cursor.next()
        
        except Exception as e:
            print()
            print(str(e))
            print()
            time.sleep(15 * 60)


tweets_list = []
itcount = 1
for i, status in enumerate(limit(tweepy.Cursor(api.user_timeline, screen_name=username, tweet_mode="extended").items())):
    if(status.created_at < from_date):
            break

    if(compare_date(created_date=status.created_at, from_date=from_date, to_date=to_date)):
        tweet_id_str = "\"" + status.id_str + "\"" 
        tweet_list_item = [
                                    status.full_text,
                                    status.created_at,
                                    tweet_id_str,
                                    status.retweet_count,
                                    status.favorite_count,
                                    status.user.name,
                                    status.user.screen_name,
                                    status.user.description
                                ]
        print(tweet_list_item)
        print()
        tweets_list.append(tweet_list_item)
    
    itcount = itcount + 1
            

columns_name = ["text", "created_at", "tweet_id", "retweet_count", "favorite_count", "user_name", "user_screen_name", "user_description"]
tweet_df = pd.DataFrame( tweets_list, columns=columns_name)

tweet_df.to_csv("./export.csv")
