from threading import Thread
import time
import baostock as bs
import pandas as pd
import os
from tqdm import tqdm

INTERVAL = 0.5


def get_a_stock_code(day: str, is_store: bool):
    """
    获取某一天的所有A股股票代码
    :param day: 交易日
    :param is_store: 是否存储为csv文件

                code tradeStatus   code_name
    0     sh.000001           1      上证综合指数
    1     sh.000002           1      上证A股指数
    2     sh.000003           1      上证B股指数
    3     sh.000004           1     上证工业类指数
    4     sh.000005           1     上证商业类指数
    ...         ...         ...         ...
    5641  sz.399994           1  中证信息安全主题指数
    5642  sz.399995           1    中证基建工程指数
    5643  sz.399996           1    中证智能家居指数
    5644  sz.399997           1      中证白酒指数
    5645  sz.399998           1      中证煤炭指数

    [5646 rows x 3 columns]
    """
    lg = bs.login()
    rs = bs.query_all_stock(day=day)  # 传入一个交易日
    data_list = []
    while (rs.error_code == "0") & rs.next():
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    bs.logout()
    if is_store:
        if os.path.exists("data") == False:
            os.mkdir("data")
        if os.path.exists(f"data/{day}") == False:
            os.mkdir(f"data/{day}")
        result.to_csv(f"data/{day}/stock_codes_{day}.csv", index=False)
    return result


def get_stock_data(
    code: str, code_name: str, start_date: str, end_date: str, day: str, is_store: bool
):
    """
    获取某只股票的日K线数据
    :param code: 股票代码
    :param code_name: 股票名称
    :param start_date: 开始日期
    :param end_date: 结束日期
    :param day: 交易日 -- 用来创建文件件用的
    :param is_store: 是否存储为csv文件
    
    login success!
            date       code    open    high     low   close preclose    volume  \
    0  2024-01-02  sh.600478  4.9100  4.9300  4.8500  4.8600   4.9200  11095250   
    1  2024-01-03  sh.600478  4.8600  4.8900  4.7800  4.8300   4.8600   9052131   
    2  2024-01-04  sh.600478  4.8400  4.8500  4.7300  4.7600   4.8300   9006522   
    3  2024-01-05  sh.600478  4.8000  4.8900  4.6800  4.7100   4.7600  12500400   
    4  2024-01-08  sh.600478  4.6800  4.7500  4.5800  4.5900   4.7100  11177021   

            amount adjustflag      turn tradestatus     pctChg       peTTM  \
    0  54199994.0000          3  0.666200           1  -1.219500  226.481968   
    1  43735917.2300          3  0.543500           1  -0.617300  225.083931   
    2  42916444.4300          3  0.540800           1  -1.449300  221.821845   
    3  59882216.0000          3  0.750500           1  -1.050400  219.491784   
    4  51996227.2300          3  0.671100           1  -2.547800  213.899636   

        pbMRQ     psTTM   pcfNcfTTM isST  
    0  2.872826  2.079518  -27.444899    0  
    1  2.855092  2.066681  -27.275486    0  
    2  2.813714  2.036729  -26.880189    0  
    3  2.784158  2.015335  -26.597834    0  
    4  2.713224  1.963989  -25.920182    0  
    logout success!
    """
    lg = bs.login()
    rs = bs.query_history_k_data_plus(
        code,
        "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
        start_date=start_date,
        end_date=end_date,
        frequency="d",
        adjustflag="3",
    )
    data_list = []
    if not rs:
        print(f"Error in get_stock_data: {rs.error_msg}")
        return pd.DataFrame()
    while (rs.error_code == "0") & rs.next():
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    bs.logout()
    if is_store:
        if os.path.exists("data") == False:
            os.mkdir("data")
        if os.path.exists(f"data/{day}") == False:
            os.mkdir(f"data/{day}")
        result.to_csv(
            f"data/{day}/stock_data_{code}_{code_name}_{start_date}_{end_date}.csv",
            index=False,
        )
    return result


def get_batch_stock_data(
    stockList: list, start_date: str, end_date: str, day: str, is_store: bool
):
    lg = bs.login()
    try:
        for data in tqdm(stockList):
            code = data["code"]
            code_name = data["code_name"]
            rs = bs.query_history_k_data_plus(
                code,
                "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
                start_date=start_date,
                end_date=end_date,
                frequency="d",
                adjustflag="3",
            )
            data_list = []
            if not rs:
                print(f"Error in get_stock_data: {rs.error_msg}")
                return pd.DataFrame()
            while (rs.error_code == "0") & rs.next():
                data_list.append(rs.get_row_data())
            result = pd.DataFrame(data_list, columns=rs.fields)
            if is_store:
                if os.path.exists("data") == False:
                    os.mkdir("data")
                if os.path.exists(f"data/{day}") == False:
                    os.mkdir(f"data/{day}")
                result.to_csv(
                    f"data/{day}/stock_data_{code}_{code_name}_{start_date}_{end_date}.csv",
                    index=False,
                )
            print(code_name)
            time.sleep(INTERVAL)  # 防止限流
    except Exception as e:
        print(f"Error in get_batch_stock_data: {e}")
    finally:
        bs.logout()


def get_trade_day(start_date: str, end_date: str, day: str, is_store: bool):
    """
    获取指定时间段内的交易日历
    :param start_date: 开始日期
    :param end_date: 结束日期
    :param is_store: 是否存储为csv文件
    """
    lg = bs.login()
    result = None
    try:
        rs = bs.query_trade_dates(start_date=start_date, end_date=end_date)
        data_list = []
        while (rs.error_code == "0") & rs.next():
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)

        if is_store:
            if os.path.exists("data") == False:
                os.mkdir("data")
            if os.path.exists(f"data/{day}") == False:
                os.mkdir(f"data/{day}")
            result.to_csv(
                f"data/{day}/trade_dates_{start_date}_{end_date}.csv", index=False
            )
    finally:
        bs.logout()
    return result
