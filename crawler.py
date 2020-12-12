#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   crawler.py
@Desc    :
@Project :   JDComment_Spider
@Contact :   1uvu.zhang@gmail.com
@License :   (C)Copyright 2018-2020, 1UVU.COM
@WebSite :   1uvu.com
@Modify Time           @Author        @Version
------------           -------        --------
2020/12/03 12:46       1uvu           0.0.1
"""

import pandas as pd
import requests
import json
import copy
import time

from configs import *


def request_maker(url: str, payloads=None) -> dict:
    resp = requests.get(url, params=payloads, headers=headers)
    print("Current comment url is: ", resp.url)
    return json.loads(resp.text)


def data_getter(j: dict) -> list:
    cl = j["comments"]
    _cl = []
    for l in cl:
        _c = copy.deepcopy(comment_data)
        _c["id"] = l["id"]
        _c["content"] = l["content"]
        _c["score"] = l["score"]
        _c["referenceName"] = l["referenceName"]
        _c["referenceTime"] = l["referenceTime"]
        _cl.append(_c)
    
    return _cl


def pipe():
    cdf = pd.DataFrame(columns=comment_data.keys())
    for pid in product_ids:  # 1 遍历产品颜色
        time.sleep(3)
        for st in range(sort_range[0], sort_range[1]):  # 2 遍历排序方式
            for sc in range(score_range[0], sort_range[1]):  # 3 遍历评论分数
                payloads["productId"] = pid
                payloads["score"] = sc
                payloads["sortType"] = st
                payloads["page"] = 0
                j = request_maker(url, payloads)
                max_page = int(j['maxPage'])
                for p in range(start_page, max_page):  # 4 遍历页码
                    print(f"Current score is {sc}, sortType is {st}, page is {p}")
                    payloads["page"] = p
                    _j = request_maker(url, payloads)
                    cl = data_getter(_j)
                    for c in cl:
                        print("Comment: ", c)
                        cdf = cdf.append(c, ignore_index=True)
                        cdf.to_excel(crawl_data_path, index=False, encoding="utf-8")


if __name__ == "__main__":
    pipe()
