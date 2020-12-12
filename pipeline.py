#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   pipeline.py
@Desc    :
@Project :   JD_Seniment_Analysis
@Contact :   1uvu.zhang@gmail.com
@License :   (C)Copyright 2018-2020, 1UVU.COM
@WebSite :   1uvu.com
@Modify Time           @Author        @Version
------------           -------        --------
2020/12/04 11:06       1uvu           0.0.1
"""
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import pandas as pd

from crawler import pipe as crawl_pipe
from processing import pipe as process_pipe
from plotter import pipe as plot_pipe
from model import pipe as model_pipe
from configs import *

if __name__ == '__main__':
    # 1 数据获取
    crawl_pipe()
    
    # 2 数据预处理
    df = pd.read_csv(crawl_data_path, encoding='utf-8')
    process_pipe(df)
    
    # 3 数据可视化
    pdf = pd.read_csv(process_data_path, encoding="utf-8")
    plot_pipe(pdf)

    # 4 数据建模
    # clf = MultinomialNB()  # 朴素贝叶斯
    clf = LogisticRegression()  # 逻辑回归
    # clf = DecisionTreeClassifier()  # 决策树
    # clf = RandomForestClassifier(n_estimators=30)  # 随机森林
    model_pipe(clf)
