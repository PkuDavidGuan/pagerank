import numpy as np
import math
import pickle
import csv
import operator

authorLink = {}
oldRank = {}
newRank = {}

authorNum = 0
iterNum = 0

alpha = 0.1
threshold = 10**-7

with open("../2014/networks/author-citation-network-nonself.txt", 'r') as infile:
    while True:
        line = infile.readline()
        if not line:
            break

        content = line.split(" ==> ")
        if len(content) != 2:
            continue
        content[0] = content[0].strip('\n').strip(' ')
        content[1] = content[1].strip('\n').strip(' ')

        if not authorLink.has_key(content[0]):
            authorLink[content[0]] = [content[1]]
            oldRank[content[0]] = 1.
            newRank[content[0]] = 0
            authorNum += 1
        else:
            authorLink[content[0]].append(content[1])
        
        if not oldRank.has_key(content[1]):
            oldRank[content[1]] = 1.
            newRank[content[1]] = 0
            authorNum += 1

print "Begin to pagerank for authors..."
# init rank
for author in oldRank.keys():
    oldRank[author] /= len(oldRank)

#pagerank
while True:
    iterNum += 1

    for author in authorLink.keys():
        addRank = oldRank[author] * 1.0 / len(authorLink[author])
        for j in authorLink[author]:
            newRank[j] += addRank

    changes = 0
    for author in newRank.keys():
        tmp = newRank[author] * alpha + (1 - alpha) / authorNum
        changes += abs(oldRank[author] - tmp)

        oldRank[author] = tmp
        newRank[author] = 0
    
    print "iterNum: " + str(iterNum) + " changes: " + str(changes)
    if changes < threshold or iterNum > 20:
        break
print "------------------------------------"

print "Top 10 authors:(" + str(authorNum) + " authors included)"
sortedRank = sorted(oldRank.items(), key=operator.itemgetter(1), reverse=True)
for i in range(0, 10):
    print sortedRank[i][0], sortedRank[i][1]
print "------------------------------------"

print "Save the result to file \"../results/retAuthor.csv\"..."
with open("../results/retAuthor.csv", "wb") as outfile:
    writer = csv.writer(outfile)
    for i in range(0, len(sortedRank)):
        writer.writerow([sortedRank[i][0], sortedRank[i][1]])        