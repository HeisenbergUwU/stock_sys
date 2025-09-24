import time
import holidays
from pandas.tseries.offsets import CustomBusinessDay
import pandas as pd
from datetime import datetime, timedelta, date
from sqlalchemy.dialects.mysql import insert
from sql.models import *
from sql.session import session, engine
from glob import glob
import os
from tqdm import tqdm
from tools.baostock_crawler import get_stock_data
import baostock as bs
import numpy as np


def trading_days(start_day: str, end_day: str):
    cn_holidays = holidays.China(years=[2025, 2026, 2027, 2028, 2029, 2030])
    cbd = CustomBusinessDay(holidays=list(cn_holidays))
    approx_trading_days = pd.date_range(start_day, end_day, freq=cbd)
    return approx_trading_days


def cal_days(offset_days: int):
    now_day = date.today()
    offset_days = now_day + timedelta(days=offset_days)
    return now_day.strftime("%Y-%m-%d"), offset_days.strftime("%Y-%m-%d")


def cal_trading_days(offset_days: int):
    now_day = date.today()
    offset_days = now_day + timedelta(days=offset_days)
    return trading_days(now_day.strftime("%Y-%m-%d"), offset_days.strftime("%Y-%m-%d"))


def is_exponent_by_rules(
    code: str, volume: int, amount: float, pe_ttm: float, pb_mrq: float
) -> bool:
    if code.startswith(("sh.000", "sz.399", "^", ".IX", "IDX", "INDX")):
        return True
    if code in {"sh.000001", "sz.399001", "^GSPC", "^DJI", "^IXIC", "^HSI"}:
        return True
    financials_zero = (
        (pe_ttm is None or pe_ttm == 0)
        and (pb_mrq is None or pb_mrq == 0)
        and (amount == 0 or amount is None)
    )
    if financials_zero:
        return True
    if volume == 0:
        return True
    return False


def is_exponent_by_id(code: str) -> bool:
    if code.startswith(("sh.000", "sz.399", "^", ".IX", "IDX", "INDX")):
        return True
    if code in {"sh.000001", "sz.399001", "^GSPC", "^DJI", "^IXIC", "^HSI"}:
        return True
    return False


def update_stock_code(is_store=True):
    from crawl_data import get_a_stock_code
    import os
    from datetime import datetime, timedelta

    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    if os.path.exists(f"data/{today}/stock_codes_{today}.csv") == True:
        print("Reading From Disk..")
        stock_codes = pd.read_csv(f"data/{today}/stock_codes_{today}.csv")
    else:
        print("Downloading From Baostock..")
        stock_codes = get_a_stock_code(day=str(yesterday), is_store=False)
        if os.path.exists("data") == False:
            os.mkdir("data")
        if os.path.exists(f"data/{today}") == False:
            os.mkdir(f"data/{today}")
        if is_store:
            stock_codes.to_csv(f"data/{today}/stock_codes_{today}.csv", index=False)
        # sql
        function_local_session = session()
        for idx, data in stock_codes.iterrows():
            stock_codes = StockCodeMap(
                code=data["code"],
                code_name=data["code_name"],
                trade_status=data["tradeStatus"],
                is_exponent=1 if is_exponent_by_id(data["code"]) else 0,
            )
            function_local_session.merge(stock_codes)
        function_local_session.commit()
        function_local_session.close_all()

    return stock_codes


def update_stock_data_from_csv(
    csv_path: str = f"./data/{date.today()}/stock_data_*.csv",
):
    paths = glob(csv_path)
    for path in tqdm(paths):
        print(f"Reading {path}")
        df = pd.read_csv(path)
        df.fillna(0, inplace=True)  # 确实数据写0
        function_local_session = session()
        stock_datas_list = []
        for idx, data in df.iterrows():
            stock_data = {
                "date": data["date"],
                "code": data["code"],
                "open": data["open"],
                "high": data["high"],
                "low": data["low"],
                "close": data["close"],
                "preclose": data["preclose"],
                "volume": data["volume"],
                "amount": data["amount"],
                "adjustflag": data["adjustflag"],
                "turn": data["turn"],
                "tradestatus": data["tradestatus"],
                "pctChg": data["pctChg"],
                "peTTM": data["peTTM"],
                "pbMRQ": data["pbMRQ"],
                "psTTM": data["psTTM"],
                "pcfNcfTTM": data["pcfNcfTTM"],
                "isST": data["isST"],
            }
            stock_datas_list.append(stock_data)
        stmt = insert(StockData).values(stock_datas_list)
        upsert_stmt = stmt.on_duplicate_key_update(
            date=stmt.inserted.date,
            open=stmt.inserted.open,
            high=stmt.inserted.high,
            low=stmt.inserted.low,
            close=stmt.inserted.close,
            preclose=stmt.inserted.preclose,
            volume=stmt.inserted.volume,
            amount=stmt.inserted.amount,
            adjustflag=stmt.inserted.adjustflag,
            turn=stmt.inserted.turn,
            tradestatus=stmt.inserted.tradestatus,
            pctChg=stmt.inserted.pctChg,
            peTTM=stmt.inserted.peTTM,
            pbMRQ=stmt.inserted.pbMRQ,
            psTTM=stmt.inserted.psTTM,
            pcfNcfTTM=stmt.inserted.pcfNcfTTM,
            isST=stmt.inserted.isST,
        )
        function_local_session.execute(upsert_stmt)
        function_local_session.commit()
        function_local_session.close_all()
        
