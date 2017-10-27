import numpy as np
import math
import pickle
import csv
import operator

paperLink = {}
paperTitle = {}
oldRank = {}
newRank = {}

paperNum = 0
iterNum = 0

alpha = 0.1
threshold = 10**-7

with open("../2014/networks/paper-citation-network-nonself.txt", 'r') as infile:
    tmp = 0
    while True:
        line = infile.readline()
        if not line:
            break

        content = line.split(" ==> ")
        if len(content) != 2:
            continue
        content[0] = content[0].strip('\n').strip(' ')
        content[1] = content[1].strip('\n').strip(' ')

        if not paperLink.has_key(content[0]):
            paperLink[content[0]] = [content[1]]
            oldRank[content[0]] = 1.
            newRank[content[0]] = 0
            paperNum += 1
        else:
            paperLink[content[0]].append(content[1])
        
        if not oldRank.has_key(content[1]):
            oldRank[content[1]] = 1.
            newRank[content[1]] = 0
            paperNum += 1

print "Begin to pagerank for authors..."
# init rank
for paper in oldRank.keys():
    oldRank[paper] /= len(oldRank)

#pagerank
while True:
    iterNum += 1

    for paper in paperLink.keys():
        addRank = oldRank[paper] * 1.0 / len(paperLink[paper])
        for j in paperLink[paper]:
            newRank[j] += addRank

    changes = 0
    for paper in newRank.keys():
        tmp = newRank[paper] * alpha + (1 - alpha) / paperNum
        changes += abs(oldRank[paper] - tmp)

        oldRank[paper] = tmp
        newRank[paper] = 0
    
    print "iterNum: " + str(iterNum) + " changes: " + str(changes)
    if changes < threshold or iterNum > 20:
        break
print "------------------------------------"

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
        title = title[9:-1]

        paperTitle[id] = title

print "Top 10 papers:(" + str(paperNum) + " papers included)"
sortedRank = sorted(oldRank.items(), key=operator.itemgetter(1), reverse=True)
for i in range(0, 10):
    print paperTitle[sortedRank[i][0]], sortedRank[i][1]
print "------------------------------------"

print "Save the result to file \"../results/retPaper.csv\"..."
with open("../results/retPaper.csv", "wb") as outfile:
    writer = csv.writer(outfile)
    for i in range(0, len(sortedRank)):
        writer.writerow([paperTitle[sortedRank[i][0]], sortedRank[i][1]])             