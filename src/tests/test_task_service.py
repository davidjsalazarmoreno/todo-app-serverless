import pytest
from unittest.mock import MagicMock, patch
from src.services.task_service import TaskService
from src.models.task import Task
from src.utils.exceptions import TaskNotFoundException

@pytest.fixture
def task_repository():
    return MagicMock()

@pytest.fixture
def task_service(task_repository):
    return TaskService(task_repository)

def test_get_all_tasks(task_service, task_repository):
    # Arrange
    user_id = "user123"
    expected_tasks = [
        Task(id="task1", title="Task 1", user_id=user_id),
        Task(id="task2", title="Task 2", user_id=user_id)
    ]
    task_repository.find_all.return_value = expected_tasks
    
    # Act
    result = task_service.get_all_tasks(user_id)
    
    # Assert
    task_repository.find_all.assert_called_once_with(user_id)
    assert result == expected_tasks

def test_get_task_by_id(task_service, task_repository):
    # Arrange
    task_id = "task1"
    user_id = "user123"
    expected_task = Task(id=task_id, title="Task 1", user_id=user_id)
    task_repository.find_by_id.return_value = expected_task
    
    # Act
    result = task_service.get_task_by_id(task_id, user_id)
    
    # Assert
    task_repository.find_by_id.assert_called_once_with(task_id, user_id)
    assert result == expected_task

def test_get_task_by_id_not_found(task_service, task_repository):
    # Arrange
    task_id = "nonexistent"
    user_id = "user123"
    task_repository.find_by_id.return_value = None
    
    # Act & Assert
    with pytest.raises(TaskNotFoundException):
        task_service.get_task_by_id(task_id, user_id)

def test_create_task(task_service, task_repository):
    # Arrange
    user_id = "user123"
    task_data = {"title": "New Task"}
    expected_task = Task(id="task1", title="New Task", user_id=user_id)
    task_repository.create.return_value = expected_task
    
    # Act
    result = task_service.create_task(task_data, user_id)
    
    # Assert
    assert result == expected_task
    task_repository.create.assert_called_once()
    # Verificar que user_id se haya añadido a los datos de la tarea
    assert task_repository.create.call_args[0][0].user_id == user_id

def test_update_task(task_service, task_repository):
    # Arrange
    task_id = "task1"
    user_id = "user123"
    task_data = {"status": "completed"}
    existing_task = Task(id=task_id, title="Task 1", user_id=user_id)
    updated_task = Task(id=task_id, title="Task 1", status="completed", user_id=user_id)
    
    task_repository.find_by_id.side_effect = [existing_task, updated_task]
    task_repository.update.return_value = True
    
    # Act
    result = task_service.update_task(task_id, task_data, user_id)
    
    # Assert
    task_repository.update.assert_called_once_with(task_id, user_id, task_data)
    assert result == updated_task

def test_delete_task(task_service, task_repository):
    # Arrange
    task_id = "task1"
    user_id = "user123"
    existing_task = Task(id=task_id, title="Task 1", user_id=user_id)
    
    task_repository.find_by_id.return_value = existing_task
    task_repository.delete.return_value = True
    
    # Act
    result = task_service.delete_task(task_id, user_id)
    
    # Assert
    task_repository.delete.assert_called_once_with(task_id, user_id)
    assert result is True