import csv, pickle, sys, re

if len(sys.argv) != 2:
    print "usage: python preprocess.py <award+regex csv>"
    quit()

# get list of arguments
args = sys.argv

awardsFile = args[1]

awardsDict = {}

with open(awardsFile, 'rb') as awardsCsv:
    csvReader = csv.reader(awardsCsv, delimiter=',')
    outputFile = open('awardRegexs.dat', 'wb')
    for row in csvReader:
        awardsDict[row[0]] = row[1]
    p = pickle.Pickler(outputFile)
    p.dump(awardsDict)
    outputFile.close()

