from http import HTTPStatus
from typing import Any, Dict

import httpx

from ...client import AuthenticatedClient
from ...types import Response


def _get_kwargs(
    key: str,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/key-value/{key}".format(client.base_url, key=key)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    key: str,
    *,
    client: AuthenticatedClient,
) -> Response[Any]:
    """Remove item

     Deletes a value for a given key
    Resource: keyValueStorage
    Authorized roles: operator

    Args:
        key (str):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        key=key,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    key: str,
    *,
    client: AuthenticatedClient,
) -> Response[Any]:
    """Remove item

     Deletes a value for a given key
    Resource: keyValueStorage
    Authorized roles: operator

    Args:
        key (str):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        key=key,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
