import re, pickle, nltk, os, csv

if not os.path.isfile('classifiers.dat') or not os.path.isfile('awardKeyWords.dat') or not os.path.isfile('awardsAndNominees.dat'):
    print "please run preprocess.py first"
    quit()

# # load the classifiers
# f = open('classifiers.dat', "r")
# u = pickle.Unpickler(f)
# classifiers = u.load()
# f.close()

# load the award key words
f = open('awardKeyWords.dat', "r")
u = pickle.Unpickler(f)
awardKeyWords = u.load()
f.close()

# # load the awards/nominees
# f = open('awardsAndNominees.dat', "r")
# u = pickle.Unpickler(f)
# awardsAndNominees = u.load()
# f.close()

# load the nomineeOccurrences
f = open('nomineeOccurrences.dat', "r")
u = pickle.Unpickler(f)
nomineeOccurrences = u.load()
f.close()

# # initialize a dict that will map classifier -> award key word -> word in tweet -> number of occurrences
# words = {}
#
# # initialize a dict that will map classifier -> award key word -> total number of words
# # this will only count the number of words that were within three words of the classifier
# wordCounts = {}
#
# for classifier in classifiers:
#     words[classifier] = {}
#     wordCounts[classifier] = {}
#     for awardKeyWord in awardKeyWords:
#         words[classifier][awardKeyWord] = {}
#         wordCounts[classifier][awardKeyWord] = 0

#print words

# ------------>>>>>>>>>>> use this for present, host, etc. <<<<<<<<<----------
# with open('goldenglobes_preprocess.txt', 'rb') as tweetsFile:
#     tweets = csv.reader(tweetsFile, delimiter=',')
#     # iterate over each tweet
#     for tweet in tweets:
#         # tokenize each tweet
#         tweetTokens = nltk.word_tokenize(tweet[0])
#
#         # check if the classifier is in the tweet
#         for classifier in classifiers:
#             for i in range(0, len(tweetTokens)):
#                 # if you find a variant of the classifier
#                 if re.search(classifier, tweetTokens[i], flags=re.I):
#                     foundAwardKeyWord = False
#                     # check if one of the award key words is also in the tweet
#                     for awardKeyWord in awardKeyWords:
#                         for j in range(0, len(tweetTokens)):
#                             # if you find a variant of an award key word
#                             if re.search(awardKeyWord, tweetTokens[j], flags=re.I):
#                                 foundAwardKeyWord = True
#
#                                 # add all the words w/in 3 words of classifier to words dict
#                                 # update wordsCounts dict accordingly
#                                 for k in range(-3, 0)+range(1, 4):
#                                     if (i+k >= 0) and (i+k) < len(tweetTokens):
#                                         if tweetTokens[k+i] in words[classifier][awardKeyWord]:
#                                             words[classifier][awardKeyWord][tweetTokens[k+i]] += 1
#                                         else:
#                                             words[classifier][awardKeyWord][tweetTokens[k+i]] = 1
#                                         wordCounts[classifier][awardKeyWord] += 1
#                                 # now go on to next award key word (don't keep search tweet for current one)
#                                 break
#
#                     # if didn't find any award key words move on to next classifier
#                     if not foundAwardKeyWord:
#                         break

with open('goldenglobes_preprocess.txt', 'rb') as tweetsFile:
    tweets = csv.reader(tweetsFile, delimiter=',')
    # iterate over each tweet
    for tweet in tweets:
        # if it contains the word win
        if re.search('win', tweet[0], flags=re.I):
            # check if it contains a key word
            for awardKeyWord in awardKeyWords:
                foundAwardKeyWord = False
                if re.search(awardKeyWord, tweet[0], flags=re.I):
                    foundAwardKeyWord = True
                    # if it contains a key word, iterate over all the nominees associated with that key word
                    # if it contains it, increment that nominee's counter
                    # nominees[0] = nominee; nominees[1] = counter
                    for award, nominees in nomineeOccurrences[awardKeyWord].items():
                        for nominee, counter in nomineeOccurrences[awardKeyWord][award].items():
                            x = nominee
                            if ' ' not in nominee:
                                x = '\s' + nominee + '\s'
                            if re.search(x, tweet[0], flags=re.I):
                                nomineeOccurrences[awardKeyWord][award][nominee] += 1

for awardKeyWord, blah in nomineeOccurrences.items():
    for award, nominees in nomineeOccurrences[awardKeyWord].items():
        winner = None
        maxCount = 0
        for nominee, count in nomineeOccurrences[awardKeyWord][award].items():
            if count > maxCount:
                winner = nominee
                maxCount = count
        print award + ": " + winner

# outputFile = open('words.dat', 'wb')
# p = pickle.Pickler(outputFile)
# p.dump(words)
# outputFile.close()
#
# outputFile = open('wordCounts.dat', 'wb')
# p = pickle.Pickler(outputFile)
# p.dump(wordCounts)
# outputFile.close()
#
# outputFile = open('nomineeOccurrences.dat', 'wb')
# p = pickle.Pickler(outputFile)
# p.dump(nomineeOccurrences)
# outputFile.close()