def _clean_value(value, default=0):
    """将空字符串转为 None，或指定默认值"""
    if value == '' or value is None:
        return default  # 可设为 None 或 0，根据字段语义决定
    return value

def update_stock_data_daily_by_baostock_api():
    lg = bs.login()
    try:
        with session() as db:
            stock_code_maps = db.query(StockCodeMap).all()
            for stock_code_map in tqdm(stock_code_maps):
                sd = (
                    db.query(StockData)
                    .filter(StockData.code == stock_code_map.code)
                    .order_by(StockData.date.desc())
                    .first()
                )
                start_time = sd.date.strftime("%Y-%m-%d")
                rs = bs.query_history_k_data_plus(
                    stock_code_map.code,
                    "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
                    start_date=start_time,
                    end_date=str(date.today()),
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
                result = result.replace('', np.nan)
                result.fillna(0, inplace=True)
                print(stock_code_map.code, stock_code_map.code_name)
                stock_datas_list = []
                for idx, data in result.iterrows():
                    stock_data = {
                        "date": data["date"],
                        "code": data["code"],
                        "open": data["open"],
                        "high": data["high"],
                        "low": data["low"],
                        "close": data["close"],
                        "preclose": data["preclose"],
                        "volume": data["volume"],
                        "amount": data["amount"],
                        "adjustflag": data["adjustflag"],
                        "turn": data["turn"],
                        "tradestatus": data["tradestatus"],
                        "pctChg": data["pctChg"],
                        "peTTM": data["peTTM"],
                        "pbMRQ": data["pbMRQ"],
                        "psTTM": data["psTTM"],
                        "pcfNcfTTM": data["pcfNcfTTM"],
                        "isST": data["isST"],
                    }
                    stock_datas_list.append(stock_data)
                stmt = insert(StockData).values(stock_datas_list)
                upsert_stmt = stmt.on_duplicate_key_update(
                    date=stmt.inserted.date,
                    open=stmt.inserted.open,
                    high=stmt.inserted.high,
                    low=stmt.inserted.low,
                    close=stmt.inserted.close,
                    preclose=stmt.inserted.preclose,
                    volume=stmt.inserted.volume,
                    amount=stmt.inserted.amount,
                    adjustflag=stmt.inserted.adjustflag,
                    turn=stmt.inserted.turn,
                    tradestatus=stmt.inserted.tradestatus,
                    pctChg=stmt.inserted.pctChg,
                    peTTM=stmt.inserted.peTTM,
                    pbMRQ=stmt.inserted.pbMRQ,
                    psTTM=stmt.inserted.psTTM,
                    pcfNcfTTM=stmt.inserted.pcfNcfTTM,
                    isST=stmt.inserted.isST,
                )
                db.execute(upsert_stmt)
                db.commit()
                time.sleep(0.5)
    finally:
        bs.logout()


def get_stock_code():
    with session() as db:
        stock_code_maps = db.query(StockCodeMap).all()
    return stock_code_maps


def read_pd_from_db(stock_code: str):
    """_summary_

    Args:
        stock_code (str): sh.000001

    Returns:
        _type_: _description_
    """
    query = f"""SELECT 
        id,
        date,
        code,
        open,
        high,
        low,
        close,
        preclose,
        volume,
        amount,
        adjustflag,
        turn,
        tradestatus,
        pctChg,
        peTTM,
        pbMRQ,
        psTTM,
        pcfNcfTTM,
        isST
    FROM stock_data
    WHERE code = '{stock_code}'
    ORDER BY date ASC;"""
    df = pd.read_sql(query, engine)
    # df["date"] = pd.to_datetime(df["date"], unit="unix")
    df.reset_index(drop=True, inplace=True)
    return df
