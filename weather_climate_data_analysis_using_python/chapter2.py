import os
from pathlib import Path

import numpy as np
import datetime
import netCDF4 as nc4
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize

import util

LAND = 0


def convert_nc_to_ncz():
    """
    本の 2.2.2(p.24) で「これ使え」的な加工済みファイルがあったけど、1次ソース（米国海洋大気庁）から作成する処理を書き起こした
    ※米国海洋大気庁 のデータはファイルダウンロード式であるので事前に手に入れておく（READMEを参照）
    """
    # B.4.2 p.164
    work_dir = Path("input")
    os.makedirs(work_dir, exist_ok=True)
    file_path = work_dir / "sst.mnmean.nc"
    sst_data = nc4.Dataset(file_path, "r")
    sst = sst_data.variables["sst"][:].transpose(2, 1, 0).astype(float)
    [imt, jmt, tmt] = sst.shape
    print(imt, jmt, tmt)  # 東西方向, 南北方向, 時間方向

    # B.4.3 lon and lat
    lon = sst_data.variables["lon"][:]
    lat = sst_data.variables["lat"][:]
    # vector to matrix
    [x_grid, y_grid] = np.meshgrid(lon, lat)
    lon2 = x_grid.T.astype(float)
    lat2 = y_grid.T.astype(float)

    # B.4.4 year and month
    # 本当は `ncdump -h sst.mnmean.nc` でヘッダを見て、基準日が1800年1月1日かをチェックしないといけないけど本のとおりにするので省略
    y = np.zeros(tmt)
    m = np.zeros(tmt)
    date_offset = datetime.datetime(1800, 1, 1)
    time = sst_data.variables["time"][:]
    for tt in range(0, tmt):
        time_data = date_offset + datetime.timedelta(days=time[tt])
        y[tt] = time_data.year
        m[tt] = time_data.month

    # B.4.5 insert nan for land
    file_path = work_dir / "lsmask.nc"
    mask_data = nc4.Dataset(file_path, "r")
    mask = mask_data.variables["mask"][:]
    mask = np.squeeze(mask).T  # 3 dim(1x180x360) to 2 dim(180x360) and trans
    for tt in range(0, tmt):
        sst_tmp = np.squeeze(sst[:, :, tt])
        sst_tmp[mask == LAND] = np.nan
        sst[:, :, tt] = sst_tmp

    # B.4.6 extract the period
    period_mask = (1982 <= y) & (y <= 2019)
    sst = sst[:, :, period_mask]
    m = m[period_mask]
    y = y[period_mask]
    [imt, jmt, tmt] = sst.shape
    print(imt, jmt, tmt)

    # B.5
    work_dir = Path("output")
    os.makedirs(work_dir, exist_ok=True)
    file_path = work_dir / "sst_OISST.npz"
    if os.path.isfile(file_path):
        os.remove(file_path)
    np.savez(file_path, sst=sst, lon2=lon2, lat2=lat2, y=y, m=m)


def draw_the_sea_surface_temperature_for_a_given_month():
    input_data = util.get_sea_surface_temperature_data()

    # 2.3.3 海面水温(SST) p.30
    # 3次元配列であるsstには360[lon]x180[lat]の各格子点における456ヶ月分の月平均海面水温が、単位℃で収録されている
    # 陸の気温はnanで潰されている
    print(input_data.sst[:, :, 0])  # 1982年1月

    # 2.4 ある月の海面水温を描画する（エルニーニョ現象があった1997年12月の海面気温）
    draw_year = 1997
    draw_month = 12
    vmin = -5  # カラーバーの下限
    vmax = 35  # カラーバーの上限
    vint = 5  # カラーバーの間隔
    color_map = plt.get_cmap("seismic")  # 深い青から深い赤に向かうカラーバーを指定
    cs = plt.contour(
        input_data.lon2,
        input_data.lat2,
        np.squeeze(
            input_data.sst[
                :, :, (input_data.y == draw_year) * (input_data.m == draw_month)
            ]
        ),  # squeeze is 360x180x1 to 360x180
        cmap=color_map,
        norm=Normalize(vmin=vmin, vmax=vmax),
        levels=np.arange(vmin, vmax + vint, vint),
        extend="both",
    )
    plt.colorbar(cs)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.xlim(0, 360)
    plt.ylim(-90, 90)
    plt.title(f"{draw_year}/{draw_month}")
    plt.show()


if __name__ == "__main__":
    # convert_nc_to_ncz()
    util.get_sea_surface_temperature_data()
    draw_the_sea_surface_temperature_for_a_given_month()
