# -*- coding: utf-8 -*-
import json
import jieba
import os
import re
import codecs
import binascii
import time

jieba.set_dictionary('/Users/fan/anaconda/bin/Workspace/sentiment/0616/big/jieba356726.txt')
jieba.load_userdict('/Users/fan/anaconda/bin/Workspace/sentiment/0616/big/cute.txt')
jieba.load_userdict('/Users/fan/anaconda/bin/Workspace/sentiment/0616/big/jieba356726.txt')
jieba.load_userdict('/Users/fan/anaconda/bin/Workspace/sentiment/0616/food/fooddict2027.txt')
jieba.load_userdict('/Users/fan/anaconda/bin/Workspace/sentiment/0616/menu/menu50806_new.txt')
jieba.load_userdict('/Users/fan/anaconda/bin/Workspace/sentiment/0616/sentiment/negativewords.txt')
jieba.load_userdict('/Users/fan/anaconda/bin/Workspace/sentiment/0616/sentiment/positivewords.txt')
jieba.load_userdict('/Users/fan/anaconda/bin/Workspace/sentiment/0616/sentiment/negative.txt')
jieba.load_userdict('/Users/fan/anaconda/bin/Workspace/sentiment/0616/sentiment/more.txt')
jieba.load_userdict('/Users/fan/anaconda/bin/Workspace/sentiment/0616/sentiment/question.txt')
jieba.load_userdict('/Users/fan/anaconda/bin/Workspace/sentiment/0616/stop/stopword2292.txt')
jieba.enable_parallel(6)

def deleteBadWords(StrIn):
    Str_BadWords = u'延伸閱讀|連絡方式|電話預約|電話|營業時間|週一|週二|週三|週四|週五|週六|週日|周一|周二|周三|周四|周五|周六|\
                    |周日|假日|公休|平日|地址|粉絲團|星期|禮拜|時間限制|您或許對這些文章有興趣|造訪日期|全年無休|最後點餐|營業|AM|PM|上一篇|下一篇|\
                    |分享此文|您可能喜歡的文章|懶人包|臉書|Facebook|facebook|FB|fb|全世界便宜住宿看這兒|下載愛食記App隨時觀看|按個讚啦|喜歡我的分享嗎|\
                    |瘋台灣民宿網|官方網站|瀏覽人次|最新消息|餐廳名稱|消費時間|無圖文版|網誌|Postedonby|新鮮關注回聲|Christabelle的藝想世界部落格由製作|\
                    |也許對這些文章也有興趣|發表迴響|電子郵件|必要欄位標記|電子郵件|個人網站|輸入圖片顯示文字好證明你不是機器人|站內搜尋分類|最新動態|\
                    |並不會被公開|你的位址 |迴響名稱|用餐日期|留言|載入中|文章文章|粉絲頁|發表|每人平均價位|按個讚|推薦你閱讀|Instagram|instagram|\
                    |美食地圖|版權所有|網友回應|歡迎加入|標籤|著作權聲明|非經授權|不得轉載'
    strClean = re.sub(Str_BadWords,'',StrIn)
    return strClean

def EnglishFullToHalf(StrIn):
    def transform(ele):
        alphabetInt = int(repr(ele.group('number'))[4:8],16)
        transAlphabeInt = alphabetInt - 65248
        return binascii.a2b_hex(hex(transAlphabeInt)[2:4])
    pattern = re.sub(u'(?P<number>[\uff21-\uff3a\uff41-\uff5a])', transform, StrIn)
    return pattern

def setBreakPoint(StrIn):
    pattern = u'[,，.。~～!！?？；]+'
    result = re.sub(pattern, ' ', StrIn)
    return result

def retain_English_Chinese_Arabic_numerals(StrIn):
    Str_English_Chinese = u'([^ 0-9a-zA-Zａ-ｚＡ-Ｚ\u4E00-\u9FCC]+)'
    #Str_English_Chinese = u'([^a-z^A-Z^ａ-ｚ^Ａ-Ｚ^^0-9^０-９^\u3105-\u3129^\u4E00-\u9FCC]+)'
    #\u3105-\u3129為所有注音符號
    #\u4E00-\u9FCC為所有中文
    strClean = re.sub(Str_English_Chinese,'',StrIn)
    return strClean

def removeSentimentInAds(StrIn):
    pattern = u'.*(喜歡|推薦|喜愛).{0,6}(文章|本文|介紹)'
    def sub(match):
        string = match.group(0)
        type1 = match.group(1) if match.group(1) else ''
        r = string.replace(type1,'')
        return r
    result = re.sub(pattern, sub, StrIn)
    return result

with open('/Users/fan/anaconda/bin/Workspace/ifoodieBlogDic20160619Update5PixnetSmallEnglish.json', 'r') as f:
    ifoodie = json.load(f)

stopwords = []
with codecs.open('/Users/fan/anaconda/bin/Workspace/sentiment/0616/stop/stopword2292.txt', 'r', 'utf-8') as f:
    for w in f.readlines():
        stopwords.append(w.split()[0])
sentiment = []
with codecs.open('/Users/fan/anaconda/bin/expand/negativeWordMerge.txt', 'r', 'utf-8') as f:
    for w in f.readlines():
        sentiment.append(w.split()[0])
with codecs.open('/Users/fan/anaconda/bin/expand/positiveWordMerge.txt', 'r', 'utf-8') as f:
    for w in f.readlines():
        sentiment.append(w.split()[0])
with codecs.open('/Users/fan/anaconda/bin/expand/inverseWordMerge.txt', 'r', 'utf-8') as f:
    for w in f.readlines():
        sentiment.append(w.split()[0])
with codecs.open('/Users/fan/anaconda/bin/expand/degreeWordMerge.txt', 'r', 'utf-8') as f:
    for w in f.readlines():
        sentiment.append(w.split()[0])
final = []
for w in stopwords:
    if w not in sentiment:
        final.append(w)

for ele in ifoodie:
    art = deleteBadWords(ifoodie[ele]['article'])
    art = EnglishFullToHalf(art)
    art = setBreakPoint(art).split()
    art_cut = [list(jieba.cut(sentence)) for sentence in art]
    article = []
    for s_cut in art_cut:
        temp = retain_English_Chinese_Arabic_numerals(' '.join(s_cut))
        print temp
        s_result = [w for w in temp.split() if w not in final]
        article.append(s_result)
    ifoodie[ele]['article'] = article
with open('/Users/fan/anaconda/bin/Workspace/data/blog_perfect_cut.json', 'w') as f:
    json.dump(ifoodie, f)