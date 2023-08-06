

import warnings
import xarray as xr
import pandas as pd
from pydantic import BaseModel, validator
from typing import Dict, List, Optional, Tuple, Union

from .constants import *
from .utils import Bbox, BboxType, TimeRange, TimeRangeType


class IndexConfig(BaseModel):
    """
    Index configuration base class.
    Specific configuration implementations can inheret from this base class.

    Attributes:
        bbox (BboxType): Bounding box, tuple of 4 numbers:
            (minx, miny, maxx, maxy)
        index_valid_range (Optional[Tuple[float, float]]): 
            Tuple of two values representing the min. and max. valid values. 

        Examples:
            # Create an IndexConfig object with a bbox around New York City.
            >>> bbox = (-74.3, 40.5, -73.5, 41.2)
            >>> index_valid_range = (0.0, 1.0)
            >>> config = IndexConfig(bbox=bbox,
                                     index_valid_range=index_valid_range)

    """

    bbox: Optional[BboxType] = DEFAULT_BBOX
    index_valid_range: Optional[Tuple[float, float]] = None

    @validator('bbox')
    def check_bbox(cls, v):
        return Bbox(*v, 2)

    @validator('index_valid_range')
    def check_index_valid_range(cls, v):
        if v is not None and v[0] > v[1]:
            raise ValueError(
                f"first value of v[0] must be smaller or equal to the second value v[1].")
        return v

    class Config:
        arbitrary_types_allowed = True
        validate_assignment = True
        validate_all = True


