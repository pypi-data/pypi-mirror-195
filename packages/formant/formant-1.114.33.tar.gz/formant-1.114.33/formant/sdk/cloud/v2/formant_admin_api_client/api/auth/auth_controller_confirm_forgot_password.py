from http import HTTPStatus
from typing import Any, Dict

import httpx

from ...client import Client
from ...models.confirm_forgot_password_request import ConfirmForgotPasswordRequest
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: ConfirmForgotPasswordRequest,
) -> Dict[str, Any]:
    url = "{}/auth/confirm-forgot-password".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    *,
    client: Client,
    json_body: ConfirmForgotPasswordRequest,
) -> Response[Any]:
    """Confirm forgot password

     Confirm Forgot Password

    Args:
        json_body (ConfirmForgotPasswordRequest):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: Client,
    json_body: ConfirmForgotPasswordRequest,
) -> Response[Any]:
    """Confirm forgot password

     Confirm Forgot Password

    Args:
        json_body (ConfirmForgotPasswordRequest):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
