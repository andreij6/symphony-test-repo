"""Simple task manager — starting point for Symphony agent tests."""

from dataclasses import dataclass, field
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
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    def add(
        self, title: str, tags: Optional[list[str]] = None, priority: str = "Medium"
    ) -> Task:
        task = Task(
            id=self._next_id, title=title, tags=tags or [], priority=priority
        )
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def complete(self, task_id: int) -> bool:
        if task_id in self._tasks:
            self._tasks[task_id].done = True
            return True
        return False

    def add_comment(self, task_id: int, text: str) -> bool:
        if task_id in self._tasks:
            self._tasks[task_id].comments.append(text)
            return True
        return False

    def list_pending(self) -> list[Task]:
        return [t for t in self._tasks.values() if not t.done]

    def list_all(self) -> list[Task]:
        return list(self._tasks.values())


if __name__ == "__main__":
    manager = TaskManager()
    manager.add("Write tests", tags=["dev"])
    manager.add("Update docs", tags=["docs"])
    manager.complete(1)

    print("Pending tasks:")
    for task in manager.list_pending():
        print(f"  [{task.id}] {task.title} {task.tags}")
