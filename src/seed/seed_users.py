from pymongo import MongoClient
import bcrypt
import uuid

MONGO_URI = "mongodb://mongodb:27017/" 
DATABASE_NAME = "todo_app"

adminId = str(uuid.uuid4())

# Seed data
users = [
    {   
        "id": str(uuid.uuid4()),
        "username": "testuser",
        "email": "testuser@example.com",
        "hashed_password": bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),  # Hash the password
        "is_active": True,
    },
    {
        "id": adminId,
        "username": "admin",
        "email": "admin@example.com",
        "hashed_password": bcrypt.hashpw("adminpassword".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        "is_active": True,
    },
]

admin_example_tasks = [
    {
        "id": str(uuid.uuid4()),
        "user_id": adminId,
        "title": "Admin Task 1",
        "description": "This is a task created by the admin user",
        "status": "pending",
        "created_at": "2021-08-01T10:00:00",
        "updated_at": "2021-08-01T10:00:00",
    },
    {
        "id": str(uuid.uuid4()),
        "user_id": adminId,
        "title": "Admin Task 2",
        "description": "This is another task created by the admin user",
        "status": "completed",
        "created_at": "2021-08-02T10:00:00",
        "updated_at": "2021-08-02T10:00:00",
    },
    {
        "id": str(uuid.uuid4()),
        "user_id": adminId,
        "title": "Admin Task 3",
        "description": "This is a third task created by the admin user",
        "status": "in-progress",
        "created_at": "2021-08-03T10:00:00",
        "updated_at": "2021-08-03T10:00:00",
    },
    {
        "id": str(uuid.uuid4()),
        "user_id": adminId,
        "title": "Admin Task 4",
        "description": "This is a fourth task created by the admin user",
        "status": "pending",
        "created_at": "2021-08-04T10:00:00",
        "updated_at": "2021-08-04T10:00:00",
    },
    {
        "id": str(uuid.uuid4()),
        "user_id": adminId,
        "title": "Admin Task 5",
        "description": "This is a fifth task created by the admin user",
        "status": "completed",
        "created_at": "2021-08-05T10:00:00",
        "updated_at": "2021-08-05T10:00:00",
    },
    {
        "id": str(uuid.uuid4()),
        "user_id": adminId,
        "title": "Admin Task 6",
        "description": "This is a sixth task created by the admin user",
        "status": "in-progress",
        "created_at": "2021-08-06T10:00:00",
        "updated_at": "2021-08-06T10:00:00",
    },
    {
        "id": str(uuid.uuid4()),
        "user_id": adminId,
        "title": "Admin Task 7",
        "description": "This is a seventh task created by the admin user",
        "status": "pending",
        "created_at": "2021-08-07T10:00:00",
        "updated_at": "2021-08-07T10:00:00",
    },
    {
        "id": str(uuid.uuid4()),
        "user_id": adminId,
        "title": "Admin Task 8",
        "description": "This is an eighth task created by the admin user",
        "status": "completed",
        "created_at": "2021-08-08T10:00:00",
        "updated_at": "2021-08-08T10:00:00",
    },
    {
        "id": str(uuid.uuid4()),
        "user_id": adminId,
        "title": "Admin Task 9",
        "description": "This is a ninth task created by the admin user",
        "status": "pending",
        "created_at": "2021-08-09T10:00:00",
        "updated_at": "2021-08-09T10:00:00",
    },
    {
        "id": str(uuid.uuid4()),
        "user_id": adminId,
        "title": "Admin Task 10",
        "description": "This is a tenth task created by the admin user",
        "status": "in-progress",
        "created_at": "2021-08-10T10:00:00",
        "updated_at": "2021-08-10T10:00:00",
    },
]

# Connect to MongoDB and insert users
def seed_users():
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    users_collection = db["users"]
    tasks_collection = db["tasks"]

    # Insert users if the collection is empty
    if users_collection.count_documents({}) == 0:
        users_collection.insert_many(users)
        print("Users seeded successfully!")
    else:
        print("Users already exist. Skipping seeding.")
        
    # Insert tasks if the collection is empty
    if tasks_collection.count_documents({}) == 0:
        tasks_collection.insert_many(admin_example_tasks)
        print("Tasks seeded successfully!")
    else:
        print("Tasks already exist. Skipping seeding.")

if __name__ == "__main__":
    seed_users()