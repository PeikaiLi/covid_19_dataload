# 2019新型冠状病毒疫情时间序列数据仓库

本项目 based on https://github.com/BlankerL/DXY-COVID-19-Data/releases/tag/2022.09.09README.en.md)

增添了一些新的功能，数据来源仍为[丁香园](https://3g.dxy.cn/newh5/view/pneumonia)。

请阅读源项目，再读本项目



## 数据说明
1. 部分数据存在重复统计的情况，如[Issue #21](https://github.com/BlankerL/DXY-COVID-19-Data/issues/21)中所述，河南省部分市级数据存在"南阳（含邓州）"及"邓州"两条数据，因此在求和时"邓州"的数据会被重复计算一次。

### 数据异常
1. 目前发现浙江省/湖北省部分时间序列数据存在数据异常，可能的原因是丁香园数据为人工录入，某些数据可能录入错误，比如某一次爬虫获取的浙江省治愈人数为537人，数分钟后被修改回正常人数。
2. [Issue #110](https://github.com/BlankerL/DXY-COVID-19-Data/issues/110)中反馈丁香园3月15日更新的吉林省长春市和吉林市的确诊人数颠倒。为了保证数据完整，我没有修改这部分数据，请大家在使用的时候手动调整。



