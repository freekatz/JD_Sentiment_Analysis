#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   processing.py
@Desc    :
@Project :   JDComment_Spider
@Contact :   1uvu.zhang@gmail.com
@License :   (C)Copyright 2018-2020, 1UVU.COM
@WebSite :   1uvu.com
@Modify Time           @Author        @Version
------------           -------        --------
2020/12/03 12:47       1uvu           0.0.1
"""

import pandas as pd

from configs import *
from utils import *


def format_phone_name(full_name, sub) -> str:
    full_name = str(full_name)
    index = full_name.find(sub)  # 第一次出现的位置
    index2 = full_name.find(sub, index + 1)  # 第二次出现的位置
    index3 = full_name.find(sub, index2 + 1)  # 第三次出现的位置
    new_name = full_name[:index3].translate(str.maketrans('/ \\', '___'))
    return new_name


def drop(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates()  # 去重
    df['content'] = df['content'].fillna('99999')  # 将空值所在行填充为99999
    df['referenceName'] = df['referenceName'].fillna('99999')
    row_comment_index = df[df.content == '99999'].index.tolist()  # 找出评论空值所在行索引
    row_type_index = df[df.referenceName == '99999'].index.tolist()  # 找出商品名称所在行索引
    row_index = row_comment_index + row_type_index
    df["referenceName"] = df.apply(lambda x: format_phone_name(x['referenceName'], ' '), axis=1)
    df = df.drop(row_index)
    
    return df


def seg(df: pd.DataFrame) -> pd.DataFrame:
    content_words = []
    for c in df.content:
        content_words.append(seg_word(c))
    
    df["content"] = content_words
    return df.dropna()


def tag(df: pd.DataFrame) -> pd.DataFrame:
    tag = []
    for s in df["score"]:
        if good_tag[0] <= s <= good_tag[1]:
            tag.append(1)
        elif bad_tag[0] <= s <= bad_tag[1]:
            tag.append(0)
        else:
            tag.append(-1)
    
    df["tag"] = tag
    return df


def pipe(df: pd.DataFrame) -> pd.DataFrame:
    df = drop(df)
    df = seg(df)
    df = tag(df)
    df.to_csv(process_data_path, index=False, encoding="utf_8_sig")
    # df = pd.read_csv(process_data_path, encoding='utf-8')
    dataset_split(df, 0.8)
    return df


if __name__ == '__main__':
    df = pd.read_csv(crawl_data_path, encoding='utf-8')
    pipe(df)
