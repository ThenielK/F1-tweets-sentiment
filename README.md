# Introduction
The project aimed to analyze the sentiment of the post-Grand Prix tweets for each team for the current 2022 season. For the scope of the project, only three teams were used - Red Bull Racing, Scuderia Ferrari, and Mercedes AMG Petronas. However, it can be done with all F1 teams, as long as they have a Twitter account and use it. This repository is complementary to and contains the code briefly explained in this Towards Data Science article: https://medium.com/@nielsdeckers/how-does-formula-1-grand-prix-performance-impact-twitter-sentiment-3cac02c201b9

# Getting the Twitter data
In the get_twitter_data.py file, there are two ways to acquire the Twitter data of a user.
The first one is by using the tweepy, which is a Python wrapper for the Twitter API v2. However, it has some limitations, for instance, you can get only 3200 tweets. Furthermore, you need to have a Twitter developer account, because you need the authorization to get the data. If you use this function make sure to put all of your authorization keys inside a JSON file named twitter_api.json which has the following format:
    
    {
        "api_key": "",
        "api_secret": "",
        "access_token": "",
        "access_secret": "",
        "client_id": "",
        "client_secret": "",
        "bearer_token:": ""
    }
    
The second approach is by using a library called - snscrape. It is a workaround for the limitation the Twitter API has because they were a problem for this project since three teams do not tweet equally as much. All it requires in order to work is the username of the user's account you want to scrape. We have added a start date, to make sure we do not get older tweets than the first Grand Prix of the season, and a boolean called only_tweets which makes sure we get only the posts of the teams and not the tweets & replies. For this approach, a Twitter developer account is not required.

# Sentiment analysis
We used a pre-trained model called Twitter-roBERTa-base for Sentiment Analysis, and it was trained on 124M tweets from January 2018 to December 2021; hence, it is probably pretty good at detecting the sentiment of the tweets. However, before fitting the data to the model you need to slightly preprocess the data. All tagged accounts have to be replaced with simply @ and the website links with http. We've found out that if the tags or the website links are on a new line they won't be transformed because the string value of the tweet looks like this - something something #great \n\nsometing else blah blah. So we also make sure to get rid of the new lines by replacing them with a simple enter. The code for this is in the sentiment_analysis.py file.

Now, when we have processed the tweets, it is time to perform a sentiment analysis on them using the model we've downloaded. For each text, we will receive a one-dimensional array with three values. These values represent the confidence of the model about the tweet being in one of the three categories - Negative, Neutral, and Positive. The sentiment of the tweet is the one for which the confidence score is the highest. For instance, ['Positive', 0.912352]. Our advice is to run this notebook with GoogleColab, because this is how it is set, and you will have to change the code cells a bit to get it working in Jupyter Notebook/Lab.

# Visualization and Results
Godd look with the Power BI :) Maybe we will add it some other time!

 
