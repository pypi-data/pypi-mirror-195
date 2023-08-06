import typing

from .client import SDKClient

try:
    import sumatra_client
    from sumatra_client import *
except ImportError:
    sumatra_client = None


event_url = "https://api.sumatra.ai/event"
api_key = None
_default_client = None


def _get_or_create_client() -> SDKClient:
    global _default_client
    if _default_client is not None:
        return _default_client

    if not event_url or not api_key:
        raise ValueError("sumatra_sdk.event_url and sumatra_sdk.api_key must be set")
    _default_client = SDKClient(event_url=event_url, api_key=api_key)
    return _default_client


def track(event_type: str, **event: typing.Any) -> None:
    """Send an event to Sumatra synchronously

    Usage:
    import sumatra_sdk
    sumatra_sdk.api_key = "***"
    sumatra_sdk.track("event_type", **data)

    :param event_type: the type of the event
    :param event: the data fields of the event
    """
    client = _get_or_create_client()
    client.track(event_type, **event)


def enrich(event_type: str, **event: typing.Any) -> typing.Mapping[str, typing.Any]:
    """Send an event to Sumatra synchronously and return the enriched data

    Usage:
    import sumatra_sdk
    sumatra_sdk.api_key = "***"
    response = sumatra_sdk.enrich("event_type", **data)
    response["features"]

    :param event_type: the type of the event
    :param event: the data fields of the event

    :returns: the body of the response from Sumatra, including enriched features and any rules, decisions, or errors that occured.
    """
    client = _get_or_create_client()
    return client.enrich(event_type, **event)


__all__ = [
    "SDKClient",
    "api_key",
    "event_url",
    "track",
    "enrich",
]

if sumatra_client:
    __all__ += sumatra_client.__all__
