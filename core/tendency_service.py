import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


def trend_slope_r2(prices):
    X = np.arange(len(prices)).reshape(-1, 1)
    y = np.array(prices)
    model = LinearRegression().fit(X, y)
    slope = model.coef_[0]
    r2 = r2_score(y, model.predict(X))
    return slope, r2


def rolling_trend(prices, window=22, step=5):
    """
    计算滚动窗口内的趋势斜率和R²值。
    :param prices: 股票价格列表或数组
    :param window: 滑动窗口大小，默认为22（约一个月的交易日）
    :param step: 滑动步长，默认为5
    :return: 包含每个窗口起始位置、斜率和R²
    """
    results = []
    for start in range(0, len(prices) - window + 1, step):
        win = prices[start : start + window]
        s, r = trend_slope_r2(win)
        results.append((start, s, r))
    return results


def is_bloom_ascent(prices, window=22, step=5, how_long: int = 1):
    results = rolling_trend(prices, window, step)
    count = 0
    for window, slope, r2 in results:
        if slope > 0 and r2 > 0.7:
            count += 1
        else:
            count = 0
    if count >= how_long:
        return True
    else:
        return False