class SpiConfig(IndexConfig):
    """
    Index configuration for the Standardized Precipitation Index.

    Attributes:
        variables (Dict): A mapping for setting the variable holding
                the preciptation data.
                In case of SPI use: {'prec': '<precipitation_variable_name>'}
        periodicity (str): The periodicity of the time series
                (i.e. the temporal resolution) represented by the input data,
                valid/supported values are 'monthly' and 'daily'.
        time_coverage_range (Optional[TimeRangeType]): 
            Tuple of start and end date of the examined time period.
            Defaults to `1971-01-01` and the current date.
        time_reference_range (Optional[TimeRangeType]): Tuple of start and
            end date of the reference time period.
            Defaults to `1971-01-01` and `2000-12-31`.
        periods (List[str]): List of number of months, defining the periods
            the index is calculated on, e.g. ["MS3", "MS6"] in the case of
            SPI-3 and SPI-6. Defaults to ["MS3"].
        ref_months (List[int]): List of months to calculate the index on.
            For example [6, 7, 8] if index should be calculatod for only the
            summer months. Defaults to the whole year.
        distribution (str): Distribution type used for fitting.
            Valid/supported values are 'gamma' and 'pearson'.
        bbox (Optional[BboxType]): Bounding box, tuple of 4 numbers:
            (minx, miny, maxx, maxy), inhereted from `IndexConfig`.
        index_valid_range (Optional[Tuple[float, float]]): 
            Tuple of two values representing the min. and max. valid values,
            inhereted from `IndexConfig`.

        Examples:
            # Create an SpiConfig object
            >>> variables = {'prec': 'prec'}
            >>> periodicity = 'daily'
            >>> time_coverage_range = ('2021-01-01', '2022-01-01')
            >>> periods = ['MS3', 'MS6', 'MS9']
            >>> bbox = (-74.3, 40.5, -73.5, 41.2)
            >>> index_valid_range = (-3.0, 3.0)
            >>> config = SpiConfig(variables=variables,
                                   periodicity=periodicity,
                                   time_coverage_range=time_coverage_range,
                                   periods=periods,
                                   bbox=bbox,
                                   index_valid_range=index_valid_range)

    """

    variables: Dict
    periodicity: str
    time_coverage_range: Optional[TimeRangeType] = DEFAULT_COVERAGE_TIME_RANGE
    time_reference_range: Optional[TimeRangeType] = DEFAULT_REFERENCE_TIME_RANGE
    periods: List[str] = DEFAULT_PERIOD
    ref_months: List[int] = DEFAULT_REF_MONTHS_LIST
    distribution: str = 'gamma'

    @validator('variables')
    def check_variables(cls, v):
        if 'prec' not in v:
            raise ValueError("'prec' variable key must be set for SPI.")
        return v

    @validator('periodicity')
    def check_periodicity(cls, v):
        try:
            return Periodicity[v]
        except KeyError as err:
            raise ValueError(f'Invalid periodicity: {v}') from err

    @validator('time_reference_range', 'time_coverage_range')
    def check_time_range(cls, v):
        return TimeRange(*v)

    @validator('periods', each_item=True)
    def check_periods(cls, v):
        try:
            return SpiPeriods[v]
        except KeyError as err:
            raise ValueError(f'Invalid period: {v}') from err

    @validator('ref_months', each_item=True)
    def check_ref_months(cls, v):
        if v not in VALID_REF_MONTHS_LIST:
            raise ValueError(f"Invalid value for ref_months: {v}")
        return v

    @validator('distribution')
    def check_distribution(cls, v):
        return Distribution(v)

    @property
    def name(self):
        """Name of the index."""
        return 'SPI'

    def configure(self, dataset: xr.Dataset):
        """
        Executes further validations based on source dataset and
        modifies parameters if neccessary.

        Args:
            dataset (xr.Dataset): Dataset the check the parameters againts.
        """

        # Pearson distribution is not yet implemented
        if self.distribution == Distribution.PEARSON:
            raise NotImplementedError("Pearson correlation is not valid")

        # Check if supplied variables are actually exists
        for v in self.variables.values():
            if v not in dataset.data_vars:
                raise ValueError(f"Invalid variable name {v}")

        # Check if periodicity is reasonable
        infer_freq = xr.infer_freq(dataset.time)  # xarray tool.
        if self.periodicity.value['frequency'] != infer_freq:
            warnings.warn(
                f"periodicity argument of {self.periodicity.value['frequency']}"
                " doesn't seem to match with time resolution of the dataset: "
                f"{infer_freq} -- results may be wrong")

        # Compare configuration time ranges and time ranges of the dataset
        # If needed adjust configuration
        self.time_reference_range.start_time = check_times_min(
            dataset=dataset,
            time_range_min=self.time_reference_range.start_time,
            message="reference start date is smaller, than dataset's start date"
                    " -- resetting start date")
        self.time_reference_range.end_time = check_times_max(
            dataset=dataset,
            time_range_max=self.time_reference_range.end_time,
            message="reference end date is larger, than dataset's end date "
                    "-- resetting end date")
        self.time_coverage_range.start_time = check_times_min(
            dataset=dataset,
            time_range_min=self.time_coverage_range.start_time,
            message="coverage start date is smaller, than dataset's start date"
                    " -- resetting start date")
        self.time_coverage_range.end_time = check_times_max(
            dataset=dataset,
            time_range_max=self.time_coverage_range.end_time,
            message="coverage end date is larger, than dataset's end date "
                    "-- resetting end date")

        # Compare configuration bbox and geographical ranges of the dataset
        # If needed adjust configuration
        self.bbox = check_geo(
            dataset=dataset,
            bbox=self.bbox.bbox,
            message="bbox is larger, than dataset's bbox -- resetting bbox")

        # Set reference month, if needed i.e. not calculate index
        # for the whole year only for specific months
        month_diff = (self.time_coverage_range.end_time.to_period(
            'M') - self.time_coverage_range.start_time.to_period('M')).n + 1
        if month_diff < 12:
            self.ref_months = [(self.time_coverage_range.start_time.to_period(
                'M') + m).month for m in range(month_diff)]


