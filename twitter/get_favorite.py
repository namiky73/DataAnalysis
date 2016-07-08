import sys
import tweepy
import csv
import sqlite3
import time


class favorite_tweet_info:
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
            insert or replace into favorites
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


def get_tweet_info(user, fav_tweet):
    fav_tweet = favorite_tweet_info(fav_tweet.author.screen_name,fav_tweet.author.followers_count,
                               fav_tweet.text,fav_tweet.id,fav_tweet.created_at,
                               fav_tweet.favorite_count,user)
    return fav_tweet



if __name__ == '__main__':

    if len(sys.argv) < 4:
        print("[warning] input a keyword")
        quit()
    user = sys.argv[1]
    start = int(sys.argv[2])
    end = int(sys.argv[3])

    con = sqlite3.connect("./data/tweet.sqlite3",timeout=30.0)
    auth = get_auth(2)
    api = tweepy.API(auth)

    j = 4
    for i in range(start,end+1):
        if i%5 == 0:
            auth = get_auth(j)
            api = tweepy.API(auth)
            j = j%5 + 1
        print(i)
        time.sleep(5)
        fav_tweets = api.favorites(user, page=i)
        for fav_tweet in fav_tweets:
            fav_tweet_info = get_tweet_info(user,fav_tweet)
            fav_tweet_info.insert_into_db(con)
        con.commit()

    # c = tweepy.Cursor(api.search, q=argvs[1])
    # for a in c.items(20):
    #     print("--------------")
    #     print(a.text)
    # print(api.home_timeline()[0].text)
    # print(api.get_user('namiky73'))
    # print(api.user_timeline('namiky73'))

    con.close()
