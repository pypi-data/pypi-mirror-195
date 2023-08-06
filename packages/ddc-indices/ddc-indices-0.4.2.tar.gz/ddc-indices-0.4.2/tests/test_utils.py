
import numpy as np
import pytest
import pandas as pd
import xarray as xr

from ddc_indices import utils


def test_bbox_init(bbox):
    assert bbox.bbox == (15.23, 44.51, 24.11, 50.92)


def test_bbox_bad_init():
    with pytest.raises(ValueError):
        utils.Bbox(17.0, 48.0, 21.0, 32.0, 2)


def test_bbox_to_str(bbox):
    assert bbox.get_bbox_str() == 'min_x=15.23, min_y=44.51, max_x=24.11, max_y=50.92'
    assert bbox.get_bbox_str(
        True) == 'min_lon=15.23, min_lat=44.51, max_lon=24.11, max_lat=50.92'


def test_bbox_reset(bbox):
    bbox.minx = 17
    bbox.miny = 48
    bbox.maxx = 21
    bbox.maxy = 52
    assert bbox.bbox == (17.0, 48.0, 21.0, 52.0)


def test_timerange_init(timerange):
    tr = (pd.Timestamp('2010-01-15'), pd.Timestamp('2018-07-22'))
    assert timerange.time_range == tr


def test_bbox_bad_init():
    with pytest.raises(ValueError):
        utils.TimeRange('2019-01-15', '2018-07-22')


def test_time_range_to_str(timerange):
    assert timerange.get_time_range_str() == ('2010-01-15', '2018-07-22')
    assert timerange.get_time_range_str(False) == (
        '2010-01-15T00:00:00', '2018-07-22T00:00:00')


def test_timerange_reset(timerange):
    timerange.start_time = '2000-01-01'
    timerange.end_time = '2008-01-01'
    tr = (pd.Timestamp('2000-01-01'), pd.Timestamp('2008-01-01'))
    assert timerange.time_range == tr


def test_timerange_to_full_months(timerange):
    timerange.convert_to_full_months()
    tr = (pd.Timestamp('2010-01-01'), pd.Timestamp('2018-07-31'))
    assert timerange.time_range == tr


def test_timerange_bad_convert():
    with pytest.raises(ValueError):
        utils.TimeRange.convert_time('2022-04-31')