class SpeiConfig(IndexConfig):
    """
    Index configuration for the
    Standardized Precipitation Evapotranspiration Index.

    Attributes:
        variables (Dict): A mapping for setting the variable holding
            the preciptation and evapotranspiration. If evapotranspiration will
            be calculated by the package, min and max and optionally mean 
            temperature values must be provided.
            {'precipitation': '<precipitation_variable_name>',
             'eto': '<evapotranspiration_variable_name>',
             'temp_min': '<temp_min_variable_name>', 
             'temp_max': '<temp_max_variable_name>', 
             'temp_mean: '<temp_min_variable_name>', }
        periodicity (str): The periodicity of the time series
                (i.e. the temporal resolution) represented by the input data,
                valid/supported values are 'monthly' and 'daily'.
        time_coverage_range (Optional[TimeRangeType]): 
            Tuple of start and end date of the examined time period.
            Defaults to `1971-01-01` and the current date.
        time_reference_range (Optional[TimeRangeType]): Tuple of start and
            end date of the reference time period.
            Defaults to `1971-01-01` and `2000-12-31`.
        periods (List[str]): List of number of months, defining the periods
            the index is calculated on, e.g. ["MS3", "MS6"] in the case of
            SPEI-3 and SPEI-6. Defaults to ["MS3"].
        ref_months (List[int]): List of months to calculate the index on.
            For example [6, 7, 8] if index should be calculatod for only the
            summer months. Defaults to the whole year.
        distribution (str): Distribution type used for fitting.
            Valid/supported values are 'gamma' and 'pearson'.
        bbox (Optional[BboxType]): Bounding box, tuple of 4 numbers:
            (minx, miny, maxx, maxy), inhereted from `IndexConfig`.
        index_valid_range (Optional[Tuple[float, float]]): 
            Tuple of two values representing the min. and max. valid values,
            inhereted from `IndexConfig`.

        Examples:
            # Create an SpeiConfig object
            >>> variables = {'prec': 'prec',
                             'eto': 'pet',
                             'temp_min': 'minimum_temp',
                             'temp_max': 'maximum_temp'}
            >>> periodicity = 'daily'
            >>> time_coverage_range = ('2021-01-01', '2022-01-01')
            >>> periods = ['MS3', 'MS6', 'MS9']
            >>> bbox = (-74.3, 40.5, -73.5, 41.2)
            >>> index_valid_range = (-3.0, 3.0)
            >>> config = SpeiConfig(variables=variables,
                                    periodicity=periodicity,
                                    time_coverage_range=time_coverage_range,
                                    periods=periods,
                                    bbox=bbox,
                                    index_valid_range=index_valid_range)

    """

    variables: Dict
    periodicity: str
    time_coverage_range: Optional[TimeRangeType] = DEFAULT_COVERAGE_TIME_RANGE
    time_reference_range: Optional[TimeRangeType] = DEFAULT_REFERENCE_TIME_RANGE
    periods: List[str] = DEFAULT_PERIOD
    ref_months: List[int] = DEFAULT_REF_MONTHS_LIST
    distribution: str = 'gamma'

    @validator('variables')
    def check_variables(cls, v):
        if 'prec' not in v:
            raise ValueError("'prec' variable key must be set for SPEI.")
        if 'eto' not in v:
            if 'temp_min' not in v and 'temp_max' not in v:
                raise ValueError("Either 'eto' or 'temp_min' and 'temp_max' "
                                 "variable keys must be set for SPEI.")
        warnings.warn(
            "Evapotranspiration dataset fetched from DDC is not a "
            "full dataset. Valid values are only after 2000.01.01. "
            "Please, make sure, that your time_reference_range is after "
            "2000.01.01, else support 'temp_min' and 'temp_max' in the "
            "config object and before computing the index estimate eto with "
            "SpeiIndex().estimate_eto()")
        return v

    @validator('periodicity')
    def check_periodicity(cls, v):
        try:
            return Periodicity[v]
        except KeyError as err:
            raise ValueError(f'Invalid periodicity: {v}') from err

    @validator('time_reference_range', 'time_coverage_range')
    def check_time_range(cls, v):
        return TimeRange(*v)

    @validator('periods', each_item=True)
    def check_periods(cls, v):
        try:
            return SpeiPeriods[v]
        except KeyError as err:
            raise ValueError(f'Invalid period: {v}') from err

    @validator('ref_months', each_item=True)
    def check_ref_months(cls, v):
        if v not in VALID_REF_MONTHS_LIST:
            raise ValueError(f"Invalid value for ref_months: {v}")
        return v

    @validator('distribution')
    def check_distribution(cls, v):
        return Distribution(v)

    @property
    def name(self):
        """Name of the index."""
        return 'SPEI'

    def configure(self, dataset: xr.Dataset):
        """
        Executes further validations based on source dataset and
        modifies parameters if neccessary.

        Args:
            dataset (xr.Dataset): Dataset the check the parameters againts.
        """

        # Pearson distribution is not yet implemented
        if self.distribution == Distribution.PEARSON:
            raise NotImplementedError("Pearson correlation is not valid")

        # Check if supplied variables are actually exists
        for v in self.variables.values():
            if v not in dataset.data_vars:
                raise ValueError(f"Invalid variable name {v}")

        # Check if periodicity is reasonable
        infer_freq = xr.infer_freq(dataset.time)  # xarray tool.
        if self.periodicity.value['frequency'] != infer_freq:
            warnings.warn(
                f"periodicity argument of {self.periodicity.value['frequency']}"
                " doesn't seem to match with time resolution of the dataset: "
                f"{infer_freq} -- results may be wrong")

        # Compare configuration time ranges and time ranges of the dataset
        # If needed adjust configuration
        self.time_reference_range.start_time = check_times_min(
            dataset=dataset,
            time_range_min=self.time_reference_range.start_time,
            message="reference start date is smaller, than dataset's start date"
                    " -- resetting start date")
        self.time_reference_range.end_time = check_times_max(
            dataset=dataset,
            time_range_max=self.time_reference_range.end_time,
            message="reference end date is larger, than dataset's end date "
                    "-- resetting end date")
        self.time_coverage_range.start_time = check_times_min(
            dataset=dataset,
            time_range_min=self.time_coverage_range.start_time,
            message="coverage start date is smaller, than dataset's start date"
                    " -- resetting start date")
        self.time_coverage_range.end_time = check_times_max(
            dataset=dataset,
            time_range_max=self.time_coverage_range.end_time,
            message="coverage end date is larger, than dataset's end date "
                    "-- resetting end date")

        # Compare configuration bbox and geographical ranges of the dataset
        # If needed adjust configuration
        self.bbox = check_geo(
            dataset=dataset,
            bbox=self.bbox.bbox,
            message="bbox is larger, than dataset's bbox -- resetting bbox")

        # Set reference month, if needed i.e. not calculate index
        # for the whole year only for specific months
        month_diff = (self.time_coverage_range.end_time.to_period(
            'M') - self.time_coverage_range.start_time.to_period('M')).n + 1
        if month_diff < 12:
            self.ref_months = [(self.time_coverage_range.start_time.to_period(
                'M') + m).month for m in range(month_diff)]


