from core.stock_data_service import read_pd_from_db, trading_days
from model import Kronos, KronosTokenizer, KronosPredictor
from core.constaint import *
from matplotlib import pyplot as plt
from sql.session import session, engine
import pandas as pd
from sql.models import *
from datetime import datetime, date, timedelta
import os

tokenizer = KronosTokenizer.from_pretrained(TOKENIZER_PATH)
model = Kronos.from_pretrained(MODEL_PATH)

predictor = KronosPredictor(model, tokenizer, device=DEVICE, max_context=CONTEXT_LEN)


def plot_prediction(kline_df, pred_df, save_path):
    pred_df.index = kline_df.index[-pred_df.shape[0] :]
    sr_close = kline_df["close"]
    sr_pred_close = pred_df["close"]
    sr_close.name = "Ground Truth"
    sr_pred_close.name = "Prediction"

    sr_volume = kline_df["volume"]
    sr_pred_volume = pred_df["volume"]
    sr_volume.name = "Ground Truth"
    sr_pred_volume.name = "Prediction"

    close_df = pd.concat([sr_close, sr_pred_close], axis=1)
    volume_df = pd.concat([sr_volume, sr_pred_volume], axis=1)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

    ax1.plot(
        close_df["Ground Truth"], label="Ground Truth", color="blue", linewidth=1.5
    )
    ax1.plot(close_df["Prediction"], label="Prediction", color="red", linewidth=1.5)
    ax1.set_ylabel("Close Price", fontsize=14)
    ax1.legend(loc="lower left", fontsize=12)
    ax1.grid(True)

    ax2.plot(
        volume_df["Ground Truth"], label="Ground Truth", color="blue", linewidth=1.5
    )
    ax2.plot(volume_df["Prediction"], label="Prediction", color="red", linewidth=1.5)
    ax2.set_ylabel("Volume", fontsize=14)
    ax2.legend(loc="upper left", fontsize=12)
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    print(f"✅ 图片已保存至: {save_path}")
    plt.close(fig)


def predict_stock(code, code_name, predict_step: int, result_path: str = "result"):
    assert predict_step <= 180
    r = read_pd_from_db(code)
    recent_day = r.tail()["date"].iloc[-1]
    start_day = recent_day + timedelta(days=1)
    end_day = start_day + timedelta(days=800)
    x_timestamp = r["date"].iloc[-CONTEXT_LEN:]
    x_timestamp = pd.to_datetime(x_timestamp)
    y_timestamp = trading_days(str(start_day), str(end_day))[:predict_step]
    y_timestamp = pd.Series(y_timestamp)
    selected_data = r[-CONTEXT_LEN:]
    selected_data = selected_data[
        ["open", "high", "low", "close", "volume", "amount"]
    ].reset_index(drop=True)
    print(selected_data.tail())
    # Generate predictions
    pred_df = predictor.predict(
        df=selected_data,
        x_timestamp=x_timestamp,
        y_timestamp=y_timestamp,
        pred_len=len(y_timestamp),
        T=1.0,  # Temperature for sampling
        top_p=0.9,  # Nucleus sampling probability
        sample_count=1,  # Number of forecast paths to generate and average
    )
    print("Forecasted Data Head:")
    print(pred_df.head())
    all_df = pd.concat([selected_data, pred_df], axis=0, ignore_index=True)
    pred_df.reset_index(drop=True, inplace=True)
    if not os.path.exists(result_path):
        os.mkdir(result_path)
    plot_prediction(all_df, pred_df, save_path=f"./result_path/{code}_{code_name}.png")
    all_df.to_csv(f"./result_path/{code}_{code_name}_all.csv")
    pred_df.to_csv(f"./result_path/{code}_{code_name}_pred.csv")
    return all_df, pred_df
