from pathlib import Path

import numpy as np

from weather_climate_data_analysis_using_python.valueobject.wcdaup import (
    SeaSurfaceTemperature,
)


def get_sea_surface_temperature_data() -> SeaSurfaceTemperature:
    """
    2.2.3 海面水温ファイルを入力する
    2.3.1 経度(longitude 0～360)と緯度(latitude 90～-90)
      経度は東経0～180度、西経0～180度 でぜんぶで360要素(ただし、lon2は東に向かって0～360で定義される)
      緯度は北緯0～90度、南緯0～90度、で全部で180要素(ただし、lat2は南緯が-90～0で定義される)
      lon2, lat2 は360行180列の行列
    """
    file_path = Path("output") / "sst_OISST.npz"
    sst_dataset = np.load(file_path)

    return SeaSurfaceTemperature(
        sst=sst_dataset["sst"],
        lon2=sst_dataset["lon2"],
        lat2=sst_dataset["lat2"],
        y=sst_dataset["y"],
        m=sst_dataset["m"],
    )
