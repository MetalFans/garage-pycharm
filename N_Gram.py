
# coding: utf-8
import operator
import codecs

class N_Gram():

    textList = []


    def __init__(self):
        pass


    def cutSentence(self, filePath, longTerms):
        cutlist = '<>/:：;；,、＂’，.。！？｢\"\'\\\n\r《》“”!@#$%^&*()'.decode('utf-8')
        text = codecs.open(filePath, 'r', 'utf-8')
        sentence = ''
        
        for lines in text.readlines():
            lines = lines.strip()
            
            for keyword in longTerms:
                lines = ''.join(lines.split(keyword))
                
            for word in lines:
                if word not in cutlist:
                    sentence += word
                else:
                    self.textList.append(sentence)
                    sentence = ''
        return self.textList


    def ngram(self, textList, termsNum, minFreq):
        words = []
        words_freq_dict = {}
        result = []
        
        for strList in textList:
            for length in range(0, len(strList) - (termsNum - 1)):
                words.append(strList[length:length + termsNum])
        
        for word in words:
            if word not in words_freq_dict:
                words_freq_dict[word] = words.count(word)
        
        words_freq_list = sorted(words_freq_dict.items(), key = operator.itemgetter(1), reverse = True)
        
        for word in words_freq_list:
            if word[1] >= minFreq:
                result.append(word)
        
        return result


    def longTermPriority(self, filePath, maxTermLength, minFreq):
        longTerms = []
        longTermsFreq = []
        
        for termsNum in range(maxTermLength, 1, -1):
            self.cutSentence(filePath, longTerms)
            self.ngram(self.textList, termsNum, minFreq)
        
        for word_freq in self.ngram(self.textList, termsNum, minFreq):
            longTerms.append(word_freq[0])
            longTermsFreq.append(word_freq)
        
        return longTermsFreq



