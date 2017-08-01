#!/usr/bin/env python3
import praw
from bg3po_oauth import login
import re
from datetime import datetime
from html import unescape

SUBREDDIT = "boardgames"
POST_BODY = "/home/bg3po/bg3po-scripts/etc/bazaar_post_body.red"


def get_month():
    month = datetime.now().strftime("%B")
    return(month)


def get_body():
    f = open(POST_BODY)
    body = f.read()
    f.close()
    return body


def post_bazaar(reddit, month):
    title = month + " Board Game Bazaar"
    post_text = get_body()
    post = reddit.subreddit(SUBREDDIT).submit(title=title, selftext=post_text)
    return (post.id)


def change_sidebar(reddit, post_id, month):
    sr = reddit.subreddit(SUBREDDIT)
    sidebar = unescape(reddit.subreddit(SUBREDDIT).description)
    new_bazaar = r'['+month+' Bazaar](/'+post_id+')'
    new_sb = re.sub(r'\[[a-zA-Z]+ Bazaar\]\(\/[a-z0-9]+\)', new_bazaar, sidebar, 1)
    reddit.subreddit(SUBREDDIT).mod.update(description=new_sb)


def main():
    month = get_month()
    reddit = login()
    post_id = post_bazaar(reddit, month)
    change_sidebar(reddit, post_id, month)

if __name__ ==  '__main__':
    main()
