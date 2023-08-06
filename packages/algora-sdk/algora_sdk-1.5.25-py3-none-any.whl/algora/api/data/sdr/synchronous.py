from typing import Optional, List

from pandas import DataFrame

from algora.api.data.query import query_dataset, query_timeseries
from algora.api.data.sdr.__util import (
    _get_by_date_request_info,
    _get_distinct_in_field_request_info,
    _commodity_request_info,
    _credit_request_info,
    _rates_request_info,
    _forex_request_info,
    _equity_request_info,
)
from algora.api.data.sdr.enum import AssetClass, Repository
from algora.api.data.sdr.model import DataFilter
from algora.common.decorators import data_request
from algora.common.function import to_pandas_with_index, no_transform
from algora.common.requests import __get_request


@data_request(
    transformers=[lambda data: to_pandas_with_index(data, index="execution_timestamp")]
)
def get_by_date(
    asset_class: AssetClass, date: str, repos: Optional[List[Repository]] = None
) -> DataFrame:
    """
    Get all SDR data by asset class, date and repositories.

    Args:
        asset_class (AssetClass): Asset class enum (COMMODITY, CREDIT, EQUITY, FOREX, RATES)
        date (str): Date in YYYY-MM-DD format (e.g. "2022-01-01")
        repos (Optional[List[Repository]]): Repository enum list (e.g. [CME, DTCC, ICE])

    Returns:
        DataFrame: DataFrame
    """
    request_info = _get_by_date_request_info(asset_class, date, repos)
    return __get_request(**request_info)


@data_request(transformers=[no_transform])
def get_distinct_in_field(asset_class: AssetClass, field: str) -> List[str]:
    """
    Get all distinct values in field.

    Args:
        asset_class (AssetClass): Asset class enum (COMMODITY, CREDIT, EQUITY, FOREX, RATES)
        field (str): Field to query for

    Returns:
        List[str]: List of all distinct values in field
    """
    request_info = _get_distinct_in_field_request_info(asset_class, field)
    return __get_request(**request_info)


@data_request
def commodity(data_filter: Optional[DataFilter] = None):
    """
    Get SDR Commodity dataset.

    Args:
        data_filter (Optional[DataFilter]): Dataset query filter

    Returns:
        DataFrame: DataFrame
    """
    request_info = _commodity_request_info(data_filter)
    return query_timeseries(**request_info)


@data_request
def credit(data_filter: Optional[DataFilter] = None):
    """
    Get SDR Credit dataset.

    Args:
        data_filter (Optional[DataFilter]): Dataset query filter

    Returns:
        DataFrame: DataFrame
    """
    request_info = _credit_request_info(data_filter)
    return query_dataset(**request_info)


@data_request
def equity(data_filter: Optional[DataFilter] = None):
    """
    Get SDR Equity dataset.

    Args:
        data_filter (Optional[DataFilter]): Dataset query filter

    Returns:
        DataFrame: DataFrame
    """
    request_info = _equity_request_info(data_filter)
    return query_dataset(**request_info)


@data_request
def forex(data_filter: Optional[DataFilter] = None):
    """
    Get SDR Forex dataset.

    Args:
        data_filter (Optional[DataFilter]): Dataset query filter

    Returns:
        DataFrame: DataFrame
    """
    request_info = _forex_request_info(data_filter)
    return query_dataset(**request_info)


@data_request
def rates(data_filter: Optional[DataFilter] = None):
    """
    Get SDR Rates dataset.

    Args:
        data_filter (Optional[DataFilter]): Dataset query filter

    Returns:
        DataFrame: DataFrame
    """
    request_info = _rates_request_info(data_filter)
    return query_dataset(**request_info)
