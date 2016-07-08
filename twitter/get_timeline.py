import sys
import tweepy
import csv
import sqlite3
import time


class tweet_info:
    def __init__(self,tweet_user,tweet_user_followers,
                 tweet_text,tweet_id,tweet_time,
                 tweet_favorites,user):
        self.tweet_user = tweet_user
        self.tweet_user_followers = tweet_user_followers
        self.tweet_text = tweet_text
        self.tweet_id = tweet_id
        self.tweet_time = tweet_time
        self.tweet_favorites = tweet_favorites
        self.user = user

    def show_info(self):
        print(self.tweet_text)

    def insert_into_db(self,con):
        con.execute('''
            insert or replace into home_tweet
            (tweet_user, tweet_user_followers, tweet_text,
            tweet_id, tweet_time, tweet_favorites, user)
            values(?,?,?,?,?,?,?)
            '''
            ,(self.tweet_user, self.tweet_user_followers, self.tweet_text,
              self.tweet_id, self.tweet_time, self.tweet_favorites, self.user))


def get_auth(num):
    f = open('./data/api_key' + str(num) + '.txt')
    lines = f.readlines()
    f.close()
    keys = []
    for line in lines:
        keys.append(line.rstrip('\n'))

    CONSUMER_KEY = keys[0]
    CONSUMER_SECRET = keys[1]
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    ACCESS_TOKEN = keys[2]
    ACCESS_SECRET = keys[3]
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    return auth


def get_tweet_info(user, tweet):
    tweet_data = tweet_info(tweet.author.screen_name,tweet.author.followers_count,
                               tweet.text,tweet.id,tweet.created_at,
                               tweet.favorite_count,user)
    return tweet_data



if __name__ == '__main__':

    if len(sys.argv) < 4:
        print("[warning] input a keyword")
        quit()
    user = sys.argv[1]
    start = int(sys.argv[2])
    end = int(sys.argv[3])

    con = sqlite3.connect("./data/tweet.sqlite3",timeout=30.0)
    auth = get_auth(1)
    api = tweepy.API(auth)

    for i in range(start,end+1):
        print(i)
        time.sleep(5)
        tweets = api.home_timeline(count=200, page=i)
        for tweet in tweets:
            tweet_data = get_tweet_info(user,tweet)
            tweet_data.insert_into_db(con)
            tweet_data.show_info()
        con.commit()
