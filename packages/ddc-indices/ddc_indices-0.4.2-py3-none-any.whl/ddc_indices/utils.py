
import numpy as np
import pandas as pd
import xarray as xr

from enum import Enum
from typing import Tuple, Union, Optional, NewType


TimeRangeType = NewType('TimeRangeType',
                        Tuple[Union[str, pd.Timestamp],
                              Union[str, pd.Timestamp]])

BboxType = NewType('BboxType',
                   Tuple[Union[str, int, float], Union[str, int, float],
                         Union[str, int, float], Union[str, int, float]])


class Bbox:
    """"Class for bounding box represented by four number.

    Args:
        minx (Union[str, int, float]): Minimum coordinate in x direction.
        miny (Union[str, int, float]): Minimum coordinate in y direction.
        maxx (Union[str, int, float]): Maximum coordinate in x direction.
        maxy (Union[str, int, float]): Maximum coordinate in y direction.
        precision (int): presion applied at rounding.
    """

    def __init__(self,
                 minx: Union[str, int, float],
                 miny: Union[str, int, float],
                 maxx: Union[str, int, float],
                 maxy: Union[str, int, float],
                 precision: Optional[int] = None):

        try:
            minx, miny, maxx, maxy = tuple(map(float, (minx, miny,
                                                       maxx, maxy)))
        except (TypeError, ValueError) as error:
            raise ValueError('Invalid input parameters, coordinates '
                             'must be convertable to float number.') from error

        if minx > maxx:
            raise ValueError('minx must be smaller or equal to maxx')

        if miny > maxy:
            raise ValueError('miny must be smaller or equal to maxy')

        self._precision = precision
        self._minx = np.round(minx, self._precision)
        self._miny = np.round(miny, self._precision)
        self._maxx = np.round(maxx, self._precision)
        self._maxy = np.round(maxy, self._precision)

    @property
    def bbox(self):
        "Returns the bounding box as a tuple."
        return (self._minx, self._miny, self._maxx, self._maxy)

    @property
    def minx(self):
        return self._minx

    @minx.setter
    def minx(self, value):
        self._minx = np.round(float(value), self._precision)

    @property
    def miny(self):
        return self._miny

    @miny.setter
    def miny(self, value):
        self._miny = np.round(float(value), self._precision)

    @property
    def maxx(self):
        return self._maxx

    @maxx.setter
    def maxx(self, value):
        self._maxx = np.round(float(value), self._precision)

    @property
    def maxy(self):
        return self._maxy

    @maxy.setter
    def maxy(self, value):
        self._maxy = np.round(float(value), self._precision)

    def get_bbox_str(self, geographic=False):
        if geographic:
            return (f"min_lon={self.minx}, min_lat={self.miny}, "
                    f"max_lon={self.maxx}, max_lat={self.maxy}")
        else:
            return (f"min_x={self.minx}, min_y={self.miny}, "
                    f"max_x={self.maxx}, max_y={self.maxy}")


class TimeRange:
    """"Class for time range represented by two dates.

    Args:
        start_time (Union[str, pd.Timestamp]): Start date.
        end_time (Union[str, pd.Timestamp]): End date.
    """

    def __init__(self,
                 start_time: Union[str, pd.Timestamp],
                 end_time: Union[str, pd.Timestamp]):
        try:
            start_time, end_time = tuple(map(self.convert_time,
                                             (start_time, end_time)))
        except (TypeError, ValueError) as exc:
            raise ValueError(
                'Invalid input parameters, times '
                'must be convertable to pandas.TimeStamp.') from exc

        if start_time > end_time:
            raise ValueError('start_time must be smaller or '
                             'equal to end_time')

        self._start_time = start_time
        self._end_time = end_time

    @property
    def time_range(self):
        return (self._start_time, self._end_time)

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        start_time = self.convert_time(value)
        if start_time <= self._end_time:
            self._start_time = start_time
        else:
            raise ValueError('start_time must be smaller or '
                             'equal to end_time')

    @property
    def end_time(self):
        return self._end_time

    @end_time.setter
    def end_time(self, value):
        end_time = self.convert_time(value)
        if end_time >= self._start_time:
            self._end_time = end_time
        else:
            raise ValueError('end_time must be greater or '
                             'equal to start_time')

    def get_time_range_str(self, only_date=True):
        if only_date:
            return (self._start_time.isoformat(sep='T').split('T')[0],
                    self._end_time.isoformat(sep='T').split('T')[0])
        else:
            return (self._start_time.isoformat(sep='T'),
                    self._end_time.isoformat(sep='T'))

    def convert_to_full_months(self):

        self._start_time = self._start_time.replace(day=1)
        self._end_time = (self._end_time if self._end_time.is_month_end
                          else self._end_time + pd.offsets.MonthEnd())

    @classmethod
    def convert_time(cls,
                     datetime: Union[str, pd.Timestamp],
                     utc: bool = False):
        try:
            return pd.to_datetime(datetime, utc=utc)
        except Exception as error:
            raise ValueError('Could not convert datetime: '
                             f'{datetime} to pandas.Timestamp.') from error
