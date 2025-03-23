# Todo App API

## Run the API

```
docker-compose build && docker-compose -f docker-compose.yml up
```

## Run the tests

```
docker-compose -f docker-compose.override.yml up --build api
```

## Debug tests

```
docker-compose build && docker-compose -f docker-compose.yml up
docker exec -it todo-app-serverless-api-1 sh
pytest --maxfail=1 --disable-warnings -v
```

## Access mongo

```
docker exec -it todo-app-serverless-mongodb-1 mongosh
```

Then:

```
use todo_app
db.users.find().pretty()
```

## Extra

Check `seed_users.py` for initial seed and the Postman collection for API testing.