from typing import Dict
from collections import namedtuple

DataPoint = namedtuple('Datapoint', 'epoch, x, y, z')
NullDataPoint = DataPoint(epoch=0, x=0, y=0, z=0)


def dict_to_data_point(row: Dict):
    return DataPoint(epoch=float(row['epoch']), x=float(row['x']), y=float(row['y']), z=float(row['z']))
