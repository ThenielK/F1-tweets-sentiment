# Libraries
import json
import requests
import pandas as pd
from datetime import date, timedelta
import snscrape.modules.twitter as sntwitter

def get_account_data(username, start_date = '2022-03-20', only_tweets = True):
    end_date = date.today() + timedelta(1)
    query = f"(from:{username}) until:{end_date} since:{start_date}"
    tweets = []

    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        if only_tweets:
            if tweet.inReplyToUser == None:
                tweets.append([tweet.content, tweet.id, tweet.date, tweet.retweetCount, tweet.replyCount, tweet.likeCount, tweet.quoteCount, tweet.user.username])
        else:
            tweets.append([tweet.content, tweet.id, tweet.date, tweet.retweetCount, tweet.replyCount, tweet.likeCount, tweet.quoteCount, tweet.user.username])

    df = pd.DataFrame(tweets, columns = ['text', 'id', 'created_at', 'public_metrics.retweet_count', 'public_metrics.reply_count', 'public_metrics.like_count', 'public_metrics.quote_count', 'user'])
    
    return df

# Creates the pd.DataFrame with the last 3100 tweets of an account
def get_account_data_api(username, token, num_tweets = 100, increment = 100):

    if num_tweets > 3200:
        raise Exception("num_tweets cannot be larger than 3200")

    if num_tweets < increment:
        raise Exception("num_tweets should be at least equal or 2,3,4,5,...31 times bigger")

    if increment > 100:
        raise Exception("the increment should be less than 100!")

    loop_range = num_tweets/increment
    if loop_rwon("The num_tweets divided by the increment should yield an integer")

    headers = {"Authorization": "Bearer " + token['access_token']}

    response_user = requests.get('https://api.twitter.com/2/users/by/username/' + username, headers=headers)
    user_info = response_user.json()
    twitterID = user_info['data']['id']

    response_tweets = requests.get(f'https://api.twitter.com/2/users/{twitterID}/tweets?max_results={increment}&tweet.fields=id,created_at,text,public_metrics', headers=headers)
    tweets_info = response_tweets.json()
    df = pd.json_normalize(tweets_info['data'])
    print(f'The last {increment} tweets')
    
    if loop_range > 1:
        for i in range(int(loop_range-1)):
            metadata = tweets_info['meta']
            if 'next_token' in metadata:
                next_token = metadata['next_token']
                response = requests.get(f'https://api.twitter.com/2/users/{twitterID}/tweets?max_results={increment}&pagination_token={next_token}&tweet.fields=id,created_at,text,public_metrics', headers=headers)
                tweets_info = response.json()
                df_new = pd.json_normalize(tweets_info['data'])
                df = pd.concat([df, df_new], ignore_index = True)
                print(f'The last {(i+2)*increment} tweets')
            df['user'] = username
            

    return df 