import pytest
import numpy as np
import xarray as xr
import pandas as pd

from ddc_indices import eto


@pytest.mark.parametrize("day_of_year, expected", [
    (3, -0.398),
    (90, 0.065),
    (156, 0.394)
])
def test_solar_declination(day_of_year, expected):
    res = eto._solar_declination(np.array([day_of_year]))
    assert round(float(res), 3) == expected


def test_solar_declination_error():
    with pytest.raises(ValueError):
        eto._solar_declination(np.array([1, 370]))


@pytest.mark.parametrize("lat, solar_dec, expected", [
    (1, 0.065, 1.672),
    (0.05, 0.394, 1.592)
])
def test_sunset_hour_angle(lat, solar_dec, expected):
    res = eto._sunset_hour_angle(np.array(lat), np.array(solar_dec))
    assert round(float(res), 3) == expected


def test_solar_declination_lat_error():
    with pytest.raises(ValueError):
        eto._sunset_hour_angle(np.array(np.deg2rad(110.0)), np.array(0.065))


def test_solar_declination_dec_error():
    with pytest.raises(ValueError):
        eto._sunset_hour_angle(np.array(1), np.array(np.deg2rad(30.0)))


@pytest.mark.parametrize("day_of_year, expected", [
    (3, 1.033),
    (90, 1.001),
    (156, 0.97)
])
def test_inv_rel_dist(day_of_year, expected):
    res = eto._inv_rel_dist_earth_sun(np.array([day_of_year]))
    assert round(float(res), 3) == expected


def test_inv_rel_dist_error():
    with pytest.raises(ValueError):
        eto._inv_rel_dist_earth_sun(np.array([1, 370]))


@pytest.mark.parametrize("latitude_radians, solar_declination_radians, "
                         "sunset_hour_angle_radians, inv_rel_dist, expected", [
                             (np.deg2rad(60.), np.deg2rad(10),
                              np.deg2rad(90), 1.02869645, 28.172),
                             (np.deg2rad(0), np.deg2rad(0),
                              np.deg2rad(10), 0.98953269, 6.458)
                         ])
def test_et_rad(latitude_radians,
                solar_declination_radians,
                sunset_hour_angle_radians,
                inv_rel_dist,
                expected):
    res = eto._et_rad(np.array([latitude_radians]),
                      np.array([solar_declination_radians]),
                      np.array([sunset_hour_angle_radians]),
                      np.array([inv_rel_dist]))
    assert round(float(res), 3) == expected


def test_et_rad_lat_error():
    with pytest.raises(ValueError):
        eto._et_rad(np.array([np.deg2rad(-120.0)]),
                    np.array([np.deg2rad(10)]),
                    np.array([np.deg2rad(90)]),
                    np.array([1.02869645]))


def test_et_rad_dec_error():
    with pytest.raises(ValueError):
        eto._et_rad(np.array([np.deg2rad(-90.0)]),
                    np.array([np.deg2rad(-50)]),
                    np.array([np.deg2rad(90)]),
                    np.array([1.02869645]))


def test_et_rad_sunset_error():
    with pytest.raises(ValueError):
        eto._et_rad(np.array([np.deg2rad(-90.0)]),
                    np.array([np.deg2rad(10)]),
                    np.array([np.deg2rad(200)]),
                    np.array([1.02869645]))


def test_eto_hargreaves(dataset):
    temp_keys = {'min': 'temp_min',
                 'max': 'temp_max'}

    res = eto.eto_hargreaves(dataset, temp_keys)
    assert type(res) == xr.DataArray
    assert set(dataset.dims.values()) == set(res.shape)


def test_eto_hargreaves_var_error(dataset):
    temp_keys = {'min': 'temp_minimum',
                 'max': 'temp_maximum'}
    with pytest.raises(KeyError):
        eto.eto_hargreaves(dataset, temp_keys)


def test_eto_hargreaves_coord_error():
    ds = xr.Dataset(
        coords={"latitude": (["latitude"], []),
                "longitude": (["longitude"], []),
                "time": (["time"], [])})

    temp_keys = {'min': 'temp_min',
                 'max': 'temp_max'}

    with pytest.raises(KeyError):
        eto.eto_hargreaves(ds, temp_keys)
