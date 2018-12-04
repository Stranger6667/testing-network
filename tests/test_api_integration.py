import pytest

pytestmark = [pytest.mark.asyncio]


@pytest.fixture
def mastercard():
    return MasterCardAPIClient()


async def test_create_card(mocker, mastercard):
    card = await mastercard.create_card(100, "EUR")
    assert card == {
        "amount": 100,
        "currency": "EUR",
        "number": mocker.ANY,
        "security_code": mocker.ANY,
        "holder": mocker.ANY,
    }
