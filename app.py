from chalice import Chalice, Response, UnauthorizedError
from src.services.task_service import TaskService
from src.services.auth_service import AuthService
import traceback  # Add this import at the top of the file
from src.repositories.task_repository import TaskRepository
from src.repositories.user_repository import UserRepository
from src.utils.exceptions import TaskNotFoundException, AuthenticationException, UnauthorizedAccessException
import os
import json

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set the default logging level
logger = logging.getLogger(__name__)  # Create a logger for this module


app = Chalice(app_name='todo-api')

# Configuración Mongo for locaaaaallll and localhost for deploy
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://mongo:27017/')
JWT_SECRET = os.environ.get('JWT_SECRET', 'test-key-for-jwt-token')

# Inicializar dependencias
task_repository = TaskRepository(MONGO_URI)
user_repository = UserRepository(MONGO_URI)
task_service = TaskService(task_repository)
auth_service = AuthService(user_repository, JWT_SECRET)

from datetime import datetime


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# Add a blacklist to store invalidated tokens
invalidated_tokens = set()

def get_current_user():
    auth_header = app.current_request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        raise UnauthorizedError("Bearer token required")
    
    token = auth_header.split(' ')[1]
    if token in invalidated_tokens:  # Check if the token is invalidated
        logger.warning("Token is invalidated")
        raise UnauthorizedError("Invalid token")
    
    try:
        payload = auth_service.validate_token(token)
        logger.info(f"Authenticated user: {payload['user_id']}")  # Log the user ID
        return payload
    except AuthenticationException as e:
        logger.warning(f"Authentication failed: {str(e)}")
        raise UnauthorizedError(str(e))
    
@app.route('/health', methods=['GET'], api_key_required=False, cors=True)
def health_check():
    logger.info("Health check endpoint called")
    return {'status': 'healthy'}

@app.route('/api/v1/login', methods=['POST'], api_key_required=False, cors=True)
def login():
    logger.info("Login endpoint called")
    request_body = app.current_request.json_body
    try:
        username = request_body.get('username')
        password = request_body.get('password')
        
        if not username or not password:
            return Response(
                body={"error": "Username and password are required"},
                status_code=400
            )
        
        token = auth_service.authenticate(username, password)
        return {"token": token}
    except AuthenticationException as e:
        logger.warning(f"Authentication failed: {str(e)}")
        return Response(
            body={"error": str(e)},
            status_code=401
        )
    except Exception as e:
        logger.error("An error occurred during login", exc_info=True)
        return Response(
            body={"error": "Internal server error"},
            status_code=500
        )

@app.route('/api/v1/register', methods=['POST'], api_key_required=False, cors=True)  # Make the endpoint public
def register():
    logger.info("Register endpoint called")
    request_body = app.current_request.json_body
    try:
        username = request_body.get('username')
        email = request_body.get('email')
        password = request_body.get('password')

        if not username or not email or not password:
            return Response(
                body={"error": "Username, email, and password are required"},
                status_code=400
            )

        user = auth_service.register_user(username, email, password)
        return Response(
            body={"message": "User registered successfully", "user_id": user.id},
            status_code=201
        )
    except Exception as e:
        logger.error("An error occurred during user registration", exc_info=True)
        return Response(
            body={"error": "Internal server error"},
            status_code=500
        )

@app.route('/api/v1/tasks', methods=['GET'], cors=True)
def get_tasks():
    logger.info("Get tasks endpoint called")
    try:
        user = get_current_user()
        tasks = task_service.get_all_tasks(user["user_id"])
        return Response(
            body=json.dumps([task.dict() for task in tasks], cls=DateTimeEncoder),  
            status_code=200
        )
    except UnauthorizedError as e:
        return Response(
            body={"error": str(e)},
            status_code=401
        )
    except Exception as e:
        logger.error("An error occurred while fetching tasks", exc_info=True)
        return Response(
            body={"error": "Internal server error"},
            status_code=500
        )

@app.route('/api/v1/tasks/{task_id}', methods=['GET'], cors=True)
def get_task(task_id):
    logger.info(f"Get task endpoint called for task_id: {task_id}")
    try:
        user = get_current_user()
        task = task_service.get_task_by_id(task_id, user["user_id"])
        return json.dumps(task.dict(), cls=DateTimeEncoder)
    except TaskNotFoundException as e:
        return Response(
            body={"error": str(e)},
            status_code=404
        )
    except UnauthorizedError as e:
        return Response(
            body={"error": str(e)},
            status_code=401
        )
    except Exception as e:
        logger.error(f"An error occurred while fetching task {task_id}", exc_info=True)
        return Response(
            body={"error": "Internal server error"},
            status_code=500
        )

@app.route('/api/v1/tasks', methods=['POST'], cors=True)
def create_task():
    logger.info("Create task endpoint called")
    try:
        user = get_current_user()
        request_body = app.current_request.json_body
        task = task_service.create_task(request_body, user["user_id"])
        return Response(
            body=json.dumps(task.dict(), cls=DateTimeEncoder),
            status_code=201
        )
    except UnauthorizedError as e:
        return Response(
            body={"error": str(e)},
            status_code=401
        )
    except Exception as e:
        logger.error("An error occurred while creating a task", exc_info=True)
        return Response(
            body={"error": "Internal server error"},
            status_code=500
        )

@app.route('/api/v1/tasks/{task_id}', methods=['PUT'], cors=True)
def update_task(task_id):
    logger.info(f"Update task endpoint called for task_id: {task_id}")
    try:
        user = get_current_user()
        request_body = app.current_request.json_body
        task = task_service.update_task(task_id, request_body, user["user_id"])
        return json.dumps(task.dict(), cls=DateTimeEncoder)
    except TaskNotFoundException as e:
        return Response(
            body={"error": str(e)},
            status_code=404
        )
    except UnauthorizedError as e:
        return Response(
            body={"error": str(e)},
            status_code=401
        )
    except Exception as e:
        logger.error(f"An error occurred while updating task {task_id}", exc_info=True)
        return Response(
            body={"error": "Internal server error"},
            status_code=500
        )

@app.route('/api/v1/tasks/{task_id}', methods=['DELETE'], cors=True)
def delete_task(task_id):
    logger.info(f"Delete task endpoint called for task_id: {task_id}")
    try:
        user = get_current_user()
        task_service.delete_task(task_id, user["user_id"])
        return Response(
            body={"message": "Task deleted successfully"},
            status_code=200
        )
    except TaskNotFoundException as e:
        return Response(
            body={"error": str(e)},
            status_code=404
        )
    except UnauthorizedError as e:
        return Response(
            body={"error": str(e)},
            status_code=401
        )
    except Exception as e:
        logger.error(f"An error occurred while deleting task {task_id}", exc_info=True)
        return Response(
            body={"error": "Internal server error"},
            status_code=500
        )

@app.route('/api/v1/logout', methods=['POST'], cors=True)
def logout():
    logger.info("Logout endpoint called")
    try:
        user = get_current_user()
        auth_header = app.current_request.headers.get('Authorization', '')
        token = auth_header.split(' ')[1]
        invalidated_tokens.add(token)  
        logger.info(f"Token invalidated for user: {user['user_id']}")
        return Response(
            body={"message": "Logout successful"},
            status_code=200
        )
    except UnauthorizedError as e:
        return Response(
            body={"error": str(e)},
            status_code=401
        )
    except Exception as e:
        logger.error("An error occurred during logout", exc_info=True)
        return Response(
            body={"error": "Internal server error"},
            status_code=500
        )