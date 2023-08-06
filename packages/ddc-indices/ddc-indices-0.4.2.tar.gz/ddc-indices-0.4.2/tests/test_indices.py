import pytest
import xarray as xr
import numpy as np
import pandas as pd
import unittest.mock as mock
from typing import Dict
from unittest.mock import patch
from ddc_indices import indices
from ddc_indices import config


def test_indices():
    assert isinstance(indices.DdcIndices.describe_indices(), dict)


def test_indices_init():
    ind = indices.DdcIndices()
    assert len(ind._indices) != 0


def test_index_validate_ds_xy(dataset):
    ds = indices.Index.validate_dataset(dataset)
    assert set(ds.dims) == {'time', 'x', 'y'}


def test_index_validate_ds_xy():
    ds = xr.Dataset(coords={
        "lat": (["lat"], []), "lon": (["lon"], []), "time": (["time"], [])})
    ds = indices.Index.validate_dataset(ds)
    assert set(ds.dims) == {'time', 'x', 'y'}


def test_index_validate_ds_bad():
    ds = xr.Dataset(coords={
        "y": (["y"], []), "x": (["x"], [])})
    with pytest.raises(ValueError):
        indices.Index.validate_dataset(ds)

# TEST SPI


def test_spi_prepare_dataset(dataset, spi_config_default):
    ds = indices.Spi._prepare_dataset(dataset, spi_config_default)
    assert ds is not None


def test_spi_global_metadata(spi_config_default):
    assert isinstance(indices.Spi._get_global_metadata(
        spi_config_default), dict)


def test_spi_local_metadata():
    assert isinstance(indices.Spi._get_local_metadata('3MS', 'gamma'), dict)


@patch('ddc_indices.config.SpiConfig.configure')
def test_spi_init(mock_configure, dataset, spi_config_default):
    mock_configure.return_value = spi_config_default
    spi = indices.Spi(dataset, spi_config_default)

    assert isinstance(spi, indices.Spi)
    assert isinstance(spi.dataset, xr.Dataset)
    assert isinstance(spi.config, config.SpiConfig)
    assert spi.index == None
    assert spi.params == None


def test_spi_compute(dataset, spi_config_default):

    spi = indices.Spi(dataset, spi_config_default)
    spi.compute()
    assert isinstance(spi.index, xr.Dataset)
    assert isinstance(spi.params, Dict)

# TEST SPEI


def test_spei_prepare_dataset(dataset, spei_config_default):
    ds = indices.Spei._prepare_dataset(dataset, spei_config_default)
    assert ds is not None


def test_spei_global_metadata(spei_config_default):
    assert isinstance(indices.Spei._get_global_metadata(
        spei_config_default), dict)


def test_spei_local_metadata():
    assert isinstance(indices.Spei._get_local_metadata('3MS', 'gamma'), dict)


@patch('ddc_indices.config.SpeiConfig.configure')
def test_spei_init(mock_configure, dataset, spei_config_default):
    mock_configure.return_value = spei_config_default
    spei = indices.Spei(dataset, spei_config_default)

    assert isinstance(spei, indices.Spei)
    assert isinstance(spei.dataset, xr.Dataset)
    assert isinstance(spei.config, config.SpeiConfig)
    assert spei.index == None
    assert spei.params == None


def test_spei_compute(dataset, spei_config_default):

    spei = indices.Spei(dataset, spei_config_default)
    spei.compute()
    assert isinstance(spei.index, xr.Dataset)
    assert isinstance(spei.params, Dict)

# TEST PNI


def test_pni_prepare_dataset(dataset, pni_config_default):
    ds = indices.Pni._prepare_dataset(dataset, pni_config_default)
    assert ds is not None


def test_pni_global_metadata(pni_config_default):
    assert isinstance(indices.Pni._get_global_metadata(
        pni_config_default), dict)


def test_pni_local_metadata():
    assert isinstance(indices.Pni._get_local_metadata('3MS'), dict)


@patch('ddc_indices.config.PniConfig.configure')
def test_pni_init(mock_configure, dataset, pni_config_default):
    mock_configure.return_value = pni_config_default
    pni = indices.Pni(dataset, pni_config_default)

    assert isinstance(pni, indices.Pni)
    assert isinstance(pni.dataset, xr.Dataset)
    assert isinstance(pni.config, config.PniConfig)
    assert pni.index == None


def test_pni_compute(dataset, pni_config_default):

    pni = indices.Pni(dataset, pni_config_default)
    pni.compute()
    assert isinstance(pni.index, xr.Dataset)
