# -*- coding: utf-8 -*-
import numpy as np
import codecs
import jieba
import jieba.posseg as pseg
import re
import operator
import json
jieba.set_dictionary('./Workspace/sentiment/0616/big/jieba356726.txt')
jieba.load_userdict('./Workspace/sentiment/0616/big/jieba356726.txt')
jieba.load_userdict('./Workspace/sentiment/0616/big/cute.txt')
jieba.load_userdict('./Workspace/sentiment/0616/food/fooddict2027.txt')
jieba.load_userdict('./Workspace/sentiment/0616/menu/menu50806_new.txt')
jieba.load_userdict('./Workspace/sentiment/0616/sentiment/negativewords.txt')
jieba.load_userdict('./Workspace/sentiment/0616/sentiment/positivewords.txt')
jieba.load_userdict('./Workspace/sentiment/0616/sentiment/negative.txt')
jieba.load_userdict('./Workspace/sentiment/0616/sentiment/more.txt')
jieba.load_userdict('./Workspace/sentiment/0616/sentiment/question.txt')
jieba.load_userdict('./Workspace/sentiment/0616/stop/stopword2292.txt')
# 負面
negdict = []
# 正面
posdict = []
# 否定
nodict = []
# 程度
plusdict = []
# 不肯定
question = []
with codecs.open('./expand/negativeWordMerge.txt', 'r', 'utf-8') as f:
    for w in f.readlines():
        negdict.append(w.split()[0])
with codecs.open('./expand/positiveWordMerge.txt', 'r', 'utf-8') as f:
    for w in f.readlines():
        posdict.append(w.split()[0])
with codecs.open('./expand/inverseWordMerge.txt', 'r', 'utf-8') as f:
    for w in f.readlines():
        nodict.append(w.split()[0])
with codecs.open('./expand/degreeWordMerge.txt', 'r', 'utf-8') as f:
    for w in f.readlines():
        plusdict.append(w.split()[0])
with codecs.open('./Workspace/sentiment/0616/sentiment/question.txt', 'r', 'utf-8') as f:
    for w in f.readlines():
        question.append(w.split()[0])

food = []
with codecs.open('./Workspace/sentiment/0616/menu/menu50806_new.txt', 'r','utf-8') as f:
    for w in f.readlines():
        food.append(w.replace(' 5000 n\n',''))
with codecs.open('./Workspace/sentiment/0616/food/fooddict2027.txt', 'r','utf-8') as f:
    for w in f.readlines():
        food.append(w.replace(' 5000 n\n',''))
with open('./Workspace/data/blog_perfect_cut.json', 'r') as f:
    ifoodie = json.load(f)