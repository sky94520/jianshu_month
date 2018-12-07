#! /usr/bin/python3.6
# -*-coding:utf-8 -*-

import requests
from lxml import etree
import csv
import json
import pprint
import logging
import pymongo
from multiprocessing import Pool

import config

logging.basicConfig(level=logging.WARNING,#控制台打印的日志级别
                    filename='new.log',
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )

#写入文件
client = pymongo.MongoClient('localhost', 27017)
mydb = client['mydb']
jianshu = mydb['jianshu']

def get_info_of_note(li):
    '''
    @param li 文章id 文章标题 文章链接
    @return 
    '''
    note_id, title, url = li[0], li[1], li[2]

    print('打开链接：', url, title)
    #打开页面
    headers = {'User-Agent': config.get_random_user_agent()}
    response = requests.get(url, headers = headers)

    #记录一些出问题的链接
    if response.status_code != 200:
        logging.warning("%s打开错误%d" % (url, response.status_code))

    selector = etree.HTML(response.text)
    #文章list
    texts = selector.xpath('//div[@class="show-content-free"]/p/text()')

    data = {
        'title': title,
        'text': '\n'.join(texts),
    }
    #为什么不加锁？
    jianshu.insert_one(data)

def get_comment_of_note(li):
    '''
    @param li 文章id 文章标题 文章链接
    @return 
    '''
    note_id, title, url = li[0], li[1], li[2]
    url = 'https://www.jianshu.com/notes/{}/comments?'.format(note_id)
    params = {
        'comment_id' : '',
        'author_only' : 'false',
        'since_id' : 0,
        'max_id' : '1586510606000',
        'order_by' : 'desc',
        'page': 1,
    }
    #打开页面
    headers = {'User-Agent': config.get_random_user_agent()}
    response = requests.get(url, headers = headers, params = params)

    pprint.pprint(response.text)


if __name__ == '__main__':
    fp = open('month_urls.csv', 'r', encoding = 'utf-8')
    reader = csv.reader(fp)

    pool = Pool(processes = 4)
    pool.map(get_info_of_note, reader)
