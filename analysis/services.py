import os
import requests
import pandas as pd
import tweepy as tw
from sqlalchemy import create_engine
import MySQLdb
import pymysql
import numpy as np
import spacy
from datetime import date
import re
import preprocessor as p
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English




def normalization(clean_list):
    lem = WordNetLemmatizer()
    normalized_list = []
    for word in clean_list:
        normalized_txt = lem.lemmatize(word,'v')
        normalized_list.append(normalized_txt)
    return normalized_list

def remove_stopwords_normalize(tweet):
    tweet_list = [elem for elem in tweet.split()]
    clean_list = [word for word in tweet_list if word.lower() not in stopwords.words('english')]
    normalized_list = normalization(clean_list)
    new_txt = " ".join([word for word in normalized_list])
    return new_txt

def preprocess(tweets_list):
    df1 = pd.DataFrame(tweets_list, columns = ['id','date','text','place','retweets_count','favorites_count','user_name','followers_count'])
  
    
    for i in range(len(df1)):
        txt = df1.loc[i]["text"]
        user = df1.loc[i]["user_name"]
        user = re.sub(r'[^a-zA-Z0-9_]', '', user)
        txt = txt.lower()
        txt=re.sub('@[A-Z0-9a-z_:]+','',txt)#replace username-tags
        txt=re.sub('^RT+','',txt)#replace RT-tags
        txt = re.sub('https?://[A-Za-z0-9./]+','',txt)#replace URLs
        txt=re.sub("[^a-zA-Z]", " ",txt)#replace hashtags
        df1.at[i,"preprocessed_text"]=txt
        df1.at[i, "user_name"] = user
         
        txt = df1['preprocessed_text'].iloc[i]
        new_txt = remove_stopwords_normalize(txt)
        df1.at[i,"preprocessed_text"] = new_txt
        
    df1 = df1.drop_duplicates(['preprocessed_text'])
    return df1

def collect_tweets(search_words):
        result = {}
        search_words = search_words
        
        # API keys assigned after creating a project using tweepy api on twitter developer site
        api_key = 'bXa3bAs7M4O1d9a3wCyYRq5dn'
        api_secret_key = 'IMXOI0vFU9KhN8Fnjm04K7NCRK6EGy5nxSUuh8FR07s78pHd65'
        access_token = '1300274872958873600-bMOVNLomg5ZZxLLA19AMShgGxB3Xrw'
        access_token_secret = 'oN3gya8E0OVJVD6Q2UTlMJrWrHAELy115qngQweYI80CJ'

        # Connect to Twitter API using the secrets
        auth = tw.OAuthHandler(api_key, api_secret_key)
        auth.set_access_token(access_token, access_token_secret)
        api = tw.API(auth, wait_on_rate_limit=True) #wait_on_rate_limit=True to avoid tweeter error status code 429(invalid url error)
        
        
        tweets_data = tw.Cursor(api.search,q=search_words,lang="en").items(20)
        tweets_list=[]

        for tweet in tweets_data:         
            lst = []
            lst.extend((tweet.id,tweet.created_at,tweet.text,tweet.place,tweet.retweet_count,tweet.favorite_count,tweet.user._json['name'],tweet.user._json['followers_count']))
            tweets_list.append(lst) 

       
        df = preprocess(tweets_list) # preprocess data

        # create sqlalchemy engine
        engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="",
                               db="text_data")) 

        #Delete previously stored data rows
        engine.execute("delete from tweets_table")


        # Insert whole DataFrame into MySQL
        df.to_sql('tweets_table', con =engine, if_exists = 'append', chunksize = 1000,index=False)


def create_tokens_list(df):
      # text_lines is list of list consisting of tokens of each line
  text_tokens_list = list()
  lines = df['text'].values.tolist() # list of all news
  
  for line in lines:
    tokens = word_tokenize(line)
    text_tokens_list.append(tokens) # lists of lists containing tokens of a news headline

  return text_tokens_list

def create_sequences(text_tokens_list):
  #vectorize text samples into 2D tensor
  tokenizer_obj = Tokenizer()
  tokenizer_obj.fit_on_texts (text_tokens_list)
  sequences = tokenizer_obj.texts_to_sequences(text_tokens_list) 

  print("tokenizer_obj: ",tokenizer_obj)
  print("sequences[0]: ",sequences[0])

  word_index = tokenizer_obj.word_index
  print("Found %d unique tokens." % len(word_index))

  return word_index,sequences

def calculate_max_length(df):
  max_length = max([len(s.split()) for s in df['text']]) #max length of text in corpus
  print("max length : ",max_length)
  return max_length

def padding_sequences(df,sequences,max_length):
  text_pad = pad_sequences(sequences, maxlen = max_length)

  print("Shape of text tensor: ", text_pad.shape)

  return text_pad

