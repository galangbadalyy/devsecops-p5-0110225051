"""Logika bisnis TaskManager."""
from typing import List, Optional

from .models import Task
from .storage import JsonStorage
from .validators import validate_due_date, validate_priority, validate_title

_PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


class TaskService:
    def __init__(self, storage: JsonStorage):
        self.storage = storage
        self.tasks: List[Task] = storage.load()

    def _next_id(self) -> int:
        return max((t.id for t in self.tasks), default=0) + 1

    def add(self, title: str, priority: str = "medium", due_date: Optional[str] = None) -> Task:
        task = Task(
            id=self._next_id(),
            title=validate_title(title),
            priority=validate_priority(priority),
            due_date=validate_due_date(due_date),
        )
        self.tasks.append(task)
        self.storage.save(self.tasks)
        return task

    def get(self, task_id: int) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise KeyError(f"Tugas dengan id {task_id} tidak ditemukan")

    def complete(self, task_id: int) -> Task:
        task = self.get(task_id)
        task.done = True
        self.storage.save(self.tasks)
        return task

    def delete(self, task_id: int) -> None:
        task = self.get(task_id)
        self.tasks.remove(task)
        self.storage.save(self.tasks)

    def list_tasks(self, only_pending: bool = False) -> List[Task]:
        items = [t for t in self.tasks if not (only_pending and t.done)]
        return sorted(items, key=lambda t: (_PRIORITY_ORDER[t.priority], t.id))

    def stats(self) -> dict:
        total = len(self.tasks)
        done = sum(1 for t in self.tasks if t.done)
        return {
            "total": total,
            "done": done,
            "pending": total - done,
            "overdue": sum(1 for t in self.tasks if t.is_overdue()),
        }
