from pathlib import Path

import numpy as np

from weather_climate_data_analysis_using_python.valueobject.wcdaup import (
    SeaSurfaceTemperatureData,
)


def get_sea_surface_temperature_data() -> SeaSurfaceTemperatureData:
    """
    2.2.3 海面水温ファイルを入力する
    2.3.1 経度(longitude)と緯度(latitude)
    3.4.1 データセットの読み込み

    Returns:
        SeaSurfaceTemperatureData: The sea surface temperature data.

    Raises:
        FileNotFoundError: If the data file is not found.

    Examples:
        >>> data = get_sea_surface_temperature_data()
    """
    file_path = Path("output") / "sst_OISST.npz"
    sst_dataset = np.load(file_path)

    return SeaSurfaceTemperatureData(
        sst=sst_dataset["sst"],
        lon2=sst_dataset["lon2"],
        lat2=sst_dataset["lat2"],
        y=sst_dataset["y"],
        m=sst_dataset["m"],
    )
