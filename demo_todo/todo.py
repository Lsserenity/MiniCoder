todos = []


def add_todo(title: str) -> dict:
    todo = {
        "id": len(todos) + 1,
        "title": title,
        "done": False,
    }

    todos.append(todo)

    return todo


def get_todos() -> list:
    return todos


def delete_todo(todo_id: int) -> dict:
    """Delete and return the todo with the given id.
    
    Args:
        todo_id: The id of the todo to delete
        
    Returns:
        The deleted todo dictionary
        
    Raises:
        KeyError: If the todo with the given id does not exist
    """
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            return todos.pop(i)
    raise KeyError(f"Todo with id {todo_id} does not exist")


def update_todo(todo_id: int, title: str = None, done: bool = None) -> dict:
    """Update and return the todo with the given id.
    
    Args:
        todo_id: The id of the todo to update
        title: Optional new title for the todo
        done: Optional new status for the todo
        
    Returns:
        The updated todo dictionary
        
    Raises:
        KeyError: If the todo with the given id does not exist
    """
    for todo in todos:
        if todo["id"] == todo_id:
            if title is not None:
                todo["title"] = title
            if done is not None:
                todo["done"] = done
            return todo
    raise KeyError(f"Todo with id {todo_id} does not exist")