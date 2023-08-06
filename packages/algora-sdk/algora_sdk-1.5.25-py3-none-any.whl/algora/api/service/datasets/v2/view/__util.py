from algora.api.service.datasets.v2.model import SearchRequest


def _get_dataset_view_request_info(id: str) -> dict:
    return {"endpoint": f"config/v2/dataset/view/{id}"}


def _get_dataset_views_request_info() -> dict:
    return {"endpoint": f"config/v2/dataset/view"}


def _search_dataset_views_request_info(request: SearchRequest) -> dict:
    return {
        "endpoint": f"config/v2/dataset/view/search",
        "json": request.request_dict(),
    }
