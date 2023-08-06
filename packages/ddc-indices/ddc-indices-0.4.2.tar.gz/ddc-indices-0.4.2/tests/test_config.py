
import pytest
import pandas as pd
import numpy as np
import xarray as xr
from pydantic import ValidationError

from ddc_indices import config
from ddc_indices.utils import TimeRange, Bbox
from ddc_indices.constants import Distribution, Periodicity


def test_index_config_default():
    conf = config.IndexConfig()
    assert isinstance(conf.bbox, Bbox)


def test_index_config_custom():
    conf = config.IndexConfig(
        bbox=(16.2, 44.5, 22.9, 51.2),
        index_valid_range=(-3, 3))

    assert isinstance(conf.bbox, Bbox)
    assert conf.index_valid_range is not None

# TEST SPI


@pytest.mark.parametrize(
    "config_obj",
    [
        ("spi_config_default"),
        ("spi_config_custom")
    ],
)
def test_spi_config(config_obj, request):
    config_obj = request.getfixturevalue(config_obj)

    assert config_obj.name == 'SPI'
    assert isinstance(config_obj.time_coverage_range, TimeRange)
    assert isinstance(config_obj.bbox, Bbox)
    assert isinstance(config_obj.periodicity, Periodicity)
    assert isinstance(config_obj.time_reference_range, TimeRange)
    assert isinstance(config_obj.periods, list)
    assert isinstance(config_obj.ref_months, list)
    assert isinstance(config_obj.distribution, Distribution)


def test_spi_config_bad_variable():
    with pytest.raises(ValidationError):
        config.SpiConfig(variables={'precip': 'precip'},
                         periodicity='monthly',
                         periods=['MS3'])


def test_spi_config_bad_period():
    with pytest.raises(ValidationError):
        config.SpiConfig(variables={'prec': 'prec'},
                         periodicity='monthly',
                         periods=['MS7'])


def test_spi_config__bad_periodicity():
    with pytest.raises(ValidationError):
        config.SpiConfig(variables={'prec': 'prec'},
                         periodicity='hourly')


def test_spi_config_bad_dist():
    with pytest.raises(ValidationError):
        config.SpiConfig(variables={'prec': 'prec'},
                         periodicity='monthly',
                         distribution='normal')


@pytest.mark.parametrize(
    "config_obj, ds, expected",
    [
        ("spi_config_default", "dataset", [(17.0, 47.0, 18.0, 48.0),
                                           '1971-01-01',
                                           '2011-08-31',
                                           12],
         ),
        ("spi_config_custom", "dataset", [(17.0, 47.0, 18.0, 48.0),
                                          '2010-01-01',
                                          '2010-06-01',
                                          6],
         )
    ],
)
def test_spi_config_configure(config_obj, ds, expected, request):
    config_obj = request.getfixturevalue(config_obj)
    ds = request.getfixturevalue(ds)

    config_obj.configure(ds)

    assert config_obj.bbox.bbox == expected[0]
    assert config_obj.time_coverage_range.time_range == (
        pd.Timestamp(expected[1]), pd.Timestamp(expected[2]))
    assert len(config_obj.ref_months) == expected[3]


# TEST SPEI

@pytest.mark.parametrize(
    "config_obj",
    [
        ("spei_config_default"),
        ("spei_config_custom")
    ],
)
def test_spei_config(config_obj, request):
    config_obj = request.getfixturevalue(config_obj)

    assert config_obj.name == 'SPEI'
    assert isinstance(config_obj.time_coverage_range, TimeRange)
    assert isinstance(config_obj.bbox, Bbox)
    assert isinstance(config_obj.periodicity, Periodicity)
    assert isinstance(config_obj.time_reference_range, TimeRange)
    assert isinstance(config_obj.periods, list)
    assert isinstance(config_obj.ref_months, list)
    assert isinstance(config_obj.distribution, Distribution)


def test_spei_config_bad_variable():
    with pytest.raises(ValidationError):
        config.SpeiConfig(variables={'precip': 'precip'},
                          periodicity='monthly',
                          periods=['MS3'])


def test_spei_config_bad_period():
    with pytest.raises(ValidationError):
        config.SpeiConfig(variables={'prec': 'prec'},
                          periodicity='monthly',
                          periods=['MS15'])


def test_spei_config__bad_periodicity():
    with pytest.raises(ValidationError):
        config.SpeiConfig(variables={'prec': 'prec'},
                          periodicity='hourly')


