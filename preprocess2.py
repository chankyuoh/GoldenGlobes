from collections import Counter
import csv
import re
from itertools import takewhile

rawtweets = 'globestweets.txt'
award_dict = {'best actree': '(best.*actress)'}
awards = {}

with open(rawtweets) as f:
    content = f.readlines()
    for line in content:
        for key,value in award_dict.iteritems():
            if re.search(r"[^a-zA-Z]%s[^a-zA-Z]" % value, line, flags=re.I | re.X):
                awards.setdefault(key, []).append(line)
                break

for key,value in awards.iteritems():
    awards[key] = Counter([words for segments in value for words in segments.split()])
    print key+' winner may be ',
    print awards[key].most_common(10)
