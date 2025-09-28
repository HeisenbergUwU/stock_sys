import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
from core.stock_data_service import *

update_stock_data_weekly_by_baostock_api()
