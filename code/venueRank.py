import numpy as np
import math
import csv
import operator

paperVenue = {}
venueLink = {}
oldRank = {}
newRank = {}

venueNum = 0
iterNum = 0

alpha = 0.1
threshold = 10**-7

with open("../2014/acl-metadata.txt", 'r') as infile:
    while True:
        id = infile.readline().strip()
        if not id:
            break
        author = infile.readline()
        title = infile.readline().strip()
        if title[-1] != '}':
            tmp = infile.readline().strip()
            title += tmp
        venue = infile.readline().strip()
        year = infile.readline()
        blank = infile.readline()
        if len(blank) > 1:
            exit(1)
        
        id = id[6:-1]
        venue = venue[9:-1]

        paperVenue[id] = venue
        if not oldRank.has_key(venue):
            oldRank[venue] = 1.0
            newRank[venue] = 0.0
            venueNum += 1

with open("../2014/networks/paper-citation-network-nonself.txt", 'r') as infile:
    while True:
        line = infile.readline()
        if not line:
            break

        content = line.split(" ==> ")
        if len(content) != 2:
            continue
        content[0] = content[0].strip('\n').strip(' ')
        content[1] = content[1].strip('\n').strip(' ')

        if not venueLink.has_key(paperVenue[content[0]]):
            venueLink[paperVenue[content[0]]] = {}
            venueLink[paperVenue[content[0]]][paperVenue[content[1]]] = 1
        else:
            if not venueLink[paperVenue[content[0]]].has_key(paperVenue[content[1]]):
                venueLink[paperVenue[content[0]]][paperVenue[content[1]]] = 1
            else:
                venueLink[paperVenue[content[0]]][paperVenue[content[1]]] += 1
        
        

# init rank
for venue in oldRank.keys():
    oldRank[venue] /= venueNum

print "Begin to pagerank for venues..."
#pagerank
while True:
    iterNum += 1

    for i in venueLink.keys():
        outerNum = 0
        for j in venueLink[i].keys():
            outerNum += venueLink[i][j]
        for j in venueLink[i].keys():
            newRank[j] += oldRank[i] * venueLink[i][j] / outerNum

    changes = 0
    for venue in newRank.keys():
        tmp = newRank[venue] * alpha + (1 - alpha) / venueNum
        changes += abs(oldRank[venue] - tmp)

        oldRank[venue] = tmp
        newRank[venue] = 0
    
    print "iterNum: " + str(iterNum) + " changes: " + str(changes)
    if changes < threshold or iterNum > 20:
        break
print "------------------------------------"

print "Top 10 venues:(" + str(venueNum) + " venues included)"
sortedRank = sorted(oldRank.items(), key=operator.itemgetter(1), reverse=True)
for i in range(0, 10):
    print sortedRank[i][0], sortedRank[i][1]
print "------------------------------------"

print "Save the result to file \"../results/retVenue.csv\"..."
with open("../results/retVenue.csv", "wb") as outfile:
    writer = csv.writer(outfile)
    for i in range(0, len(sortedRank)):
        writer.writerow([sortedRank[i][0], sortedRank[i][1]])