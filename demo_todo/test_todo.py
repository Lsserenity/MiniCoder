import pytest

from todo import add_todo, get_todos, delete_todo, todos


def setup_function():
    todos.clear()


def test_add_todo():
    todo = add_todo("Learn Python")

    assert todo["id"] == 1
    assert todo["title"] == "Learn Python"
    assert todo["done"] is False


def test_get_todos():
    add_todo("Task A")
    add_todo("Task B")
    
    result = get_todos()
    
    assert len(result) == 2
    assert result[0]["title"] == "Task A"
    assert result[1]["title"] == "Task B"


def test_delete_todo():
    # Add a todo
    todo = add_todo("Task to delete")
    
    # Delete it
    deleted = delete_todo(todo["id"])
    
    # Verify it was deleted and returned correctly
    assert deleted["id"] == todo["id"]
    assert deleted["title"] == "Task to delete"
    assert deleted["done"] is False
    
    # Verify it's no longer in the list
    assert len(get_todos()) == 0


def test_delete_todo_missing_id():
    # Try to delete a non-existent todo
    with pytest.raises(KeyError, match="Todo with id 999 does not exist"):
        delete_todo(999)
