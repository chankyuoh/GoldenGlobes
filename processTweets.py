import re, pickle, nltk, os, csv
from collections import Counter


def subtract_lists(a, b):
    multiset_difference = Counter(a) - Counter(b)
    result = []
    for i in a:
        if i in multiset_difference:
            result.append(i)
            multiset_difference -= Counter((i,))
    return result

if not os.path.isfile('awardRegexs.dat'):
    print "please run preprocess.py first"
    quit()

# this dict maps awards to regex
f = open('awardRegexs.dat', "r")
u = pickle.Unpickler(f)
awardDict = u.load()
f.close()

f = open('stopWords.dat', "r")
u = pickle.Unpickler(f)
ignoreWords = u.load()
f.close()

hostOccurrences = {}
awardsTweets = {}
presentAwardsTweets = {}
nomineeAwardsTweets = {}
hashtags = []
handles = []

with open('goldenglobes_preprocess.txt', 'rb') as tweetsFile:
    tweets = csv.reader(tweetsFile, delimiter=',')
    # iterate over each tweet
    for tweet in tweets:
        tweetTokens = nltk.word_tokenize(tweet[0])
        # handles host tweets
        if re.search('host', tweet[0], flags=re.I):
            if '@' in tweet[0]:
                for i in range(0, len(tweetTokens)):
                    if tweetTokens[i] == '@' and i+1 < len(tweetTokens):
                        handle = tweetTokens[i+1]
                        if handle in hostOccurrences:
                            hostOccurrences[handle] += 1
                        else:
                            hostOccurrences[handle] = 1
        # for other tweets
        # else:
        elif re.search('win', tweet[0], flags=re.I):
            for key, value in awardDict.iteritems():
                if re.search(r"[^a-zA-Z]%s[^a-zA-Z]" % value, tweet[0], flags=re.I | re.X):
                    t = tweet[0].lower()
                    t = t.translate(None, ',.?!:;/()\"\'')
                    awardsTweets.setdefault(key, []).append(t)
                    break
        elif re.search('present', tweet[0], flags=re.I):
            for key, value in awardDict.iteritems():
                if re.search(r"[^a-zA-Z]%s[^a-zA-Z]" % value, tweet[0], flags=re.I | re.X):
                    t = tweet[0].lower()
                    t = t.translate(None, ',.?!:;/()\"\'')
                    presentAwardsTweets.setdefault(key, []).append(t)
                    break
        elif re.search('nomin', tweet[0], flags=re.I):
            for key, value in awardDict.iteritems():
                if re.search(r"[^a-zA-Z]%s[^a-zA-Z]" % value, tweet[0], flags=re.I | re.X):
                    t = tweet[0].lower()
                    t = t.translate(None, ',.?!:;/()\"\'')
                    nomineeAwardsTweets.setdefault(key, []).append(t)
                    break

        if '#' in tweet[0]:
            for i in range(0, len(tweetTokens)):
                if tweetTokens[i] == '#' and i+1 < len(tweetTokens):
                    hashtag = tweetTokens[i+1].lower()
                    hashtags.append(hashtag)

        if '@' in tweet[0]:
            for i in range(0, len(tweetTokens)):
                if tweetTokens[i] == '@' and i+1 < len(tweetTokens):
                    handle = tweetTokens[i+1].lower()
                    handles.append(handle)

print ""
stopWords = nltk.corpus.stopwords.words('english')
for key, value in awardsTweets.iteritems():
    awardsTweets[key] = Counter([words for segments in value for words in segments.split()])
    possibilities = []
    for k, v in awardsTweets[key].most_common(25):
        possibilities.append(k)
    possibilities = subtract_lists(subtract_lists(possibilities, stopWords), ignoreWords)
    print 'Winner of ' + key+': ',
    for possibility in possibilities:
        if not re.search('http', possibility, flags=re.I | re.X):
            print possibility.replace("@","").replace("#","") + " ",
    print ""
print ""

for key, value in presentAwardsTweets.iteritems():
    presentAwardsTweets[key] = Counter([words for segments in value for words in segments.split()])
    possibilities = []
    for k, v in presentAwardsTweets[key].most_common(25):
        possibilities.append(k)
    for i in range(0, len(possibilities)):
        possibilities[i] = possibilities[i].replace("@","").replace("#","")
    possibilities = subtract_lists(subtract_lists(possibilities, stopWords), ignoreWords)
    print 'Presenter of ' + key+': ',
    for possibility in possibilities:
        if not re.search('http', possibility, flags=re.I | re.X):
            print possibility + " ",
    print ""
print ""

for key, value in nomineeAwardsTweets.iteritems():
    nomineeAwardsTweets[key] = Counter([words for segments in value for words in segments.split()])
    possibilities = []
    for k, v in nomineeAwardsTweets[key].most_common(40):
        possibilities.append(k)
    for i in range(0, len(possibilities)):
        possibilities[i] = possibilities[i].replace("@","").replace("#","")
    possibilities = subtract_lists(subtract_lists(possibilities, stopWords), ignoreWords)
    print 'Nominees for ' + key+': ',
    for possibility in possibilities:
        if not re.search('http', possibility, flags=re.I | re.X):
            # print possibility.replace("@","").replace("#","") + " ",
            print possibility + " ",
    print ""
print ""

hostGuess = ""
maxMentions = 0
for handle, counter in hostOccurrences.items():
    if counter > maxMentions:
        hostGuess = handle
        maxMentions = counter

print "Host: ", hostGuess
print ""

allHashtags = Counter([words for segments in hashtags for words in segments.split()])
possibilities = []
for k, v in allHashtags.most_common(25):
    possibilities.append(k)
possibilities = subtract_lists(subtract_lists(possibilities, stopWords), ignoreWords)
print 'Most used hashtags: ',
for possibility in possibilities:
    if not re.search('http', possibility, flags=re.I | re.X):
        print possibility.replace("@","").replace("#","") + " ",
print ""
print ""

allHandles = Counter([words for segments in handles for words in segments.split()])
possibilities = []
for k, v in allHandles.most_common(25):
    possibilities.append(k)
possibilities = subtract_lists(subtract_lists(possibilities, stopWords), ignoreWords)
print 'Most used handles: ',
for possibility in possibilities:
    if not re.search('http', possibility, flags=re.I | re.X):
        print possibility.replace("@","").replace("#","") + " ",
print ""
print ""
