import pandas as pd
import numpy as np
from scipy.special import softmax
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class Sentiment_Analysis():

  def __init__(self, model_path):
    # load the model and tokenizer
    self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
    self.tokenizer = AutoTokenizer.from_pretrained(model_path)

  def preprocess_tweets(self, data):
    all_tweets = data['text'].tolist()
    processed_tweets = []
    for tweet in all_tweets:
      current_tweet = []

      if '\n\n'  in tweet:
        tweet  = tweet.replace('\n\n', ' ')
      elif '\n' in tweet:
        tweet = tweet.replace('\n', ' ')

      for word in tweet.split(' '):
        if '@' in word and len(word) > 1:
          word = '@user'
        elif word.startswith('http'):
          word = 'http'
        
        current_tweet.append(word)
      processed_tweet = " ".join(current_tweet)
      processed_tweets.append(processed_tweet)

    return processed_tweets

  def sentiment_analysis(self, tweets):
    labels = ['Negative', 'Neutral', 'Positive']
    rated_tweets = []

    for t in tweets:
      encoded_tweet = self.tokenizer(t, return_tensors = 'pt')

      output = self.model(**encoded_tweet)
      scores = softmax(output[0][0].detach().numpy())
      max_value = np.max(scores)
      index_of_max_values = np.where(scores == max_value)[0][0]
      
      rated_tweets.append((labels[index_of_max_values], max_value))
    
    return rated_tweets