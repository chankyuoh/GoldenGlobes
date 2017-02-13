import csv, pickle, sys, re

if len(sys.argv) != 3:
    print "usage: python preprocess.py <award+regex csv> <stop words csv>"
    quit()

# get list of arguments
args = sys.argv

awardsFile = args[1]
stopWordsFile = args[2]

awardsDict = {}
stopWords = []

with open(awardsFile, 'rb') as awardsCsv:
    csvReader = csv.reader(awardsCsv, delimiter=',')
    outputFile = open('awardRegexs.dat', 'wb')
    for row in csvReader:
        awardsDict[row[0]] = row[1]
    p = pickle.Pickler(outputFile)
    p.dump(awardsDict)
    outputFile.close()

with open(stopWordsFile, 'rb') as stopWordsCsv:
    csvReader = csv.reader(stopWordsCsv, delimiter=',')
    outputFile = open('stopWords.dat', 'wb')
    for row in csvReader:
        stopWords.append(row[0])
    p = pickle.Pickler(outputFile)
    p.dump(stopWords)
    outputFile.close()
