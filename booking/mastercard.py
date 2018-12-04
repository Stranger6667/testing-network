import attr
from lxml import etree
from lxml.builder import E

from ..http import xml_request
from .exceptions import MasterCardAPIError


@attr.s()
class MasterCardAPIClient:
    """API client for MasterCard XML API."""

    ...

    def build_payload(self, *commands):
        """Build an XML payload for a request to MasterCard API."""
        payload = ...
        return payload

    async def _call(self, *commands):
        """Make a call to MasterCard API."""
        payload = self.build_payload(*commands)
        response = await xml_request(
            "POST", url=self.url, data=payload, verify_ssl=self.verify_ssl, cert=self.request_pem
        )
        parsed = etree.fromstring(response._body)
        error = parsed.find("Error")
        if error is not None:
            raise MasterCardAPIError(error)
        return parsed

    async def create_card(self, amount: str, currency: str):
        response = await self._call(
            E.CreatePurchaseRequest(Amount=amount, CurrencyCode=currency),
            E.ApprovePurchaseRequest(),
            E.GetCPNDetailsRequest(),
        )
