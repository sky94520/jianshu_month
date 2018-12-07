#! /usr/bin/python3.6
# -*-coding:utf-8 -*-

from urllib.parse import urlsplit, parse_qs
import pprint

url = 'https://www.jianshu.com/trending/monthly?seen_snote_ids%5B%5D=37748501&seen_snote_ids%5B%5D=37776875&seen_snote_ids%5B%5D=37794473&seen_snote_ids%5B%5D=37197951&seen_snote_ids%5B%5D=36807878&seen_snote_ids%5B%5D=36463859&seen_snote_ids%5B%5D=36765004&seen_snote_ids%5B%5D=36341650&seen_snote_ids%5B%5D=36798485&seen_snote_ids%5B%5D=36883342&seen_snote_ids%5B%5D=36152995&seen_snote_ids%5B%5D=36404763&seen_snote_ids%5B%5D=36786520&seen_snote_ids%5B%5D=36560243&seen_snote_ids%5B%5D=36808340&seen_snote_ids%5B%5D=36891380&seen_snote_ids%5B%5D=35443912&seen_snote_ids%5B%5D=36673167&seen_snote_ids%5B%5D=36553581&seen_snote_ids%5B%5D=36647346&seen_snote_ids%5B%5D=37032895&seen_snote_ids%5B%5D=37786258&seen_snote_ids%5B%5D=36464755&seen_snote_ids%5B%5D=36688371&seen_snote_ids%5B%5D=37160818&seen_snote_ids%5B%5D=36457154&seen_snote_ids%5B%5D=36832954&seen_snote_ids%5B%5D=37248150&seen_snote_ids%5B%5D=30967754&seen_snote_ids%5B%5D=36322137&seen_snote_ids%5B%5D=36966999&seen_snote_ids%5B%5D=33293857&seen_snote_ids%5B%5D=36687303&seen_snote_ids%5B%5D=36883389&seen_snote_ids%5B%5D=36796011&seen_snote_ids%5B%5D=36964449&seen_snote_ids%5B%5D=36949243&seen_snote_ids%5B%5D=36709893&seen_snote_ids%5B%5D=36565806&seen_snote_ids%5B%5D=36839961&page=3'

result = urlsplit(url)
#得到参数
queries = result.query
#解析参数
params = parse_qs(queries)
#pprint.pprint(params)
print(params)
