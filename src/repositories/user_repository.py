from pymongo import MongoClient
from ..models.user import User

class UserRepository:
    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client.todo_app
        self.collection = self.db.users

    def find_by_id(self, user_id: str):
        user = self.collection.find_one({"id": user_id})
        if user:
            return User(**user)
        return None

    def find_by_username(self, username: str):
        user = self.collection.find_one({"username": username})
        if user:
            return User(**user)
        return None

    def find_by_email(self, email: str):
        user = self.collection.find_one({"email": email})
        if user:
            return User(**user)
        return None

    def create(self, user: User):
        user_dict = user.dict()
        result = self.collection.insert_one(user_dict)
        return user

    def update(self, user_id: str, user_data: dict):
        user_data["updated_at"] = datetime.now()
        result = self.collection.update_one(
            {"id": user_id},
            {"$set": user_data}
        )
        return result.modified_count > 0

    def delete(self, user_id: str):
        result = self.collection.delete_one({"id": user_id})
        return result.deleted_count > 0