from fa_purity.date_time import (
    DatetimeFactory,
)


def test_epoch() -> None:
    assert DatetimeFactory.EPOCH_START
