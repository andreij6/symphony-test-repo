import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from main import Task, TaskManager


def test_add_task():
    m = TaskManager()
    t = m.add("Hello")
    assert t.id == 1
    assert t.title == "Hello"
    assert not t.done


def test_complete_task():
    m = TaskManager()
    t = m.add("Do something")
    assert m.complete(t.id)
    assert m.list_pending() == []


def test_complete_missing_task():
    m = TaskManager()
    assert not m.complete(999)


def test_list_pending_filters_done():
    m = TaskManager()
    m.add("First")
    m.add("Second")
    m.complete(1)
    pending = m.list_pending()
    assert len(pending) == 1
    assert pending[0].title == "Second"


def test_tags():
    m = TaskManager()
    t = m.add("Tagged", tags=["alpha", "beta"])
    assert t.tags == ["alpha", "beta"]
