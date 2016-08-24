# -*- coding: utf-8 -*-

import pandas as pd
from konlpy.tag import Kkma
from konlpy.tag import Hannanum
from konlpy.utils import pprint
from konlpy.tag import Mecab
from konlpy.tag import Twitter
import re
import json




filter = [u"즉시", u"할인", u"쿠폰", u"해외", u"포장", u"출고", u"무료", u"카드", u"[", u"]",
          u"배송", u"ㅁ", u"정품", u"박스",u"구매",u"대행",u"직구",
          u"세계",u"특허", u"4%", u"5%", u"당일", u"발송", u"판매", u"신한", u"KB국민", 
          u"(", u")", u"6%", u"10%", u"8%"]

filter = []
wordList = {}

print "init konlpy"
#komoran = Komoran()
twitter = Twitter() 
#mecab = Mecab()
def split_knolpy(str):
    return twitter.morphs(str)

def check_duplicate(cate1, cate2, cate3, name):
    
    for key1, row1 in wordList.iteritems():
        for key2, row2 in row1.iteritems():
            for key3, row3 in row2.iteritems():
                for key4, count in row3.iteritems():
                    if cate1 == key1 and cate2 == key2 and cate3 == key3:
#                            wordList[key1][key2][key3][key4]2
                            continue
                    if key4 == name:
                        wordList[key1][key2][key3][key4]=1
                        return True
    return False

train_df = pd.read_pickle("../soma_goods_train.df")

#print train_df
print type(train_df)

i = 0
count = 0
print "start learning"
test_data = {}
for index, row in train_df.iterrows():
#    print str(i) + " " +str(index) + " " +row['cate1'] + " " + row['cate2'] + " " + row['cate3'] + "//" +row['name']
    
#    if i== 10000 :
#        break
    i= i+1
    cate1 = row['cate1']
    cate2 = row['cate2']
    cate3 = row['cate3']
    name = row['name'] 
#    print name
#    print name
#    print ";".join(split_knolpy(name))
#    print "=="
    words = split_knolpy(name)#mecab.nouns(name)#re.split('[ /_]', name)#kkma.nouns(name)
#    pprint (words)
    if(i % 100 == 0):
        print "learning " + str(i) + " / 10000"
    
    if i % 10  < 2:
        
        while True:
            if cate1 in test_data :
                if cate2 in test_data[cate1] :
                    if cate3 in test_data[cate1][cate2] :
                        test_data[cate1][cate2][cate3][name] = 1
                        break
                    else:
                        test_data[cate1][cate2][cate3] = {}
                else:
                    test_data[cate1][cate2] = {}
            else:
                test_data[cate1] = {}
        continue
#        print str(i) + " " +str(index) + " " +row['cate1'] + " " + row['cate2'] + " " + row['cate3'] + "//" +row['name']
        
    for word in filter: 
        name = name.replace(word, " ")    
    words = split_knolpy(name)#re.split('[ /_]', name)#kkma.nouns(name)
#    for n in range(5):
#    words.extend( split_knolpy(cate1))#re.split('[ /_]', cate1) )
#    for n in range(10):
#    words.extend( split_knolpy(cate2))#re.split('[ /_]', cate2) )
#    for n in range(1):
    words.extend( split_knolpy(cate3))#re.split('[ /_]', cate3) )
    words.extend( re.split('[ /_;]', name) )
#    words.append( (cate3))#re.split('[ /_]', cate3) )
    
    for j in range(len(words)-1):
        words.append( "".join([words[j], words[j+1]] ))
    
    for j in range(len(name)):
        words.append(name[j:j+1])
    
    for word in words:
                
        if len(word)<2:
            continue
        
        while True:
            if cate1 in wordList :
                if cate2 in wordList[cate1] :
                    if cate3 in wordList[cate1][cate2] :
                        if word in wordList[cate1][cate2][cate3] :
                            
#                            if check_duplicate(cate1, cate2, cate3, word) == True:
#                                wordList[cate1][cate2][cate3][word] = 1
#                            else:
#                                if wordList[cate1][cate2][cate3][word] == 0 :
#                                    wordList[cate1][cate2][cate3][word] = 1
#                                else :
                            wordList[cate1][cate2][cate3][word]+=1
                            break
                        else :
                            wordList[cate1][cate2][cate3][word] = 0
                    else:
                        wordList[cate1][cate2][cate3] = {}
                else:
                    wordList[cate1][cate2] = {}
            else:
                wordList[cate1] = {}
#    if index==230346:
#        break
#        wordList[cate1][cate2][cate3][cate3.replace(" ","")] = len(wordList[cate1][cate2][cate3]) / 10
#        wordList[cate1][cate2][cate3][cate2.replace(" ","")] = len(wordList[cate1][cate2][cate3]) / 15
#        wordList[cate1][cate2][cate3][cate1.replace(" ","")] = len(wordList[cate1][cate2][cate3]) / 20
    """
    for word in split_knolpy( (row['cate2'])):
        if len(word)<2:
            continue
        
        while True:
            if cate1 in wordList :
                if cate2 in wordList[cate1] :
                    if cate3 in wordList[cate1][cate2] :
                        if word in wordList[cate1][cate2][cate3] :
                            
                            wordList[cate1][cate2][cate3][word]=1000
                                                       
                            break
                        else :
                            wordList[cate1][cate2][cate3][word] = 0
                    else:
                        wordList[cate1][cate2][cate3] = {}
                else:
                    wordList[cate1][cate2] = {}
            else:
                wordList[cate1] = {}
    for word in split_knolpy( (row['cate3'])):
        if len(word)<2:
            continue
        
        while True:
            if cate1 in wordList :
                if cate2 in wordList[cate1] :
                    if cate3 in wordList[cate1][cate2] :
                        if word in wordList[cate1][cate2][cate3] :
                            
                            wordList[cate1][cate2][cate3][word]=1000
                                                       
                            break
                        else :
                            wordList[cate1][cate2][cate3][word] = 0
                    else:
                        wordList[cate1][cate2][cate3] = {}
                else:
                    wordList[cate1][cate2] = {}
            else:
                wordList[cate1] = {}
        """
        
    
jsontext = json.dumps(wordList)
jsontext2 = json.dumps(test_data)
print "start save"
file = open('learn_data.txt','w')
file.write(jsontext)
file.close()

file = open('test_data.txt','w')
file.write(jsontext2)
file.close()
        
print "done"
