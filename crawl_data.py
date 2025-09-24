from tools.baostock_crawler import (
    get_a_stock_code,
    get_stock_data,
    get_trade_day,
    get_batch_stock_data,
)
import pandas as pd
from datetime import datetime, timedelta
import os
from tqdm import tqdm

today = datetime.now().date()
yesterday = today - timedelta(days=1)
# 一般用昨天的数据，当天数据不更新的。。 baostock


def get_year_trade_day():
    border_start = today
    border_end = today + timedelta(days=366)
    if os.path.exists("data") == False:
        os.mkdir("data")
    if os.path.exists(f"data/trade_days_{border_start.year}.csv") == True:
        print("Reading From Disk..")
        trade_days = pd.read_csv(f"data/trade_days_{border_start.year}.csv")
    else:
        print("Downloading From Baostock..")
        trade_days = get_trade_day(border_start, border_end, yesterday, False)
        trade_days.to_csv(f"data/trade_days_{border_start.year}.csv", index=False)
    print(trade_days.tail())
    return trade_days


def download_all_stock_data_today():
    # 获取A股代码列表
    if os.path.exists(f"data/{today}/stock_codes_{today}.csv") == True:
        print("Reading From Disk..")
        stock_codes = pd.read_csv(f"data/{today}/stock_codes_{today}.csv")
    else:
        print("Downloading From Baostock..")
        stock_codes = get_a_stock_code(day=str(yesterday), is_store=False)
        stock_codes.to_csv(f"data/{today}/stock_codes_{today}.csv", index=False)

    # 遍历股票代码获取数据
    """
            code tradeStatus   code_name
    0     sh.000001           1      上证综合指数
    1     sh.000002           1      上证A股指数
    """
    border_start = yesterday - timedelta(days=512)
    border_end = yesterday
    stockList = []
    for idx, data in tqdm(stock_codes.iterrows()):
        # 获取每只股票的历史数据
        stockList.append({"code": data["code"], "code_name": data["code_name"]})
    get_batch_stock_data(
        stockList, str(border_start), str(border_end), str(today), True
    )


# get_year_trade_day()
download_all_stock_data_today()
