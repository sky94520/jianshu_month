#! /usr/bin/python3.6
# -*-coding:utf-8 -*-

import requests
import time
from lxml import etree
import pprint
from urllib.parse import urljoin
import csv

import config

headers = {
        'User-Agent' : config.get_random_user_agent(),
        }

base_url = 'https://www.jianshu.com/'

def get_monthly_info(url, params = None):
    '''
    获取对应页面的详细页面url
    @param url 主要链接
    '''
    response = requests.get(url, headers = headers, params = params)

    #print(response.url)
    #解析
    selector = etree.HTML(response.text)

    infos = selector.xpath('//ul[@class="note-list"]/li')
    for info in infos:
        #文章id
        note_id = info.xpath('./@data-note-id')[0]
        #文章名
        title = info.xpath('.//*[@class="title"]/text()')[0]
        #链接
        href = info.xpath('.//*[@class="title"]/@href')[0]

        yield {
            'note_id' : note_id,
            'title' : title,
            'url' : urljoin(base_url, href)
        }

def main():
    start_url = 'https://www.jianshu.com/trending/monthly?'

    seen_snote_ids = []
    #保存
    fp = open('month_urls.csv', 'w', encoding = 'utf-8')
    fieldnames = ['note_id', 'title', 'url']

    writer = csv.DictWriter(fp, fieldnames = fieldnames)
    #读取前几页
    for page in range(1, 7):
        params = {'seen_snote_ids[]' : seen_snote_ids, 'page' : page}

        if page > 3:
            params['utm_medium'] = 'index-banner-s'
            params['utm_source'] = 'desktop'

        print('正在爬取第%d页' % page)

        for data in get_monthly_info(start_url, params):
            writer.writerow(data)
            print('保存:', data['title'])
            seen_snote_ids.append(data['note_id'])
    #close
    fp.close()

if __name__ == '__main__':
    main()
