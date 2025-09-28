# DEV

```
sqlacodegen mysql+pymysql://root:?@fakenews.ddns.net:3306/stock > models.py
```

# baostock

每日最新数据更新时间：
当前交易日 17:30，完成日 K 线数据入库；
当前交易日 18:00，完成复权因子数据入库；
第二自然日 11:00，完成分钟 K 线数据入库；
第二自然日 1:30，完成前交易日“其它财务报告数据”入库；
周六 17:30，完成周线数据入库；

# PREDICT

结果保存在 prediction_result 中
