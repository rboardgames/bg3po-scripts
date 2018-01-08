import praw
from bg3po_oauth import login

subname = 'boardgames'
reddit = login()
subreddit = reddit.subreddit(subname)

flairs = {}
flair_templates = subreddit.flair.templates
for ft in flair_templates:
    if ft['flair_css_class']:
        flairs[ft['flair_css_class'][6:]] = 0

for f in subreddit.flair(limit=None):
    if f['flair_css_class']:
        if f['flair_css_class'] not in flairs:
            print('Found error in flairs: {}'.format(f))
            flairs[f['flair_css_class']] = 0

        flairs[f['flair_css_class']] += 1

count_sorted_flairs = sorted(flairs.items(), key=lambda x: x[1], reverse=True)
name_sorted_flairs = sorted(flairs.items(), key=lambda x: x[0])

for l in [count_sorted_flairs, name_sorted_flairs]:
    print('--------------------------')
    for name, count in l:
        print('* {}: {}'.format(name, count))

print('--------------------------')
# output markup for reddit
print('|Sorted by Count||_____|Sorted by Name||')
print('|------|-----|----|------|-----|')
print('|Name|Count||Name|Count|')
total = 0
for i in range(len(count_sorted_flairs)):
    total += count_sorted_flairs[i][1]
    print('{}|{}||{}|{}'.format(
        count_sorted_flairs[i][0], count_sorted_flairs[i][1],
        name_sorted_flairs[i][0], name_sorted_flairs[i][1]))

print('\n\nTotal users with flair: {}'.format(total))
