import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from main import Task, TaskManager


def test_add_task(tmp_path):
    storage = tmp_path / "tasks.json"
    m = TaskManager(storage)
    t = m.add("Hello")
    assert t.id == 1
    assert t.title == "Hello"
    assert not t.done
    assert t.priority == "Medium"


def test_add_task_with_priority(tmp_path):
    storage = tmp_path / "tasks.json"
    m = TaskManager(storage)
    t = m.add("High priority task", priority="High")
    assert t.priority == "High"


def test_complete_task(tmp_path):
    storage = tmp_path / "tasks.json"
    m = TaskManager(storage)
    t = m.add("Do something")
    assert m.complete(t.id)
    assert m.list_pending() == []


def test_complete_missing_task(tmp_path):
    storage = tmp_path / "tasks.json"
    m = TaskManager(storage)
    assert not m.complete(999)


def test_list_pending_filters_done(tmp_path):
    storage = tmp_path / "tasks.json"
    m = TaskManager(storage)
    m.add("First")
    m.add("Second")
    m.complete(1)
    pending = m.list_pending()
    assert len(pending) == 1
    assert pending[0].title == "Second"


def test_tags(tmp_path):
    storage = tmp_path / "tasks.json"
    m = TaskManager(storage)
    t = m.add("Tagged", tags=["alpha", "beta"])
    assert t.tags == ["alpha", "beta"]


def test_add_comment(tmp_path):
    storage = tmp_path / "tasks.json"
    m = TaskManager(storage)
    t = m.add("Review code")
    assert m.add_comment(t.id, "Looks good")
    assert m.add_comment(t.id, "Needs tests")
    assert t.comments == ["Looks good", "Needs tests"]


def test_add_comment_missing_task(tmp_path):
    storage = tmp_path / "tasks.json"
    m = TaskManager(storage)
    assert not m.add_comment(999, "nope")


def test_empty_comments_on_new_task(tmp_path):
    storage = tmp_path / "tasks.json"
    m = TaskManager(storage)
    t = m.add("Fresh task")
    assert t.comments == []


def test_persistence(tmp_path):
    storage = tmp_path / "tasks.json"
    m1 = TaskManager(storage)
    m1.add("A task")

    m2 = TaskManager(storage)
    tasks = m2.list_all()
    assert len(tasks) == 1
    assert tasks[0].title == "A task"


def test_comment_persistence(tmp_path):
    storage = tmp_path / "tasks.json"
    m1 = TaskManager(storage)
    t = m1.add("A task")
    m1.add_comment(t.id, "A comment")

    m2 = TaskManager(storage)
    tasks = m2.list_all()
    assert len(tasks) == 1
    assert tasks[0].comments == ["A comment"]


def test_like_task(tmp_path):
    storage = tmp_path / "tasks.json"
    m = TaskManager(storage)
    t = m.add("Like me")
    assert t.likes == 0
    assert m.like(t.id)
    assert t.likes == 1
    assert m.like(t.id)
    assert t.likes == 2


def test_like_missing_task(tmp_path):
    storage = tmp_path / "tasks.json"
    m = TaskManager(storage)
    assert not m.like(999)


def test_like_persistence(tmp_path):
    storage = tmp_path / "tasks.json"
    m1 = TaskManager(storage)
    t = m1.add("Like me")
    m1.like(t.id)
    m1.like(t.id)

    m2 = TaskManager(storage)
    tasks = m2.list_all()
    assert len(tasks) == 1
    assert tasks[0].likes == 2