class PniConfig(IndexConfig):
    """Index configuration for the Percent of Normal Index (PNI).

    Attributes:
        variables (Dict): A mapping for setting the variable holding
            the preciptation data.
            {'precipitation': '<precipitation_variable_name>'}
        periodicity (str): The periodicity of the time series
                (i.e. the temporal resolution) represented by the input data,
                valid/supported values are 'monthly' and 'daily'.
        time_coverage_range (Optional[TimeRangeType]): 
            Tuple of start and end date of the examined time period.
            Defaults to `1971-01-01` and the current date.
        time_reference_range (Optional[TimeRangeType]): Tuple of start and
            end date of the reference time period.
            Defaults to `1971-01-01` and `2000-12-31`.
        periods (List[str]): List of number of months, defining the periods
            the index is calculated on, e.g. ["MS3", "MS6"] in the case of
            PNI-3 and PNI-6. Defaults to ["MS3"].
        ref_months (List[int]): List of months to calculate the index on.
            For example [6, 7, 8] if index should be calculatod for only the
            summer months. Defaults to the whole year.
        bbox (Optional[BboxType]): Bounding box, tuple of 4 numbers:
            (minx, miny, maxx, maxy), inhereted from `IndexConfig`.
        index_valid_range (Optional[Tuple[float, float]]): 
            Tuple of two values representing the min. and max. valid values,
            inhereted from `IndexConfig`.

        Examples:
            # Create an PniConfig object
            >>> variables = {'prec': 'prec'}
            >>> periodicity = 'daily'
            >>> time_coverage_range = ('2021-01-01', '2022-01-01')
            >>> periods = ['MS3', 'MS6', 'MS9']
            >>> bbox = (-74.3, 40.5, -73.5, 41.2)
            >>> index_valid_range = (0.0, 1.0)
            >>> config = PniConfig(variables=variables,
                                   periodicity=periodicity,
                                   time_coverage_range=time_coverage_range,
                                   periods=periods,
                                   bbox=bbox,
                                   index_valid_range=index_valid_range)

    """

    variables: Dict
    periodicity: str
    time_coverage_range: Optional[TimeRangeType] = DEFAULT_COVERAGE_TIME_RANGE
    time_reference_range: Optional[TimeRangeType] = DEFAULT_REFERENCE_TIME_RANGE
    periods: List[str] = DEFAULT_PERIOD
    ref_months: List[int] = DEFAULT_REF_MONTHS_LIST

    @validator('variables')
    def check_variables(cls, v):
        if 'prec' not in v:
            raise ValueError("'prec' variable key must be set for PNI.")
        return v

    @validator('periodicity')
    def check_periodicity(cls, v):
        try:
            return Periodicity[v]
        except KeyError as err:
            raise ValueError(f'Invalid periodicity: {v}') from err

    @validator('time_reference_range', 'time_coverage_range')
    def check_time_range(cls, v):
        return TimeRange(*v)

    @validator('periods', each_item=True)
    def check_periods(cls, v):
        try:
            return PniPeriods[v]
        except KeyError as err:
            raise ValueError(f'Invalid period: {v}') from err

    @validator('ref_months', each_item=True)
    def check_ref_months(cls, v):
        if v not in VALID_REF_MONTHS_LIST:
            raise ValueError(f"Invalid value for ref_months: {v}")
        return v

    @property
    def name(self):
        """Name of the index."""
        return 'PNI'

    def configure(self, dataset: xr.Dataset):
        """
        Executes further validations based on source dataset and
        modifies parameters if neccessary.

        Args:
            dataset (xr.Dataset): Dataset the check the parameters againts.
        """

        # Check if supplied variables are actually exists
        for v in self.variables.values():
            if v not in dataset.data_vars:
                raise ValueError(f"Invalid variable name {v}")

        # Check if periodicity is reasonable
        infer_freq = xr.infer_freq(dataset.time)  # xarray tool.
        if self.periodicity.value['frequency'] != infer_freq:
            warnings.warn(
                f"periodicity argument of {self.periodicity.value['frequency']}"
                " doesn't seem to match with time resolution of the dataset: "
                f"{infer_freq} -- results may be wrong")

        # Compare configuration time ranges and time ranges of the dataset
        # If needed adjust configuration
        self.time_reference_range.start_time = check_times_min(
            dataset=dataset,
            time_range_min=self.time_reference_range.start_time,
            message="reference start date is smaller, than dataset's start date"
                    " -- resetting start date")
        self.time_reference_range.end_time = check_times_max(
            dataset=dataset,
            time_range_max=self.time_reference_range.end_time,
            message="reference end date is larger, than dataset's end date "
                    "-- resetting end date")
        self.time_coverage_range.start_time = check_times_min(
            dataset=dataset,
            time_range_min=self.time_coverage_range.start_time,
            message="coverage start date is smaller, than dataset's start date"
                    " -- resetting start date")
        self.time_coverage_range.end_time = check_times_max(
            dataset=dataset,
            time_range_max=self.time_coverage_range.end_time,
            message="coverage end date is larger, than dataset's end date "
                    "-- resetting end date")

        # Compare configuration bbox and geographical ranges of the dataset
        # If needed adjust configuration
        self.bbox = check_geo(
            dataset=dataset,
            bbox=self.bbox.bbox,
            message="bbox is larger, than dataset's bbox -- resetting bbox")

        # Set reference month, if needed i.e. not calculate index
        # for the whole year only for specific months
        month_diff = (self.time_coverage_range.end_time.to_period(
            'M') - self.time_coverage_range.start_time.to_period('M')).n + 1
        if month_diff < 12:
            self.ref_months = [(self.time_coverage_range.start_time.to_period(
                'M') + m).month for m in range(month_diff)]


