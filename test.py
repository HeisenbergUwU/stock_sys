from core.kronos_service import predict_stock
from datetime import timedelta

# r = read_pd_from_db("sh.000001")
# print(r.tail()["date"].iloc[-1] + timedelta(days=1))
predict_stock("sh.000001", "-", 180)
