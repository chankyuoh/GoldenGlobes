import csv, pickle, sys, re

# get list of arguments
args = sys.argv

awardsFile = args[1]
awardKeyWordsFileName = args[2]
awardsAndNomineesFileName = args[3]

awardsList = []
awardsRegexList = []
awardsDict = {}
awardKeyWordsList = []
awardsAndNominees = {}

with open(awardsFile, 'rb') as awardsCsv:
    csvReader = csv.reader(awardsCsv, delimiter=',')
    outputFile = open('awardRegexs.dat', 'wb')
    for row in csvReader:
        awardsDict[row[0]] = row[1]
    p = pickle.Pickler(outputFile)
    p.dump(awardsDict)
    outputFile.close()

with open(awardKeyWordsFileName, 'rb') as awardKeyWordsCsv:
    csvReader = csv.reader(awardKeyWordsCsv, delimiter=',')
    outputFile = open('awardKeyWords.dat', 'wb')
    #awardKeyWordsList = []
    for row in csvReader:
        awardKeyWordsList.append(row[0])
    p = pickle.Pickler(outputFile)
    p.dump(awardKeyWordsList)
    outputFile.close()

with open(awardsAndNomineesFileName, 'rb') as awardsAndNomineesCsv:
    csvReader = csv.reader(awardsAndNomineesCsv, delimiter=',')
    outputFile = open('awardsAndNominees.dat', 'wb')
    #awardsAndNominees = {}
    for row in csvReader:
        nominees = []
        award = row[0]
        for i in range(1,len(row)):
            nominees.append(row[i])
        awardsAndNominees[award] = nominees
    p = pickle.Pickler(outputFile)
    p.dump(awardsAndNominees)
    outputFile.close()

# will map award key word -> award name -> nominee -> # of occurrences
nomineeOccurrences = {}
for awardKeyWord in awardKeyWordsList:
    nomineeOccurrences[awardKeyWord] = {}

for award, nominees in awardsAndNominees.items():
    for awardKeyWord in awardKeyWordsList:
        if re.search(awardKeyWord, award, flags=re.I):
            nomineeOccurrences[awardKeyWord][award] = {}
            for nominee in nominees:
                nomineeOccurrences[awardKeyWord][award][nominee] = 0
            break

outputFile = open('nomineeOccurrences.dat', 'wb')
p = pickle.Pickler(outputFile)
p.dump(nomineeOccurrences)
outputFile.close()
