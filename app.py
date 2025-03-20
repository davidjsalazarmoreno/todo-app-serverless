from chalice import Chalice, Response, BadRequestError, UnauthorizedError, NotFoundError
from src.services.task_service import TaskService
from src.services.auth_service import AuthService
from src.repositories.task_repository import TaskRepository
from src.repositories.user_repository import UserRepository
from src.utils.exceptions import TaskNotFoundException, AuthenticationException, UnauthorizedAccessException
import os
import json

app = Chalice(app_name='todo-api')

# Configuración
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key')

# Inicializar dependencias
task_repository = TaskRepository(MONGO_URI)
user_repository = UserRepository(MONGO_URI)
task_service = TaskService(task_repository)
auth_service = AuthService(user_repository, JWT_SECRET)

def get_current_user():
    auth_header = app.current_request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        raise UnauthorizedError("Bearer token required")
    
    token = auth_header.split(' ')[1]
    try:
        payload = auth_service.validate_token(token)
        return payload
    except AuthenticationException as e:
        raise UnauthorizedError(str(e))

@app.route('/login', methods=['POST'])
def login():
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
        return Response(
            body={"error": str(e)},
            status_code=401
        )
    except Exception as e:
        return Response(
            body={"error": "Internal server error"},
            status_code=500
        )

@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        user = get_current_user()
        tasks = task_service.get_all_tasks(user["user_id"])
        return {"tasks": [task.dict() for task in tasks]}
    except UnauthorizedError as e:
        return Response(
            body={"error": str(e)},
            status_code=401
        )
    except Exception as e:
        return Response(
            body={"error": "Internal server error"},
            status_code=500
        )

@app.route('/tasks/{task_id}', methods=['GET'])
def get_task(task_id):
    try:
        user = get_current_user()
        task = task_service.get_task_by_id(task_id, user["user_id"])
        return task.dict()
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
        return Response(
            body={"error": "Internal server error"},
            status_code=500
        )

@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        user = get_current_user()
        request_body = app.current_request.json_body
        task = task_service.create_task(request_body, user["user_id"])
        return Response(
            body=task.dict(),
            status_code=201
        )
    except UnauthorizedError as e:
        return Response(
            body={"error": str(e)},
            status_code=401
        )
    except Exception as e:
        return Response(
            body={"error": "Internal server error"},
            status_code=500
        )

@app.route('/tasks/{task_id}', methods=['PUT'])
def update_task(task_id):
    try:
        user = get_current_user()
        request_body = app.current_request.json_body
        task = task_service.update_task(task_id, request_body, user["user_id"])
        return task.dict()
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
        return Response(
            body={"error": "Internal server error"},
            status_code=500
        )

@app.route('/tasks/{task_id}', methods=['DELETE'])
def delete_task(task_id):
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
        return Response(
            body={"error": "Internal server error"},
            status_code=500
        )