def test_spei_config_bad_dist():
    with pytest.raises(ValidationError):
        config.SpeiConfig(variables={'prec': 'prec'},
                          periodicity='monthly',
                          distribution='normal')


@pytest.mark.parametrize(
    "config_obj, ds, expected",
    [
        ("spei_config_default", "dataset", [(17.0, 47.0, 18.0, 48.0),
                                            '1971-01-01',
                                            '2011-08-31',
                                            12],
         ),
        ("spei_config_custom", "dataset", [(17.5, 47.3, 17.8, 47.8),
                                           '2010-01-01',
                                           '2011-08-31',
                                           12],
         )
    ],
)
def test_spei_config_configure(config_obj, ds, expected, request):
    config_obj = request.getfixturevalue(config_obj)
    ds = request.getfixturevalue(ds)

    config_obj.configure(ds)

    assert config_obj.bbox.bbox == expected[0]
    assert config_obj.time_coverage_range.time_range == (
        pd.Timestamp(expected[1]), pd.Timestamp(expected[2]))
    assert len(config_obj.ref_months) == expected[3]


# TEST PNI


@pytest.mark.parametrize(
    "config_obj",
    [
        ("pni_config_default"),
        ("pni_config_custom")
    ],
)
def test_pni_config(config_obj, request):
    config_obj = request.getfixturevalue(config_obj)

    assert config_obj.name == 'PNI'
    assert isinstance(config_obj.time_coverage_range, TimeRange)
    assert isinstance(config_obj.bbox, Bbox)
    assert isinstance(config_obj.periodicity, Periodicity)
    assert isinstance(config_obj.time_reference_range, TimeRange)
    assert isinstance(config_obj.periods, list)
    assert isinstance(config_obj.ref_months, list)


def test_pni_config_bad_variable():
    with pytest.raises(ValidationError):
        config.PniConfig(variables={'precip': 'precip'},
                         periodicity='monthly',
                         periods=['MS3'])


def test_pni_config_bad_period():
    with pytest.raises(ValidationError):
        config.PniConfig(variables={'prec': 'prec'},
                         periodicity='monthly',
                         periods=['MS7'])


def test_pni_config__bad_periodicity():
    with pytest.raises(ValidationError):
        config.PniConfig(variables={'prec': 'prec'},
                         periodicity='hourly')


@pytest.mark.parametrize(
    "config_obj, ds, expected",
    [
        ("pni_config_default", "dataset", [(17.0, 47.0, 18.0, 48.0),
                                           '1971-01-01',
                                           '2011-08-31',
                                           12],
         ),
        ("pni_config_custom", "dataset", [(17.0, 47.3, 17.8, 48.0),
                                          '1970-01-31',
                                          '2011-08-31',
                                          12],
         )
    ],
)
def test_pni_config_configure(config_obj, ds, expected, request):
    config_obj = request.getfixturevalue(config_obj)
    ds = request.getfixturevalue(ds)

    config_obj.configure(ds)

    assert config_obj.bbox.bbox == expected[0]
    assert config_obj.time_coverage_range.time_range == (
        pd.Timestamp(expected[1]), pd.Timestamp(expected[2]))
    assert len(config_obj.ref_months) == expected[3]

# TEST UTILITY FUNCTIONS


@pytest.mark.parametrize("bbox, expected", [
    ((17.1, 47.2, 17.4, 47.4), (17.1, 47.2, 17.4, 47.4)),
    ((10.0, 40.0, 28.0, 55.0), (17.0, 47.0, 18.0, 48.0))
])
def test_check_geo(dataset, bbox, expected):
    assert config.check_geo(dataset, bbox) == expected


@pytest.mark.parametrize("time_range_min, expected", [
    (pd.Timestamp('1960-01-01'), '1970-01-31T00:00:00'),
    (pd.Timestamp('1980-01-01'), '1980-01-01T00:00:00')
])
def test_check_times_min(dataset, time_range_min, expected):
    date = config.check_times_min(dataset, time_range_min)
    assert date.strftime('%Y-%m-%dT%X') == expected


@pytest.mark.parametrize("time_range_max, expected", [
    (pd.Timestamp('2010-01-01'), '2010-01-01T00:00:00'),
    (pd.Timestamp('2020-01-01'), '2011-08-31T00:00:00')
])
def test_check_times_max(dataset, time_range_max, expected):
    date = config.check_times_max(dataset, time_range_max)
    assert date.strftime('%Y-%m-%dT%X') == expected
