#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   utils.py
@Desc    :
@Project :   JD_Seniment_Analysis
@Contact :   1uvu.zhang@gmail.com
@License :   (C)Copyright 2018-2020, 1UVU.COM
@WebSite :   1uvu.com
@Modify Time           @Author        @Version
------------           -------        --------
2020/12/04 9:51       1uvu           0.0.1
"""
from collections import Counter
import pandas as pd
import codecs
import jieba
import re

from configs import *

from configs import *


def dataset_split(df: pd.DataFrame, frac=0.8):
    # 划分数据集为训练集，测试集
    good = df[df["tag"] == 0]
    common = df[df["tag"] == -1]
    bad = df[df["tag"] == 1]
    origin_data = pd.concat([good, bad], axis=0, join="outer")
    train_data = origin_data.sample(frac=frac, random_state=0, axis=0)
    test_data = origin_data.drop(labels=train_data.axes[0])
    print(len(good) + len(bad))
    print(len(train_data) + len(test_data))
    train_data.to_csv(train_data_path, index=False, encoding="utf_8_sig")
    test_data.to_csv(test_data_path, index=False, encoding="utf_8_sig")


def filter_words_by_re(words: list) -> list:
    rtn = []
    for word in words:
        flag = False
        for p in patterns:
            if re.search(p, word) is None:
                flag = True
            else:
                flag = False
                break
        if flag:
            rtn.append(word)
    
    return rtn


def seg_word(sentence: str) -> str:
    """使用jieba对文档分词"""
    seg_list = jieba.cut(sentence)
    seg_result = []
    for w in seg_list:
        seg_result.append(w)
    # 读取停用词文件
    stopwords = set()
    fr = codecs.open(stopwords_path, 'r', 'utf-8')
    for word in fr:
        stopwords.add(word.strip())
    fr.close()
    # 去除停用词
    return seg_tag.join(filter_words_by_re(list(filter(lambda x: x not in stopwords, seg_result))))


def word_rank(df: pd.DataFrame) -> dict:
    df = df.dropna()
    rank_list = []
    for content in df["content"]:
        rank_list += re.split(seg_tag, content)
    return Counter(rank_list)


def time_rank(df: pd.DataFrame) -> dict:
    df = df.dropna()
    time_list = []
    for time in df["referenceTime"]:
        time_list.append(re.search(r" (\d+):", time).groups()[0])
    return Counter(time_list)


def name_rank(df: pd.DataFrame) -> (dict, dict):
    df = df.dropna()
    size_list = []
    color_list = []
    for name in df["referenceName"]:
        size_list.append(re.search(r" (\d+)GB", name).groups()[0])
        color_list.append(re.search(r"GB (.+) ", name).groups()[0])
    return Counter(size_list), Counter(color_list)