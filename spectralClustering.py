# -*- coding: utf-8 -*-
import gensim
from gensim import models
import json
import operator
import numpy as np
import math
import time
from sklearn.cluster import SpectralClustering
model = models.Doc2Vec.load('/Users/fan/anaconda/bin/Workspace/Doc2Vec_Size_100_1_m_new')
with open('/Users/fan/anaconda/bin/Workspace/data/subject.json', 'r') as f:
     sentiment = json.load(f)
mergedlist = []
for ele in sentiment:
    mergedlist.extend(sentiment[ele]['positiveSubject'])
    mergedlist.extend(sentiment[ele]['negativeSubject'])
getter = operator.itemgetter(0)
mergedlist = list(set(map(getter, mergedlist)))
wordV = [model[ele] for ele in mergedlist]
smatrix = gensim.similarities.MatrixSimilarity(gensim.matutils.Dense2Corpus(np.array(wordV).T))
print 'Similarity Matrix Complete'
sarray = np.array(smatrix)
sarray[sarray>1] = 1.0
sarray[sarray<-1] = -1.0
angularD = np.arccos(sarray)/math.pi
sim = 1 - angularD
print 'Similarity Complete'
print 'Spectral Clustering Begin'
start = time.time()
spectral_clustering = SpectralClustering(n_clusters = 100)
sc = spectral_clustering.fit_predict(sim)
print time.time()-start
r = dict(zip(mergedlist, sc))
tempD = {}
for ele in r:
    if str(r[ele]) not in tempD:
        tempD[str(r[ele])] = [ele]
    else:
        tempD[str(r[ele])].append(ele)
with open('./Workspace/data/SpectralClustering_minCount_1_n_100.json', 'w') as f:
    json.dump(tempD, f)