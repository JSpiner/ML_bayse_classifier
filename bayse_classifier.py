# -*- coding: utf-8 -*-

import pandas as pd
import json
import re
from konlpy.tag import Kkma
from konlpy.tag import Twitter
from konlpy.tag import Hannanum
from konlpy.tag import Mecab
from konlpy.utils import pprint
import math

all_words = 0
all_word = {}
def search(words, wordList):
    resCate1 = ""
    resCate2 = ""
    resCate3 = ""
    resCate4 = ""
    resCate5 = ""
    resCate6 = ""
    resCate7 = ""
    resCate8 = ""
    resCate9 = ""

    maxpt = []
    maxpt2 = []
    
    maxPoint = -99999
    maxPoint2 = 0
    for key1, cate1 in wordList.iteritems():
        for key2, cate2 in cate1.iteritems():
            for key3, cate3 in cate2.iteritems():
                
                point = 0.
                pt = []
                for word in words:
#                    if len(word)<3:
#                        continue
                    p = 0
                    c = 1
                    
                    if word in cate3:
                        catepoint = cate3[word]
                    else:
                        catepoint = 0
                        
#                    catepoint+=10
#                    catepoint = int(catepoint/10)
#                    catepoint*=10
                        
                    p = math.log( float(catepoint + 1) / (len(cate3) + all_words)  )
                    """
                    if word in cate3 :
#                        if cate3[word] > 0:
#                        p = -math.log(float(1) / (len(cate3) + len(words) ) )
#                        p = -math.log( float(cate3[word] ) / (len(cate3) + len(words) ) )
                       
                        if cate3[word] > 10:
                            p = 20 # len(cate3) / len(words) * math.log(cate3[word]) * 10
                            c+=1
                        else:
                            p = -math.log( float(1) / (len(cate3) + len(words) ) )
                    else:
                        p = 0
                        p = -math.log( len(words) * (len(cate3) + len(words)) )"""
                    p = round(p, 3)
                    point+=p
                    pt.append(p)

    #                        print word
#                point*= len(cate3) / 108

#                print "%s %s %f" % (key2 ,key3 , point)
                if point>maxPoint or maxPoint == -99999:
                    resCate7 = resCate4
                    resCate8 = resCate5
                    resCate9 = resCate6
                    
                    resCate4 = resCate1
                    resCate5 = resCate2
                    resCate6 = resCate3
            
                    resCate1 = key1
                    resCate2 = key2
                    resCate3 = key3
                    maxPoint2 = maxPoint
                    maxPoint = point
                    maxpt2 = maxpt
                    maxpt = pt
#    print "%s %s %s" % (resCate1, resCate2, resCate3)
    resCate = ";".join( [resCate1, resCate2, resCate3] )
    
#    if resCate in dropout_data:
#        percent = dropout_data[resCate]
#        rnd = 
    
    return resCate1, resCate2, resCate3, resCate4, resCate5, resCate6, resCate7, resCate8, resCate9, maxPoint, maxPoint2, maxpt, maxpt2
    
def check_correct(cate1, cate2, cate3, words):
    
    point = 0.
    pt = []
    for word in words:
#                    if len(word)<3:
#                        continue
        p = 0
        if word in wordList[cate1][cate2][cate3] :
#                        if cate3[word] > 0:
#                        p = -math.log(float(1) / (len(cate3) + len(words) ) )
#                        p = -math.log( float(cate3[word] ) / (len(cate3) + len(words) ) )
            if wordList[cate1][cate2][cate3][word] == 1000:
                p = 20#(cate3[word] - 3)*(cate3[word] - 3)
            elif wordList[cate1][cate2][cate3][word] > 10:
                p = wordList[cate1][cate2][cate3][word]
            elif wordList[cate1][cate2][cate3][word] > 50:
                p = 20
            elif wordList[cate1][cate2][cate3][word] > 10:
                p = 20
            else:
                p = -math.log( float(1) / (len(wordList[cate1][cate2][cate3]) + len(words) ) )
        else:
            p = 0
            p = -math.log( len(words) * (len(wordList[cate1][cate2][cate3]) + len(words)) )
        p = round(p, 3)
        point+=p
        pt.append(p)
    return pt
    
