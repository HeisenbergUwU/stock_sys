# TEST
```
sqlacodegen mysql+pymysql://root:?@fakenews.ddns.net:3306/stock > models.py
```

# baostock
每日最新数据更新时间：
当前交易日17:30，完成日K线数据入库；
当前交易日18:00，完成复权因子数据入库；
第二自然日11:00，完成分钟K线数据入库；
第二自然日1:30，完成前交易日“其它财务报告数据”入库；
周六17:30，完成周线数据入库；