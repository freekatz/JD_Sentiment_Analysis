# JD_Sentiment_Analysis
一个简单的京东商品评论爬虫、处理、可视化、情感分析与模型评估实践。

分为四大模块：爬虫、预处理、分析和可视化、建模，其余还包括配置和工具模块。

-    charts目录：存放数据可视化输出结果：词云图、折线图、饼状图
-   data目录：存放各种数据：原始数据、预处理数据、训练集和测试集
-   res：存放资源文件，stopwords.txt存放停用词
-   configs.py：存放所有相关的静态配置
-   crawler.py：爬虫模块
-   model.py：建模与评估模块
-   pipeline.py：主控制模块
-   plotter.py：数据可视化模块
-   processing.py：数据预处理模块
-   utils.py：存放所有相关工具函数
-   requirements.txt：存放python库依赖版本信息