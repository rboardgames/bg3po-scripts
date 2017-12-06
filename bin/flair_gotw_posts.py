import logging
import praw
from bg3po_oauth import login

reddit = login()
user = 'bg3po'
sub = 'boardgames'

for s in reddit.redditor(user).submissions.new(limit=None):
    if s.subreddit == sub:
        if 'Game of the Week' in s.title:
            if 'Redux' not in s.title:
                print(s.title)
                s.mod.flair(text='GotW', css_class='gotw')

