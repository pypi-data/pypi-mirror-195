from datetime import datetime
import typing
import logging
import json
import asyncio

import httpx

logger = logging.getLogger(__name__)


class SDKClient:
    def __init__(
        self,
        *,
        event_url: str = "https://api.sumatra.ai/event",
        api_key: str,
    ):
        self._event_url = event_url
        self._api_key = api_key
        self._async_client: typing.Optional[httpx.AsyncClient] = None

    def track(self, event_type: str, **event: typing.Any) -> None:
        """Send an event to Sumatra synchronously

        :param event_type: the type of the event
        :param event: the data fields of the event
        """
        self.enrich(event_type, **event)

    def enrich(
        self, event_type: str, **event: typing.Any
    ) -> typing.Mapping[str, typing.Any]:
        """Send an event to Sumatra synchronously and return the enriched data

        :param event_type: the type of the event
        :param event: the data fields of the event

        :returns: the body of the response from Sumatra, including enriched features and any rules, decisions, or errors that occured.
        """
        event["_type"] = event_type
        logger.debug("Sending event", extra=event)
        post_time = datetime.now()
        response = httpx.post(
            f"{self._event_url}?features&decisions&rules",
            headers={"x-api-key": self._api_key},
            json=event,
        )
        response_time = round((datetime.now() - post_time).total_seconds() * 1000)
        logger.debug(f"Response Time: {response_time}ms")
        response.raise_for_status()
        return self._check_response(event_type, response.status_code, response.json())

    async def __aenter__(self) -> "SDKClient":
        if self._async_client is not None:
            return self
        self._async_client = httpx.AsyncClient()
        await self._async_client.__aenter__()
        return self

    async def __aexit__(self, *args) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        """Close the underlying httpx.AsyncClient if one is in use"""
        if self._async_client:
            await self._async_client.aclose()
            self._async_client = None

    async def track_async(self, event_type: str, **event: typing.Any) -> None:
        """Send an event to Sumatra asynchronously

        Usage:
        async with sumatra.SDKClient(...) as client:
            await client.track_async("event_type", **data)

        :param event_type: the type of the event
        :param event: the data fields of the event
        """
        await self.enrich_async(event_type, **event)

    async def enrich_async(
        self, event_type: str, **event: typing.Any
    ) -> typing.Mapping[str, typing.Any]:
        """Send an event to Sumatra asynchronously and return a future of the enriched data

        Usage:
        async with sumatra.SDKClient(...) as client:
            response = await client.enrich_async("event_type", **data)
            response["features"]

        :param event_type: the type of the event
        :param event: the data fields of the event

        :returns: the body of the response from Sumatra, including enriched features and any rules, decisions, or errors that occured.
        """
        if self._async_client is None:
            await self.__aenter__()
            assert self._async_client is not None  # type hint

        event["_type"] = event_type
        logger.debug("Sending async event", extra=event)
        post_time = datetime.now()
        response = await self._async_client.post(
            f"{self._event_url}?features&decisions&rules",
            headers={"x-api-key": self._api_key},
            json=event,
        )
        response_time = round((datetime.now() - post_time).total_seconds() * 1000)
        logger.debug(f"Response Time: {response_time}ms")
        response.raise_for_status()
        return self._check_response(event_type, response.status_code, response.json())

    def _check_response(
        self, event_type: str, status_code: int, response: typing.Dict
    ) -> typing.Dict:
        logger.debug("Event response", extra=response)
        if "event_id" not in response:
            raise RuntimeError(
                f"Sumatra returned {status_code}: {json.dumps(response)}"
            )
        if "errors" in response:
            for feature, e in response["errors"].items():
                logger.error(
                    f"{event_type} {response.get('event_id', '')} feature '{feature}': {e}",
                    extra={
                        "_type": event_type,
                        "event_id": response.get("event_id"),
                        "feature": feature,
                        "error": e,
                    },
                )
        return response