class PdsiConfig(IndexConfig):

    @property
    def name(self):
        """Name of the index."""
        return 'PDSI'

##### --- UTILITY FUNCTIONS --- #####


def check_times_min(dataset: xr.Dataset,
                    time_range_min: pd.Timestamp,
                    message: Optional[str] = None) -> pd.Timestamp:

    if time_range_min < dataset['time'].min():
        if message:
            warnings.warn(message)
        return pd.Timestamp(dataset['time'].min().values)
    else:
        return time_range_min


def check_times_max(dataset: xr.Dataset,
                    time_range_max: pd.Timestamp,
                    message: Optional[str] = None) -> pd.Timestamp:

    if time_range_max > dataset['time'].max():
        if message:
            warnings.warn(message)
        return pd.Timestamp(dataset['time'].max().values)
    else:
        return time_range_max


def check_geo(dataset: Union[xr.Dataset, xr.DataArray],
              bbox: Tuple[float, float, float, float],
              message: Optional[str] = None
              ) -> Tuple[float, float, float, float]:
    count = 0
    bbox = list(bbox)
    if bbox[0] < dataset['x'].min():
        bbox[0] = float(dataset['x'].min())
        count += 1

    if bbox[1] < dataset['y'].min():
        bbox[1] = float(dataset['y'].min())
        count += 1

    if bbox[2] > dataset['x'].max():
        bbox[2] = float(dataset['x'].max())
        count += 1

    if bbox[3] > dataset['y'].max():
        bbox[3] = float(dataset['y'].max())
        count += 1

    if count != 0 and message:
        warnings.warn(message)

    return tuple(bbox)
