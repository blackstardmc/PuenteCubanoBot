import logging

import httpx

from bot.config import API_BASE_URL
from bot.api.exceptions import (
    ApiConnectionError,
    ApiResponseError,
    ApiTimeoutError,
)


logger = logging.getLogger(__name__)


class ApiClient:
    def __init__(self) -> None:
        self.base_url = API_BASE_URL.rstrip("/")

    async def _get(
        self,
        path: str,
        params: dict | None = None,
    ) -> dict:

        url = f"{self.base_url}/{path.lstrip('/')}"

        try:
            async with httpx.AsyncClient(
                timeout=10.0
            ) as client:

                response = await client.get(
                    url,
                    params=params,
                )

                response.raise_for_status()

                data = response.json()

                if not isinstance(data, dict):
                    raise ApiResponseError(
                        "La API devolvió un formato inesperado."
                    )

                return data

        except httpx.TimeoutException as error:
            logger.error(
                "Timeout consultando %s",
                url,
            )

            raise ApiTimeoutError(
                f"Timeout consultando {url}"
            ) from error

        except httpx.ConnectError as error:
            logger.error(
                "Error de conexión con %s",
                url,
            )

            raise ApiConnectionError(
                f"No se pudo conectar con {url}"
            ) from error

        except httpx.HTTPStatusError as error:
            logger.error(
                "HTTP %s consultando %s",
                error.response.status_code,
                url,
            )

            raise ApiResponseError(
                f"API respondió HTTP "
                f"{error.response.status_code}"
            ) from error

        except ValueError as error:
            logger.exception(
                "JSON inválido recibido desde %s",
                url,
            )

            raise ApiResponseError(
                "La API devolvió JSON inválido."
            ) from error

    async def get_products(self) -> dict:
        return await self._get(
            "/products/records"
        )

    async def get_combos(self) -> dict:
        return await self._get(
            "/combo/records",
            params={
                "page": 1,
                "perPage": 60,
            },
        )

    async def get_combo_exchanges(self) -> dict:
        return await self._get(
            "/comboExchange/records"
        )

    async def get_currencies(self) -> dict:
        return await self._get(
            "/currency/records"
        )

    async def get_exchanges(self) -> dict:
        return await self._get(
            "/exchange/records"
        )

    async def get_combo_categories(self) -> dict:
        return await self._get(
            "/comboCategory/records"
        )

    async def get_recharges(self) -> dict:
        return await self._get(
            "/recharge/records"
        )