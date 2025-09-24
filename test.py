from core.kronos_service import predict_stock
from datetime import timedelta

from core.stock_data_service import get_stock_code

all_stock_code = get_stock_code()
for stock_code in all_stock_code:
    predict_stock(stock_code.code, stock_code.code_name, 180, "2025-09-24")
