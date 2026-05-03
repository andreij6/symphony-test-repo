"""Simple task manager — starting point for Symphony agent tests."""

import json
from dataclasses import asdict, dataclass, field
from typing import Optional


@dataclass
class Task:
    id: int
    title: str
    done: bool = False
    priority: str = "Medium"
    tags: list[str] = field(default_factory=list)
    comments: list[str] = field(default_factory=list)


class TaskManager:
    def __init__(self, storage_path: Optional[str] = None) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id = 1
        self._storage_path = storage_path
        self._load()

    def _load(self) -> None:
        if not self._storage_path:
            return
        try:
            with open(self._storage_path) as f:
                data = json.load(f)
                self._tasks = {
                    int(k): Task(**v) for k, v in data.get("tasks", {}).items()
                }
                self._next_id = data.get("next_id", 1)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def _save(self) -> None:
        if not self._storage_path:
            return
        with open(self._storage_path, "w") as f:
            json.dump(
                {
                    "tasks": {k: asdict(v) for k, v in self._tasks.items()},
                    "next_id": self._next_id,
                },
                f,
                indent=2,
            )

    def add(
        self, title: str, tags: Optional[list[str]] = None, priority: str = "Medium"
    ) -> Task:
        task = Task(
            id=self._next_id,
            title=title,
            tags=list(tags) if tags else [],
            priority=priority,
        )
        self._tasks[self._next_id] = task
        self._next_id += 1
        self._save()
        return task

    def complete(self, task_id: int) -> bool:
        if task_id in self._tasks:
            self._tasks[task_id].done = True
            self._save()
            return True
        return False

    def add_comment(self, task_id: int, text: str) -> bool:
        if task_id in self._tasks:
            self._tasks[task_id].comments.append(text)
            self._save()
            return True
        return False

    def list_pending(self) -> list[Task]:
        return [t for t in self._tasks.values() if not t.done]

    def list_all(self) -> list[Task]:
        return list(self._tasks.values())


if __name__ == "__main__":
    manager = TaskManager("tasks.json")
    if not manager.list_all():
        manager.add("Write tests", tags=["dev"])
        manager.add("Update docs", tags=["docs"])
        manager.complete(1)

    print("Pending tasks:")
    for task in manager.list_pending():
        print(f"  [{task.id}] {task.title} {task.tags}")
