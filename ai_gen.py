from core.kronos_service import predict_stock
from datetime import timedelta
import os
from core.stock_data_service import get_stock_code
from tools.AllMix import sanitize_filename
all_stock_code = get_stock_code()
for stock_code in all_stock_code:
    result_path = "2025-09-24"
    stock_code.code_name = sanitize_filename(stock_code.code_name)
    if not os.path.exists(
        f"./{result_path}/{stock_code.code}_{stock_code.code_name}.png"
    ):
        predict_stock(stock_code.code, stock_code.code_name, 180, result_path)

# sh.600072_中船科技
