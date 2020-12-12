#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   configs.py
@Desc    :
@Project :   JDComment_Spider
@Contact :   1uvu.zhang@gmail.com
@License :   (C)Copyright 2018-2020, 1UVU.COM
@WebSite :   1uvu.com
@Modify Time           @Author        @Version
------------           -------        --------
2020/12/03 12:46       1uvu           0.0.1
"""
from fake_useragent import UserAgent

ua = UserAgent()
#  通过调整下面的参数控制爬虫过程
product_ids = ['100016034400', '100009077475', '100016034358', '100016034374', '100016034356']
score_range = (3, 5 + 1)  # tobe format [1, 5]
sort_range = (1, 5 + 1)  # tobe format [1, 5]
start_page = 35  # tobe format [...]

url = "https://club.jd.com/comment/productPageComments.action"
payloads = {
    "productId": product_ids[0],
    "score": 1,
    "sortType": 5,
    "page": 0,
    "pageSize": 10
}
referer = "https://item.jd.com/100009077475.html#comment"
headers = {
    'Accept': '*/*',
    "User-Agent": ua.random,
    'Referer': referer
}
comment_data = {
    "id": "",  # 用户 id
    "score": "",  # 评价分数
    "referenceName": "",  # 商品名称
    "referenceTime": "",  # 购买时间
    "content": "",  # 评论内容
}

data_target_path = "./data"
crawl_data_path = data_target_path + "/crawl.csv"
process_data_path = data_target_path + "/process.csv"
train_data_path = data_target_path + "/train.csv"
test_data_path = data_target_path + "/test.csv"
stopwords_path = "./res/stopwords.txt"
plot_target_path = "./charts"

patterns = [
    r"\d+",
    r"[A-Z|a-z]+",
    r"[年|月|日| |\n|\r|]+",
]

seg_tag = " "

good_tag = [4, 5]
common_tag = [3]
bad_tag = [1, 2]
