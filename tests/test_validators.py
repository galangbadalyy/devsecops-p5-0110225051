import pytest

from taskmanager.validators import validate_due_date, validate_priority, validate_title


def test_title_valid_dan_di_trim():
    assert validate_title("  Belajar CI/CD  ") == "Belajar CI/CD"


@pytest.mark.parametrize("bad", ["", "   ", None, "a" * 101])
def test_title_tidak_valid(bad):
    with pytest.raises(ValueError):
        validate_title(bad)


def test_priority():
    assert validate_priority("HIGH") == "high"
    with pytest.raises(ValueError):
        validate_priority("urgent")


def test_due_date():
    assert validate_due_date("2026-10-31") == "2026-10-31"
    assert validate_due_date("") is None
    with pytest.raises(ValueError):
        validate_due_date("31-10-2026")
