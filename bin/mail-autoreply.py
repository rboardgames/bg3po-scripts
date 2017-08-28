#!/usr/bin/env python3

# checks /u/bg3po's PMs and sends a notice to the sender to let them
# know that their message has not been read by their intended 
# recipient

import praw
from praw.models import Comment, Message
import sys
import logging
import re
from bg3po_oauth import login

log = logging.getLogger(__name__)

SUBREDDIT='boardgames'
AUTOREPLY_MSG = """\
You have PM'ed /u/bg3po.  This user is a bot account for doing administrative
tasks for the moderators of /r/boardgames. No human checks this account.

Please double check who you intended to send the message to. If your message
is of an administrative nature for /r/boardgames, please 
[message the moderators](http://www.reddit.com/message/compose?to=%2Fr%2Fboardgames)"""

def set_ks_link(r, msg):
    '''Extract day and link from message body and update sidebar with it.'''
    print('Setting KS roundup link in sidebar')
    sr = r.get_subreddit(SUBREDDIT)
    sb = sr.get_settings()['description']
    m = re.search('Date: ([0-9/]+)[ \n]', msg.body)
    if not m:
        print('Unable to find date in message body.')
        return

    day = m.group(1)
    m = re.search('Link: (.+)[\n]', msg.body)
    if not m:
        print('Unable to find link in message body.')
        return

    link = m.group(1)
    if len(link) != 6:
        print('Ignoring badly formatted KS Roundup URL. Must be only six chars.')
        return

    # [Kickstarter Roundup 10/25](/3q5p6x)
    new_ks_link = '[Kickstarter Roundup {}](/{})'.format(day, link)
    print('New link: {}'.format(new_ks_link))
    new_sb = re.sub(r'\[Kickstarter Roundup ([0-9/]+)\]\(\/[a-z0-9]+\)', new_ks_link, sb, 1)
    sr.update_settings(description=new_sb)

def to_stick_or_not_to_stick_that_is_the_question(r, msg, sticky):
    mode = 'sticky' if sticky else 'unsticky'
    print('Setting post to {}'.format(mode))
    sr = r.get_subreddit(SUBREDDIT)
    
    url = msg.body
    print('getting submission: {}'.format(url))
    sub = r.get_submission(url)
    if not sub:
        print('Error finding post with given URL: {}'.format(url))
        return

    if not sticky:
        sub.unsticky()
    else:
        sub.sticky()

def set_unsticky(r, msg):
    '''Set the given thread to be sticky.'''
    to_stick_or_not_to_stick_that_is_the_question(r, msg, sticky=False)

def set_sticky(r, msg):
    '''Set the given thread to be sticky.'''
    to_stick_or_not_to_stick_that_is_the_question(r, msg, sticky=True)

# all /r/bg mods can execute any command
# these should be read from somewhere rather than hardcoded. 
mods = [
    'phil_s_stein',
    'Zelbinian'
    'DaboGirl'
]

# specific commands may be executable by non-mods. 
cmds = {
    'setksru': {
        # 'allowed': mods + ['someuser', 'anotheruser']  # non-mod user example
        'allowed': mods,
        'cmd': set_ks_link
    },
    'sticky post': {
        'allowed': mods,
        'cmd': set_sticky
    },
    'unsticky post': {
        'allowed': mods,
        'cmd': set_unsticky
    }
}

def main():
    r = login()
    unread = r.inbox.unread(limit=None)

    for msg in unread:
        if isinstance(msg, Comment):
            # this is probably a mention in a comment body. Ignore it.
            pass
        elif isinstance(msg, Message):
            # first check for bg3po commands.
            if msg.subject in cmds:
                if msg.author.name in cmds[msg.subject]['allowed']:
                    log.info('Handling command {} from {}'.format(msg.subject, msg.author.name))
                    cmds[msg.subject]['cmd'](r, msg)

            else:   # All other messages the bg3po get the auto-response.
                msg.reply(AUTOREPLY_MSG)

        log.info('Marking bg3po {} as read: {}'.format(msg.__class__, msg))
        msg.mark_read()

if __name__ == '__main__':
    main()
