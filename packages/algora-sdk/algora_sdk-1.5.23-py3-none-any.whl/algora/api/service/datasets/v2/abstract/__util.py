from algora.api.service.datasets.v2.model import DatasetRequest, SearchRequest


def _get_abstract_dataset_request_info(id: str) -> dict:
    return {"endpoint": f"config/v2/dataset/abstract/{id}"}


def _get_abstract_datasets_request_info() -> dict:
    return {"endpoint": f"config/v2/dataset/abstract"}


def _search_abstract_datasets_request_info(request: SearchRequest) -> dict:
    return {
        "endpoint": f"config/v2/dataset/abstract/search",
        "json": request.request_dict(),
    }


def _create_abstract_dataset_request_info(request: DatasetRequest) -> dict:
    return {"endpoint": f"config/v2/dataset/abstract", "json": request.request_dict()}


def _update_abstract_dataset_request_info(id: str, request: DatasetRequest) -> dict:
    return {
        "endpoint": f"config/v2/dataset/abstract/{id}",
        "json": request.request_dict(),
    }


def _delete_abstract_dataset_request_info(id: str) -> dict:
    return {"endpoint": f"config/v2/dataset/abstract/{id}"}
