import pytest
import xarray as xr
import numpy as np
import pandas as pd

from ddc_indices import compute
from ddc_indices.constants import Distribution, SpiPeriods, SpeiPeriods, PniPeriods


@pytest.fixture
def array_1d():
    np.random.seed(42)
    time = pd.date_range(start="2010-01-01", periods=24, freq='M')
    values = np.random.randint(0, 100, size=len(time))
    return xr.DataArray(values, coords=[time], dims=['time'])


def test_compute_spi(dataset):

    time_coverage_range = (pd.Timestamp('1970-01-01'),
                           pd.Timestamp('1991-12-31'))
    time_reference_range = (pd.Timestamp('1970-01-01'),
                            pd.Timestamp('2010-12-31'))
    period = SpiPeriods.MS3
    distribution = Distribution.GAMMA
    ref_months_list = [6, 7, 8]
    spi, a, b = compute.compute_spi(dataset['prec'],
                                    time_coverage_range,
                                    time_reference_range,
                                    period,
                                    distribution,
                                    ref_months_list)
    assert isinstance(spi, xr.DataArray)
    assert isinstance(a, xr.DataArray)
    assert isinstance(b, xr.DataArray)
    assert spi.sum().values > 50 and spi.sum().values < 55


def test_compute_spei(dataset):

    time_coverage_range = (pd.Timestamp('1970-01-01'),
                           pd.Timestamp('1991-12-31'))
    time_reference_range = (pd.Timestamp('1970-01-01'),
                            pd.Timestamp('2010-12-31'))
    period = SpeiPeriods.MS3
    distribution = Distribution.GAMMA
    ref_months_list = [6, 7, 8]
    spei, a, b = compute.compute_spei(dataset['prec'],
                                      dataset['eto'],
                                      time_coverage_range,
                                      time_reference_range,
                                      period,
                                      distribution,
                                      ref_months_list)
    assert isinstance(spei, xr.DataArray)
    assert isinstance(a, xr.DataArray)
    assert isinstance(b, xr.DataArray)
    assert spei.sum().values > -30 and spei.sum().values < -25


def test_compute_pni(dataset):

    time_coverage_range = (pd.Timestamp('1970-01-01'),
                           pd.Timestamp('1991-12-31'))
    time_reference_range = (pd.Timestamp('1970-01-01'),
                            pd.Timestamp('2010-12-31'))
    period = PniPeriods.MS3
    ref_months_list = [6, 7, 8]
    pni = compute.compute_pni(dataset['prec'],
                              time_coverage_range,
                              time_reference_range,
                              period,
                              ref_months_list)
    assert isinstance(pni, xr.DataArray)
    assert pni.sum().values > 7988 and pni.sum().values < 7992


def test_get_rolling_sum(array_1d):
    res = compute._get_rolling_sum(array_1d, 3)
    assert isinstance(res, xr.DataArray)
    assert res.values[1] == 143


def test_get_indexes(array_1d):
    assert compute._get_indexes(array_1d, 'time.month', 6) == [5, 17]


def test_get_gamma_params(dataset):
    a, b = compute._get_gamma_params(dataset['prec'])
    assert isinstance(a, xr.DataArray)
    assert isinstance(b, xr.DataArray)
    assert dataset['prec'][0, :, :].shape == a.shape == b.shape


def test_fit_gamma(dataset):
    fitting_params = compute._get_gamma_params(dataset['prec'])
    reference_data = dataset['prec'].sel(
        time=slice('1970-01-01', '1990-01-01'))
    norm, a, b = compute._fit_gamma(
        dataset['prec'], reference_data, fitting_params)
    assert isinstance(norm, xr.DataArray)
    assert isinstance(a, xr.DataArray)
    assert isinstance(b, xr.DataArray)
    assert dataset['prec'].shape == norm.shape
    assert dataset['prec'][0, :, :].shape == a.shape
    assert dataset['prec'][0, :, :].shape == b.shape
    assert np.absolute(norm).sum() != 0
