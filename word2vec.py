import codecs
import time
from gensim import models

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        with codecs.open(self.dirname,'r','utf-8') as f:
            for line in f.readlines():
                yield line.lower().split()

start = time.time()
mysentence = MySentences('/Users/fan/anaconda/bin/workspace/data/jieba_cut_by_sentence_big.txt')
model = models.Word2Vec(mysentence, size=200, window=5, min_count=1, workers=4, sg=1)
#model.save('/Users/fan/anaconda/bin/Workspace/Word2Vec_sz_200_mc_1_sg_by_sentence_big')
print time.time()-start