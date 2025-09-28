from core.kronos_service import *
from datetime import timedelta
import os
from core.stock_data_service import get_stock_code
from tools.AllMix import sanitize_filename
from datetime import date

STEP = 60
PATH_1 = date.today().strftime("%Y-%m-%d")
all_stock_code = get_stock_code()


def daily_predict():
    # daily K
    for stock_code in all_stock_code:
        result_path = f"./prediction_result/{PATH_1}#daily"
        if not os.path.exists(result_path):
            os.makedirs(result_path)
        stock_code.code_name = sanitize_filename(stock_code.code_name)
        if not os.path.exists(
            f"./{result_path}/{stock_code.code}_{stock_code.code_name}.png"
        ):
            all_df, pred_df = predict_stock(
                stock_code.code, stock_code.code_name, STEP, result_path, "d"
            )
            pred_df.to_csv(
                result_path + f"/{stock_code.code}_{stock_code.code_name}_pred.csv"
            )


def weekly_predict():
    # daily K
    for stock_code in all_stock_code:
        result_path = f"./prediction_result/{PATH_1}#weekly"
        if not os.path.exists(result_path):
            os.makedirs(result_path)
        stock_code.code_name = sanitize_filename(stock_code.code_name)
        if not os.path.exists(
            f"./{result_path}/{stock_code.code}_{stock_code.code_name}.png"
        ):
            all_df, pred_df = predict_stock(
                stock_code.code, stock_code.code_name, STEP, result_path, "w"
            )
            pred_df.to_csv(
                result_path + f"/{stock_code.code}_{stock_code.code_name}_pred.csv"
            )


def monthly_predict():
    # daily K
    for stock_code in all_stock_code:
        result_path = f"./prediction_result/{PATH_1}#monthly"
        if not os.path.exists(result_path):
            os.makedirs(result_path)
        stock_code.code_name = sanitize_filename(stock_code.code_name)
        if not os.path.exists(
            f"./{result_path}/{stock_code.code}_{stock_code.code_name}.png"
        ):
            all_df, pred_df = predict_stock(
                stock_code.code, stock_code.code_name, STEP, result_path, "m"
            )
            pred_df.to_csv(
                result_path + f"/{stock_code.code}_{stock_code.code_name}_pred.csv"
            )


def daily_predict_batch(batch_size: int = 16):
    # daily K
    result_path = f"./prediction_result/{PATH_1}#daily"
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    step = 0
    while True:
        if all_stock_code[step * batch_size : (step + 1) * batch_size]:
            codes = []
            codes_names = []
            for stock_code in all_stock_code[
                step * batch_size : (step + 1) * batch_size
            ]:
                codes.append(stock_code.code)
                codes_names.append(sanitize_filename(stock_code.code_name))
            predict_batch_stock(
                STEP, result_path, "d", codes=codes, code_names=codes_names
            )
        else:
            break


def weekly_predict_batch(batch_size: int = 16):
    result_path = f"./prediction_result/{PATH_1}#weekly"
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    step = 0
    while True:
        if all_stock_code[step * batch_size : (step + 1) * batch_size]:
            codes = []
            codes_names = []
            for stock_code in all_stock_code[
                step * batch_size : (step + 1) * batch_size
            ]:
                codes.append(stock_code.code)
                codes_names.append(sanitize_filename(stock_code.code_name))
            predict_batch_stock(
                STEP, result_path, "w", codes=codes, code_names=codes_names
            )
        else:
            break


def monthly_predict_batch(batch_size: int = 16):
    result_path = f"./prediction_result/{PATH_1}#monthly"
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    step = 0
    while True:
        if all_stock_code[step * batch_size : (step + 1) * batch_size]:
            codes = []
            codes_names = []
            for stock_code in all_stock_code[
                step * batch_size : (step + 1) * batch_size
            ]:
                codes.append(stock_code.code)
                codes_names.append(sanitize_filename(stock_code.code_name))
            predict_batch_stock(
                STEP, result_path, "m", codes=codes, code_names=codes_names
            )
        else:
            break
