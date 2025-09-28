import numpy as np
from typing import List, Tuple, Optional


def trend_slope_r2(ys) -> Tuple[float, float]:
    """
    对 ys 拟合直线 y = a + b x（x = 0,1,2,...）得到斜率 b 和 R² 值。
    若序列常数或方差为 0，则返回 slope = 0, r2 = 0。
    """
    ys = np.array(ys, dtype=float)
    n = len(ys)
    if n < 2:
        return 0.0, 0.0

    # x 是 0,1,2,...,n-1
    xs = np.arange(n, dtype=float)
    # 拟合线性回归：最小二乘法解
    # b = cov(x, y) / var(x), a = mean(y) - b * mean(x)
    x_mean = xs.mean()
    y_mean = ys.mean()
    # 计算协方差、方差
    cov_xy = np.sum((xs - x_mean) * (ys - y_mean))
    var_x = np.sum((xs - x_mean) ** 2)
    if var_x == 0:
        return 0.0, 0.0

    b = cov_xy / var_x
    a = y_mean - b * x_mean

    # 拟合值
    y_pred = a + b * xs
    # 计算 SSE, SST
    ss_res = np.sum((ys - y_pred) ** 2)
    ss_tot = np.sum((ys - y_mean) ** 2)
    # 避免除 0
    if ss_tot == 0:
        # 若 ys 完全常数（方差为 0），那就没有趋势可言
        return b, 0.0

    r2 = 1.0 - (ss_res / ss_tot)
    # 有可能 r2 为负（拟合比平均线还差）—你可以把它截断为 0
    if r2 < 0:
        r2 = 0.0

    return b, r2


def rolling_trend(
    prices: List[float], window: int = 22, step: int = 5
) -> List[Tuple[int, float, float]]:
    """
    对价格序列做滚动窗口拟合，返回 (window 起始索引, slope, r2) 列表。
    """
    n = len(prices)
    results = []
    for start in range(0, n - window + 1, step):
        win = prices[start : start + window]
        slope, r2 = trend_slope_r2(win)
        results.append((start, slope, r2))
    return results


def is_bloom_ascent(
    prices: List[float],
    window: int = 22,
    step: int = 5,
    how_long: int = 2,
    r2_threshold: float = 0.7,
    slope_threshold: Optional[float] = None,
    min_avg_r2: Optional[float] = None,
) -> bool:
    """
    判断是否出现连续 how_long 个窗口里有显著上升趋势。
    条件是：斜率 > 0（或 > slope_threshold），且 r2 >= r2_threshold。
    还可以加一些额外约束：如平均 r2 >= min_avg_r2。
    """
    trends = rolling_trend(prices, window, step)
    # 如果窗口数量不足 how_long，则直接返回 False
    if len(trends) < how_long:
        return False

    # 统计连续符合条件窗口
    count = 0
    # 也可以保存符合窗口的 r2 列表，用于后续平均判断
    passed_r2s = []
    for start_idx, slope, r2 in trends:
        ok_slope = (
            (slope > 0) if (slope_threshold is None) else (slope > slope_threshold)
        )
        ok_r2 = r2 >= r2_threshold
        if ok_slope and ok_r2:
            count += 1
            passed_r2s.append(r2)
            if count >= how_long:
                break
        else:
            count = 0
            passed_r2s = []
    if count < how_long:
        return False

    # 若用户指定了 min_avg_r2，进一步检查平均 r2 合格
    if min_avg_r2 is not None:
        avg_r2 = sum(passed_r2s[-how_long:]) / float(how_long)
        if avg_r2 < min_avg_r2:
            return False

    return True
