from pymongo import MongoClient
import bcrypt

# MongoDB connection URI
MONGO_URI = "mongodb://mongodb:27017/"  # Use "mongodb" if running inside the container
DATABASE_NAME = "todo_app"

# Seed data
users = [
    {
        "username": "testuser",
        "email": "testuser@example.com",
        "hashed_password": bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),  # Hash the password
        "is_active": True,
    },
    {
        "username": "admin",
        "email": "admin@example.com",
        "hashed_password": bcrypt.hashpw("adminpassword".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        "is_active": True,
    },
]

# Connect to MongoDB and insert users
def seed_users():
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    users_collection = db["users"]

    # Insert users if the collection is empty
    if users_collection.count_documents({}) == 0:
        users_collection.insert_many(users)
        print("Users seeded successfully!")
    else:
        print("Users already exist. Skipping seeding.")

if __name__ == "__main__":
    seed_users()