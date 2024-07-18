from dataclasses import dataclass

import numpy


@dataclass
class SeaSurfaceTemperatureData:
    """
    Class representing sea surface temperature data.

    Attributes:
        sst (numpy.ndarray): Sea surface temperature data.
        lon2 (numpy.ndarray): 経度は東経0～180度、西経0～180度 でぜんぶで360要素(ただし、lon2は東に向かって0～360で定義される)
        lat2 (numpy.ndarray): 緯度は北緯0～90度、南緯0～90度、で全部で180要素(ただし、lat2は南緯が-90～0で定義される)
        y (numpy.ndarray): Years.
        m (numpy.ndarray): Months.
    """

    sst: numpy.ndarray
    lon2: numpy.ndarray
    lat2: numpy.ndarray
    y: numpy.ndarray
    m: numpy.ndarray
