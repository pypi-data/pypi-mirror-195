from typing import Optional
from contextvars import ContextVar, Token

REQUEST_ID_CTX_KEY = 'request_id'

_request_id_ctx_var: ContextVar[Optional[str]] = ContextVar(REQUEST_ID_CTX_KEY, default=None)


def get_request_id() -> Optional[str]:
    return _request_id_ctx_var.get()


def set_request_id(value: str) -> Token:
    return _request_id_ctx_var.set(value)


def reset_request_id(token: Token):
    _request_id_ctx_var.reset(token)


def get_headers(headers: dict = None) -> dict:
    if headers is None:
        headers = {}
    headers.update({
        'X-Request-ID': get_request_id()
    })
    return headers
