"""Simple task manager — starting point for Symphony agent tests."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    id: int
    title: str
    done: bool = False
    tags: list[str] = field(default_factory=list)
    description: str = ""


class TaskManager:
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    def add(self, title: str, tags: Optional[list[str]] = None, description: str = "") -> Task:
        task = Task(id=self._next_id, title=title, tags=tags or [], description=description)
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def complete(self, task_id: int) -> bool:
        if task_id in self._tasks:
            self._tasks[task_id].done = True
            return True
        return False

    def list_pending(self) -> list[Task]:
        return [t for t in self._tasks.values() if not t.done]

    def list_all(self) -> list[Task]:
        return list(self._tasks.values())


if __name__ == "__main__":
    manager = TaskManager()
    manager.add("Write tests", tags=["dev"], description="Cover all edge cases")
    manager.add("Update docs", tags=["docs"], description="Add API reference section")
    manager.complete(1)

    print("Pending tasks:")
    for task in manager.list_pending():
        print(f"  [{task.id}] {task.title} {task.tags}")
