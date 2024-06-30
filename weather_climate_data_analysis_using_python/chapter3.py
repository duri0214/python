import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import datetime
import netCDF4 as nc4
import pandas as pd
from matplotlib.colors import Normalize


def convert_jma_to_df() -> pd.DataFrame:
    """
    https://www.data.jma.go.jp/gmd/risk/obsdl/index.php
    地点: 東京
    項目:
      データの種類: 月別値
      項目: 月平均気温
    対象期間: 連続した期間で表示する - 1875/6(22.3℃) - 2020/9(27.7℃)

    1. `data.csv` を `jma_temps_data.csv` にリネームして `input` フォルダに保存
    """
    df = pd.read_csv(
        "input/jma_temps_data.csv", skiprows=[0, 1, 2, 4], encoding="shift_jis"
    )
    df[["年", "月"]] = df["年月"].str.split("/", expand=True)
    df["年"] = df["年"].astype(int)
    df["月"] = df["月"].astype(int)
    df = df.rename(columns={"平均気温(℃)": "平均気温"})
    df = df[["年", "月", "平均気温"]]

    plt.plot(df["平均気温"])
    plt.title("Average Temperatures")
    plt.xlabel("Time")
    plt.ylabel("Temperature")
    plt.show()
    return df


def calc_climatic_values(temp_data: pd.DataFrame):
    label_month = np.arange(1, 13, 1)
    work_clim = np.zeros(12)

    for target_month in range(1, 13):
        work_clim[target_month - 1] = temp_data[temp_data["月"] == target_month][
            "平均気温"
        ].mean(skipna=True)

    plt.plot(label_month, work_clim)
    plt.xticks(label_month)
    plt.show()


if __name__ == "__main__":
    calc_climatic_values(convert_jma_to_df())
