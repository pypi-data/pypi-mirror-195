from typing import Optional, cast
from bittrade_huobi_websocket.models import RequestMessage, endpoints

from bittrade_huobi_websocket.rest.http_factory_decorator import http_factory
from bittrade_huobi_websocket.models.rest.get_all_open_orders import AllOpenOrdersParams


@http_factory
def get_all_open_orders_http_factory(params: AllOpenOrdersParams):
    return RequestMessage(
        "GET", endpoints.HuobiEndpoints.GET_ALL_OPEN_ORDERS, params=params.to_dict()
    )
