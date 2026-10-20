"""Validasi input pengguna."""
from datetime import date

VALID_PRIORITIES = ("low", "medium", "high")
MAX_TITLE_LENGTH = 100


def validate_title(title: str) -> str:
    title = (title or "").strip()
    if not title:
        raise ValueError("Judul tugas tidak boleh kosong")
    if len(title) > MAX_TITLE_LENGTH:
        raise ValueError(f"Judul maksimal {MAX_TITLE_LENGTH} karakter")
    return title


def validate_priority(priority: str) -> str:
    priority = (priority or "").strip().lower()
    if priority not in VALID_PRIORITIES:
        raise ValueError(f"Prioritas harus salah satu dari {VALID_PRIORITIES}")
    return priority


def validate_due_date(value):
    """Mengembalikan string ISO yang valid, atau None jika kosong."""
    if value is None or str(value).strip() == "":
        return None
    try:
        return date.fromisoformat(str(value).strip()).isoformat()
    except ValueError as exc:
        raise ValueError("Format tanggal harus YYYY-MM-DD") from exc
