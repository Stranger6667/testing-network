@pytest.mark.vcr()
def test_ancillaries_core():
    core = BigScaryClass("123", "test_service", "test", None)
    core.load_data()
    assert core.flights == {...}
    assert core.reservations == [...]
    assert core.segments == {...}
    assert core.passengers == {...}
