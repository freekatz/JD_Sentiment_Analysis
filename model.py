#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   model.py
@Desc    :
@Project :   JD_Seniment_Analysis
@Contact :   1uvu.zhang@gmail.com
@License :   (C)Copyright 2018-2020, 1UVU.COM
@WebSite :   1uvu.com
@Modify Time           @Author        @Version
------------           -------        --------
2020/12/04 11:07       1uvu           0.0.1
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_validate
from sklearn.metrics.scorer import make_scorer
from sklearn import metrics
import pandas as pd
import numpy as np
import time

from utils import *


def pipe(clf):
    # 读入测试集、训练集
    train_df = pd.read_csv(train_data_path).dropna()
    test_df = pd.read_csv(test_data_path).dropna()
    
    x_train = train_df["content"]
    y_train = train_df["tag"]
    x_test = test_df["content"]
    y_test = test_df["tag"]
    
    # 查看数据集分布
    y_train = list(y_train)
    y_test = list(y_test)
    print("训练集差评数据数量：", y_train.count(0), "训练集好评数据数量：",  y_train.count(1))
    print("测试集差评数据数量：", y_test.count(0), "测试集好评数据数量：", y_test.count(1))

    # 使用TF-IDF进行文本转向量处理
    tv = TfidfVectorizer(max_features=6000, ngram_range=(1, 2))
    tv.fit(x_train)
    
    # 训练模型
    clf.fit(tv.transform(x_train), y_train)
    
    # 交叉验证
    cv(tv.transform(x_train), y_train, clf)
    
    # 测试集验证
    simple_score(tv.transform(x_test), y_test, clf)
    
    # 输入例子测试
    t_good = "手机款式新颖，运行速度快，的确有优势。包装安全，快递及时，服务态度很好。比较了好几个购物平台，还是更加信任京东自营商城，所以第一次在京东买手机，非常满意。 "
    t_bad = "摄像头有白点，外观还不够完美，已经申请换机了，售后服务态度也不好"

    print(t_good, "\n判断结果为: ", simple_test(clf, tv.transform(pd.Series([seg_word(t_good)]))))
    print(t_bad, "\n判断结果为: ", simple_test(clf, tv.transform(pd.Series([seg_word(t_bad)]))))
    return clf


def cv(x_train, y_train, clf):
    scoring = {
        'precision_macro': 'precision_macro',
        'recall_macro': make_scorer(metrics.recall_score, average='macro'),
        'roc_auc_macro': make_scorer(metrics.roc_auc_score, average='macro'),
        'f1_macro': make_scorer(metrics.f1_score, average="macro"),
        'accuracy': make_scorer(metrics.accuracy_score),
    }
    cv_results = cross_validate(clf, x_train, y_train, scoring=scoring,
                                n_jobs=4, cv=10, return_train_score=False, )
    for key in cv_results.keys():
        print(f"{key}:\t{np.mean(cv_results[key])}")


def simple_score(x_text, y_test, clf):
    start = time.time()
    y_pred = clf.predict(x_text)
    end = time.time()
    print("fit_time:	%.9f" % (end - start))
    s1 = metrics.precision_score(y_test, y_pred)
    s2 = metrics.recall_score(y_test, y_pred)
    s3 = metrics.roc_auc_score(y_test, y_pred)
    s4 = metrics.f1_score(y_test, y_pred)
    s5 = metrics.accuracy_score(y_test, y_pred)
    s6 = metrics.confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = s6.ravel()
    print(f"test_precision_macro: {s1}")
    print(f"test_recall_macro: {s2}")
    print(f"test_roc_auc_macro: {s3}")
    print(f"test_f1_macro: {s4}")
    print(f"test_accuracy: {s5}")
    print(f"test_confusion_matrix: {s6}")
    print("tn, fp, fn, tp = ", (tn, fp, fn, tp))


def simple_test(clf, test):
    prob = clf.predict_proba(test)
    print("预测结果详情：", prob[0])
    if prob[0][0] > 0.5:
        res = "bad"
    else:
        res = "good"
    return res


if __name__ == '__main__':
    # clf = MultinomialNB()  # 朴素贝叶斯
    clf = LogisticRegression()  # 逻辑回归
    # clf = DecisionTreeClassifier()  # 决策树
    # clf = RandomForestClassifier(n_estimators=30)  # 随机森林
    pipe(clf)
