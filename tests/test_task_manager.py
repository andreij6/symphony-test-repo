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


def test_add_comment():
    m = TaskManager()
    t = m.add("Review code")
    assert m.add_comment(t.id, "Looks good")
    assert m.add_comment(t.id, "Needs tests")
    assert t.comments == ["Looks good", "Needs tests"]


def test_add_comment_missing_task():
    m = TaskManager()
    assert not m.add_comment(999, "nope")


def test_empty_comments_on_new_task():
    m = TaskManager()
    t = m.add("Fresh task")
    assert t.comments == []


def test_category_defaults_to_none():
    m = TaskManager()
    t = m.add("No category")
    assert t.category is None


def test_add_task_with_category():
    m = TaskManager()
    t = m.add("Design spec", category="work")
    assert t.category == "work"


def test_list_by_category():
    m = TaskManager()
    m.add("Work task 1", category="work")
    m.add("Personal task", category="personal")
    m.add("Work task 2", category="work")
    work = m.list_by_category("work")
    assert len(work) == 2
    assert all(t.category == "work" for t in work)


def test_list_by_category_no_match():
    m = TaskManager()
    m.add("Task", category="work")
    assert m.list_by_category("personal") == []