wordList = {}
test_data = {}

print "init konlpy"
#mecab = Mecab()
twitter = Twitter()
def split_knolpy(str):
    return twitter.morphs(str)

file = open('learn_data.txt', 'r')
data = file.read()
wordList = json.loads(data)
file.close()

file = open('test_data.txt', 'r')
data = file.read()
test_data = json.loads(data)
file.close()

file = open('dropout_data.txt', 'r')
data = file.read()
dropout_data = json.loads(data)
file.close()

filter = [u"즉시", u"할인", u"쿠폰", u"해외", u"포장", u"출고", u"무료", u"카드", u"[", u"]",
          u"배송", u"ㅁ", u"정품", u"박스",u"구매",u"대행",u"직구",
          u"세계",u"특허", u"4%", u"5%", u"당일", u"발송", u"판매", u"신한", u"KB국민", 
          u"(", u")", u"6%", u"10%", u"8%"]
#filter = []

print "done"

for key, value in wordList.iteritems():
    for key1, value1 in value.iteritems():
        for key2, value2 in value1.iteritems():
            for key3, value3 in value2.iteritems():
                if key3 in all_word:
                    all_word[key3]+=1
                else:
                    all_word[key3] = 1
                
    #            break
all_words = len(all_word)
sum = 0.
accur = 0.
cate_all_list = {}
cate_correct_list = {}
for key, value in test_data.iteritems():
    for key1, value1 in value.iteritems():
        for key2, value2 in value1.iteritems():
            count = 0
            category = key + ";" + key1 + ";" + key2
#            pprint (test_data[key][key1][key2])
#            pprint (test_data[key][key1])
            
    
            for key3 in test_data[key][key1][key2]:
                percent = 0.
                text = key3
                
#                    cate_correct_list[category] = 0
                    
                    
                for word in filter: 
                    text = text.replace(word, " ")    
                words = split_knolpy(text)
                
                for j in range(len(words)-1):
                    words.append( "".join([words[j], words[j+1]] ))

                for j in range(len(text)):
                    words.append(text[j:j+1])
                    
                
                cate1, cate2, cate3, cate4, cate5, cate6, cate7, cate8, cate9, point1, point2, pt, pt2 = search(words, wordList)
    
                sum+=1
         
                ans_cate = ";".join([cate1,cate2,cate3])
                if ans_cate in cate_all_list:
                    cate_all_list[ans_cate] += 1
                else:
                    cate_all_list[ans_cate] = 1
#                if cate4 == key and cate5 == key1 and cate6 == key2:
#                    accur+=1
#                elif cate7 == key and cate8 == key1 and cate9 == key2:
#                    accur+=1
                if cate1 == key and cate2 == key1 and cate3 == key2:
                    accur+=1
            
                else:
                    
                    if  ans_cate in cate_correct_list:
                        cate_correct_list[ans_cate] += 1
                    else:
                        cate_correct_list[ans_cate] = 1
                    print str(accur/sum*100) + "%"
                    print ";".join([key, key1, key2]) + " --> " + ";".join([cate1,cate2,cate3])
                    print key3
                    print 
                    """print "correct : %s %s %s" % (key, key1, key2)
                    print "wrong   : %s %s %s %f" % (cate1, cate2, cate3, point1)
                    print "wrong2  : %s %s %s %f" % (cate4, cate5, cate6, point2)
                    print "wrong3  : %s %s %s %f" % (cate7, cate8, cate9, point2)
    #                    pprint(words)
                    print text + " " + str(len(words))
                    print ';'.join(words)
                    print key3
                    print pt
                    print pt2
                    print check_correct(key, key1, key2, words)
                    print "" """
            
#                print ""
        
        
print str(accur/sum*100) + "%"



#
dropout_data = {}
for row in cate_correct_list:
    print row 
    print str(cate_correct_list[row]) + "/" + str(cate_all_list[row]) + " : " + str(float(cate_correct_list[row])/cate_all_list[row]*100)
    print
    dropout_data[row] = float(cate_correct_list[row])/cate_all_list[row]*100

    
jsontext = json.dumps(dropout_data)
file = open('dropout_data.txt','w')
file.write(jsontext)
file.close()





