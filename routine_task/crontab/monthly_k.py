import os
import sys
from pathlib import Path

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
from core.stock_data_service import *

update_stock_data_monthly_by_baostock_api()
