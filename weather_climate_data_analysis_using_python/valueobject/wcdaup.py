from dataclasses import dataclass

import numpy


@dataclass
class SeaSurfaceTemperature:
    sst: numpy.ndarray
    lon2: numpy.ndarray
    lat2: numpy.ndarray
    y: numpy.ndarray
    m: numpy.ndarray
