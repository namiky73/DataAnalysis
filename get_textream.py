import socks
import socket
import urllib.request, urllib.error
from bs4 import BeautifulSoup
import sqlite3
import sys
from stem import Signal
from stem.control import Controller
# from urllib.request import FancyURLopener
# from datetime import datetime
# import time
# import random



class Tor:
    def __init__(self):
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050)
        socket.socket = socks.socksocket
    def test(self):
        return urllib.request.urlopen("https://api.ipify.org?format=json").read()


class PostItem:
    def __init__(self,user,user_url,comment,year,date_mmdd,time24,positive,negative):
        self.user = user
        self.user_url = user_url
        self.comment = comment
        self.year = year
        self.date_mmdd = date_mmdd
        self.time24 = time24
        self.positive = positive
        self.negative = negative

    def check(self):
        print(self.user,"[",self.user_url,"]")
        print(str(self.year)+self.date_mmdd,self.time24)
        print(self.comment)
        print(self.positive,self.negative)


def get_thread_info(url):
    thread_info = {}
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html,'lxml')

    thread_count = soup.find("h1").find("a").get("href").rsplit("/",1)[1].replace(",","")
    comment_count = soup.find(class_="threadLength").string.replace(",","")
    span = soup.find("h1").getText().rsplit(" ",1)[1]

    # span = span.rstrip("〜")
    spans = span.split("〜")
    span_start = spans[0]
    if len(spans) == 2:
        if spans[1] == "":
            span_end = "now"
        else:
            span_end = spans[1]
    else:
        span_end = "one day"

    thread_info["thread_count"] = int(thread_count)
    thread_info["comment_count"] = int(comment_count)
    thread_info["span_start"] = span_start.replace("/","")
    # span_endは、日付・"now(継続中)"・"one day（1日未満のスレッド）"のいずれか
    thread_info["span_end"] = span_end.replace("/","")
    return thread_info


def scrape_page(url):
    post_item_list = []
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html,'lxml')
    comment_divs = soup.find_all("div",class_="comment")

    for comment_div in comment_divs:
        user_p = comment_div.find("p",class_="comWriter")
        user_a = user_p.find("a")
        if user_a:
            user = user_a.getText();
            user_url = user_a.get("href")
        else:
            user = "unknown"
            user_url = "unknown"
        # print(user,user_url)

        date_time = user_p.find("span",class_=None).getText().split(" ")
        date = date_time[0]
        time24 = date_time[1].replace(":","")
        month_day = date.split("月",1)
        month = month_day[0]
        day = month_day[1].rstrip("日")
        if len(month) == 1:
            month = "0" + month
        if len(day) == 1:
            day = "0" + day
        # print(month+day,time24)

        comment = comment_div.find("p",class_="comText").getText()
        # print(comment)

        positive = comment_div.find("li",class_="positive").find("span").getText()
        negative = comment_div.find("li",class_="negative").find("span").getText()
        # print(positive,negative)

        item = PostItem(user,user_url,comment,2016,month+day,time24,positive,negative)
        post_item_list.append(item)

    return post_item_list



if __name__ == '__main__':


    if len(sys.argv) < 2:
        print("[error] input a textream url")
        quit()

    # input_url = "http://textream.yahoo.co.jp/message/1002315/2315/"
    input_url = sys.argv[1]

    count = 1
    with Controller.from_port(port = 9051) as controller:
        Tor = Tor()
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

        thread_count = get_thread_info(input_url)
        print(thread_count)

        post_item_list = scrape_page(input_url)
        for item in post_item_list:
            print("-------------")
            item.check()

        # for row in rows:
        #     if count%10 == 0:
        #         controller.authenticate()
        #         controller.signal(Signal.NEWNYM)
        #     time.sleep(random.uniform(0.5,1.0))
        #     req = urllib.request.Request(
        #         row[1], # URL
        #         data=None,
        #         headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36 (KHTML, like Gecko) Chrome"}
        #     )
