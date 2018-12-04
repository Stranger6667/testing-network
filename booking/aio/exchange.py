from decimal import Decimal

import aiohttp

from ..exceptions import NoExchangeRateError


async def to_eur(amount: Decimal, currency: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "http://127.0.0.1:5000/to_eur", params={"amount": str(amount), "currency": currency}
        ) as response:
            data = await response.json()
            try:
                response.raise_for_status()
            except aiohttp.ClientResponseError:
                if data["detail"] == "No such rate":
                    raise NoExchangeRateError
                raise
            return Decimal(data["result"])
