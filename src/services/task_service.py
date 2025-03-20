from ..models.task import Task
from ..repositories.task_repository import TaskRepository
from ..utils.exceptions import TaskNotFoundException, UnauthorizedAccessException

class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def get_all_tasks(self, user_id: str):
        return self.task_repository.find_all(user_id)

    def get_task_by_id(self, task_id: str, user_id: str):
        task = self.task_repository.find_by_id(task_id, user_id)
        if not task:
            raise TaskNotFoundException(f"Task with id {task_id} not found")
        return task

    def create_task(self, task_data: dict, user_id: str):
        task_data["user_id"] = user_id
        task = Task(**task_data)
        return self.task_repository.create(task)

    def update_task(self, task_id: str, task_data: dict, user_id: str):
        # Verificar si la tarea existe
        existing_task = self.get_task_by_id(task_id, user_id)
        
        success = self.task_repository.update(task_id, user_id, task_data)
        if not success:
            raise TaskNotFoundException(f"Failed to update task with id {task_id}")
        
        # Obtener la tarea actualizada
        return self.get_task_by_id(task_id, user_id)

    def delete_task(self, task_id: str, user_id: str):
        # Verificar si la tarea existe y pertenece al usuario
        self.get_task_by_id(task_id, user_id)
        
        success = self.task_repository.delete(task_id, user_id)
        if not success:
            raise TaskNotFoundException(f"Failed to delete task with id {task_id}")
        return True