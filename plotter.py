#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   plotter.py
@Desc    :
@Project :   JDComment_Spider
@Contact :   1uvu.zhang@gmail.com
@License :   (C)Copyright 2018-2020, 1UVU.COM
@WebSite :   1uvu.com
@Modify Time           @Author        @Version
------------           -------        --------
2020/12/03 12:47       1uvu           0.0.1
"""
import copy

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import wordcloud

from configs import *
from utils import *


# 0. 基础信息：总数，score 平均值
def base(cdf):
    sum = len(cdf["id"])
    mean = np.mean(cdf["score"])
    print(f"评论总数：{sum}，评论分数平均值：{mean}")


# 1. score 饼图
def pie(cdf):
    score = list(cdf["score"])
    score_set = set(score)
    score_list = [0] * len(score_set)
    for s in score_set:
        print("评论分数 ", s, " 的数量为：", score.count(s))
        score_list[s - 1] = score.count(s)
    score_series = pd.Series(score_list, index=["score: " + str(l) for l in score_set], name="")
    score_series.plot.pie(autopct='%.2f%%')
    plt.rcParams['figure.dpi'] = 400
    plt.rcParams['savefig.dpi'] = 400
    plt.tight_layout()
    plt.savefig(plot_target_path + "/pie.png")


# 2. 词云
def cloud(pdf):
    # style define
    w = wordcloud.WordCloud(
        width=1000, height=700,
        background_color='white',
        font_path='msyh.ttc'
    )
    _rank = word_rank(pdf)
    
    w.generate_from_frequencies(_rank)
    w.to_file(plot_target_path + "/cloud.png")


# 3. 购买时间折线：24小时
def line(pdf):
    rank = time_rank(pdf)
    print(rank)
    time_series = pd.Series(rank, index=rank.keys(), name="")[::-1]
    
    time_series.plot(marker='o', color='r')
    x_str = ["{}h".format(i) for i in np.arange(0, 23, 2)]
    plt.xticks(np.arange(0, 23, 2), x_str)
    plt.rcParams['figure.dpi'] = 400
    plt.rcParams['savefig.dpi'] = 400
    plt.tight_layout()
    plt.savefig(plot_target_path + "/line.png")


def pipe(pdf):
    base(pdf)
    pie(pdf)
    cloud(pdf)
    line(pdf)


if __name__ == '__main__':
    pdf = pd.read_csv(process_data_path, encoding="utf-8")
    pipe(pdf)
