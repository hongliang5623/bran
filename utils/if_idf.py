# -*- coding:utf-8-*-
import jieba
import jieba.analyse

file_path = 'G:\\Datas\\idf\\test.txt'
f = open(file_path, 'r')
texts = f.readlines()
num_text = 0
text_content = ''.join(texts)
keywords = jieba.analyse.extract_tags(
        text_content, topK=20, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'), withFlag=True)
keyword_result = []
for keyword in keywords:
    (word, flag) = keyword[0]
    weight = keyword[1]
    keyword_result.append((word, weight, flag))
keyword_result.sort(key=lambda key: key[1], reverse=True)
for word, weight, flag in keyword_result:
    print word, weight, flag