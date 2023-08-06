from algora.api.data.query.model import TimeseriesQueryRequest, DistinctQueryRequest


def _query_datasets_request_info(id: str, data=None, json=None) -> dict:
    return {"endpoint": f"data/datasets/query/{id}", "data": data, "json": json}


def _query_dataset_csv_request_info(id: str, data=None) -> dict:
    return {"endpoint": f"data/datasets/query/{id}.csv", "data": data}


def _query_timeseries_request_info(request: TimeseriesQueryRequest) -> dict:
    return {"endpoint": f"data/timeseries", "json": request.request_dict()}


def _query_dataset_csv_request_info_v2(
    id: str, request: TimeseriesQueryRequest
) -> dict:
    return {"endpoint": f"data/{id}.csv", "json": request.request_dict()}


def _query_distinct_fields_request_info(request: DistinctQueryRequest) -> dict:
    return {"endpoint": f"data/distinct", "json": request.request_dict()}
