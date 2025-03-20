from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from ..models.task import Task

class TaskRepository:
    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client.todo_app
        self.collection = self.db.tasks

    def find_all(self, user_id: str):
        tasks = self.collection.find({"user_id": user_id})
        return [Task(**task) for task in tasks]

    def find_by_id(self, task_id: str, user_id: str):
        task = self.collection.find_one({"id": task_id, "user_id": user_id})
        if task:
            return Task(**task)
        return None

    def create(self, task: Task):
        task_dict = task.dict()
        result = self.collection.insert_one(task_dict)
        return task

    def update(self, task_id: str, user_id: str, task_data: dict):
        task_data["updated_at"] = datetime.now()
        result = self.collection.update_one(
            {"id": task_id, "user_id": user_id},
            {"$set": task_data}
        )
        return result.modified_count > 0

    def delete(self, task_id: str, user_id: str):
        result = self.collection.delete_one({"id": task_id, "user_id": user_id})
        return result.deleted_count > 0