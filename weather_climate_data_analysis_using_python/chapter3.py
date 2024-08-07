import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import datetime
import netCDF4 as nc4
import pandas as pd
from matplotlib.colors import Normalize

from weather_climate_data_analysis_using_python import util


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
    """
    3.3.2 気候値を計算する
    @param temp_data:
    """
    label_month = np.arange(1, 13, 1)
    work_clim = np.zeros(12)

    for target_month in range(1, 13):
        work_clim[target_month - 1] = temp_data[temp_data["月"] == target_month][
            "平均気温"
        ].mean(skipna=True)

    plt.plot(label_month, work_clim)
    plt.xticks(label_month)
    plt.show()


def draw_monthly_climate_values_of_sea_surface_temperature_distribution():
    """
    海面水温分布の月次気候値を描画
    3.4.1 データセットの読み込み
    3.4.2 海面水温気候値を計算 p.41
    """
    input_data = util.get_sea_surface_temperature_data()
    [imt, jmt, tmt] = input_data.sst.shape
    sst_clim = np.zeros((imt, jmt, 12))
    # TODO: calc_climatic_values を見てリファクタリングする
    for mm in range(1, 13):
        # 1次元目（経度）,2次元目（緯度）の方向には手をつけない
        # 　 =>「配列の要素全部」という意味でコロンを置く
        # 3次元目（時間の方向）について, 東京の気温の例と同様に
        # sstのうちmがmmに等しい成分のみ取り出し
        # 平均を取って時間ステップmm-1番目に代入
        sst_clim[:, :, mm - 1] = np.mean(input_data.sst[:, :, input_data.m == mm], 2)
    savefile = "output/sstc_OISST.npz"
    np.savez(savefile, sst_clim=sst_clim, lon2=input_data.lon2, lat2=input_data.lat2)

    # vminはカラーバーの下限, vmaxはカラーバーの上限
    # vintはカラーバーの間隔
    vmin = -5
    vmax = 35
    vint = 5

    # 1月から12月までについて順番に描画
    for mm in range(1, 13):
        cm = plt.get_cmap("seismic")
        cs = plt.contourf(
            input_data.lon2,
            input_data.lat2,
            sst_clim[:, :, mm - 1],
            cmap=cm,
            norm=Normalize(vmin=vmin, vmax=vmax),
            levels=np.arange(vmin, vmax + vint, vint),
            extend="both",
        )
        plt.colorbar(cs)
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        clim_title = "month = " + str(mm)
        plt.title(clim_title)
        plt.xlim(0, 360)
        plt.ylim(-90, 90)
        plt.show()


if __name__ == "__main__":
    calc_climatic_values(convert_jma_to_df())
    draw_monthly_climate_values_of_sea_surface_temperature_distribution()
