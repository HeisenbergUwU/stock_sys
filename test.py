from core.tendency_service import is_bloom_ascent
from glob import glob
import pandas as pd
import re
import shutil
import os

result_path = "2025-09-24"
good_result = "goot_result"
pred_csv_paths = glob(f"./{result_path}/*_pred.csv")

if not os.path.exists(f"{good_result}"):
    os.mkdir(good_result)


for path in pred_csv_paths:
    data = pd.read_csv(path)
    close = data["close"]
    r = is_bloom_ascent(close)
    if r:
        # 正则表达式提取股票代码和名称
        match = re.search(r".?([a-z]{2}\.\d{6})_(.*?)_pred\.csv", path)
        if match:
            # 抛弃异常
            try:
                stock_code = match.group(1)
                stock_name = match.group(2)
                print(f"股票代码：{stock_code}")
                print(f"股票名称：{stock_name}")
                with open(f"{good_result}/good_stock.txt", "a+", encoding="utf8") as f:
                    f.write(f"{stock_code} - {stock_name}\n")
                shutil.copy(
                    f"./{result_path}/{stock_code}_{stock_name}.png",
                    f"./{good_result}/{stock_code}_{stock_name}.png",
                )
            except:
                pass
        else:
            print("未能提取股票信息")
