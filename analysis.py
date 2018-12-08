#! /usr/bin/python3.6
# -*-coding:utf-8 -*-

import jieba.analyse
import pymongo
from collections import Counter
import numpy as np
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import sys

import config

def analysis(db_name, collection_name):
    '''
    分析数据
    @param db_name mongo数据库名
    @param collection_name 集合名称
    @return 返回collections.Counter
    '''
    client = pymongo.MongoClient('localhost', 27017)
    mydb = client[db_name]
    jianshu = mydb[collection_name]

    #获取所有数据，返回的为一个迭代器
    results = jianshu.find()
    #计数器
    counter = Counter()

    #停用词表
    jieba.analyse.set_stop_words('./chinese_stop_words.txt')

    for result in results:
        text = result['text']
        tags = jieba.analyse.extract_tags(text, withWeight = True)
        #tags = jieba.analyse.extract_tags(text, topK = 100, withWeight = True)

        for item in tags:
            counter[item[0]] += item[1]

    return counter

def write_frequencies(counter, number, filename):
    '''
    把前number个高频词写入对应文件
    @param counter Counter计量器
    @param number 前number个高频词
    @filename 要写入的文件名
    '''
    fp = open(filename, 'w')
    index = 0

    for k,v in counter.most_common(number):
        if index > number:
            break
        fp.write('\'%s\', ' % k)
        #print(k, v)
        index += 1
    print('共%d高频词写入%s成功' % (number, filename))
    fp.close()

def word_cloud(words):
    '''
    生成词云
    '''
    img = Image.open('./timg.jpeg')
    img_array = np.array(img)

    wc = WordCloud(
            background_color = 'white',
            width = 1500,
            height = 1500,
            mask = img_array,
            font_path = './微软雅黑+Arial.ttf')

    #wc.generate_from_text(text)
    wc.generate_from_frequencies(words)
    plt.imshow(wc)
    plt.axis('off')
    plt.show()
    wc.to_file('./new.png')

if __name__ == '__main__':
    '''
    参数：1.word 分析并生成词云
          2.freq 高频词写入
    '''
    length = len(sys.argv)
    param = 'word'
    number = 100
    filename = 'frequent.txt'

    #获取数据
    if length > 1:
        param = sys.argv[1]
    
    if length > 2:
        number = int(sys.argv[2])

    if length > 3:
        filename = sys.argv[3]

    if param == 'word':
        counter = analysis('mydb', 'jianshu')
        word_cloud(counter)
    elif param == 'freq':
        counter = analysis('mydb', 'jianshu')
        write_frequencies(counter, number, filename)
    else:
        print('请输入正确的参数 word|(freq [number] [filename])')
