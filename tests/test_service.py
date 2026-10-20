import pytest

from taskmanager.service import TaskService
from taskmanager.storage import JsonStorage


@pytest.fixture
def service(tmp_path):
    return TaskService(JsonStorage(str(tmp_path / "tasks.json")))


def test_add_dan_persist(service, tmp_path):
    service.add("Tulis laporan", "high", "2026-12-01")
    reloaded = TaskService(JsonStorage(str(tmp_path / "tasks.json")))
    assert len(reloaded.tasks) == 1
    assert reloaded.tasks[0].priority == "high"


def test_complete_dan_stats(service):
    t = service.add("Satu")
    service.add("Dua")
    service.complete(t.id)
    assert service.stats()["done"] == 1
    assert service.stats()["pending"] == 1


def test_delete_dan_not_found(service):
    t = service.add("Hapus saya")
    service.delete(t.id)
    with pytest.raises(KeyError):
        service.get(t.id)


def test_urutan_prioritas(service):
    service.add("rendah", "low")
    service.add("tinggi", "high")
    assert [t.title for t in service.list_tasks()] == ["tinggi", "rendah"]


def test_overdue(service):
    service.add("Telat", due_date="2000-01-01")
    assert service.stats()["overdue"] == 1
