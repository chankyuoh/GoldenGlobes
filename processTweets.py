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
ignoreWords = ['rt', 'golden', 'globes', '#goldenglobes', 'tv', 'win', 'wins', 'winner', 'winning', 'won', 'film',
               'movie', 'series', 'feature', 'supporting', 'actor', 'actress', 'best', 'performance', 'motion',
               'screenplay', 'role', 'limited', 'director', 'animated', 'picture', 'original', 'score', 'foreign',
               'language', 'television', '-', 'drama', 'comedy', 'musical', 'cecil', 'b', 'demille', 'award', 'song',
               'present', '#goldenglobe', '2017', '2017-01-09', '@goldenglobes', 'congrats', 'congratulations',
               '#congrats', 'yes', 'goes', 'globe', 'show', 'shows', 'miniseries', 'mini', 'presenting', 'presenter',
               'presented', 'presents', 'presenters', 'year', '&amp', 'nominee', 'nominees', 'pair', 'next',
               'comedymusical', 'nominating', 'nominated', 'years', 'category', 'nomination', 'nominations', 'clip',
               'watch', 'red', 'carpet', 'dress', 'think', 'believe', 'speech', 'like', 'live', 'night', 'hope',
               'hope', 'goldenglobe', 'goldenglobes', 'goldenglobes2017', 'cnnent', '2017s', '1','2','3','4','5','6',
               '7','8','9','0','seriestv','deserved','#tvseriesmusicalcomedy','much','@writermonkey77','cnnbrk',
               'forbesshowbiz','seriestv', 'musicalcomedy', 'cnn', 'breaking', 'news','psiff17','spanish','starwars',
               'rogueone','orgies','never','mind','place','fifth','three','tonight','nocturnal','g','come','dont',
               'see','forget','tune','good','couldnt','nice','superhero','take','stage','rameshlaus','dubaionetv',
               'dubai1goldenglobes','time','made', 'give','needs','please','toi','goldeng','presentation','rock',
               'ally','equality','well-deserved','sold','undoubtedly','ht','awards','back','represent','honored',
               'incredible','tonights','hubinsurance','mbtsmovie','mov','rules','apply','thenerdaily','even','really',
               'love','nationalscreenwritersdays','day','get','bestactress','drector','notmydebt','directorthere',
               'many','one','female', 'isnt','name','wasnt','single','release','iggypops','luck','1st','whats','sad',
               'wishing','whose','afp','involved','cinema','tells','wallacejnichols','ferdosa_','introduces','interest',
               'search','look','actoractress','alum','shes','great','filmaniaindo','single','every','wishes','women',
               'stunning','therealtaraji','tennews','incredibly','get','burberry','recently','talented','guesswho',
               'receiving','twittermoments','career','30','receives','express_pics','canadamoments','leftbankpics',
               'nuts','season','snubbed','first','wi','jcamilveracruz','psiff17','monday','snapped','last','including',
               'carpet','waiting','watched','cynpark13','introduce','introduces','search','films','interest','none','look',
               '3rd','gets','goldenglobes','turnbull']
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
