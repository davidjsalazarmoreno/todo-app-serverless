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

## Deployment

Create a test user, an user group and attach the following policies to the user group, then add the user to the user group.

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iam:CreateRole",
        "iam:PassRole",
        "iam:AttachRolePolicy",
        "iam:PutRolePolicy",
        "iam:GetRole",
        "lambda:*",
        "apigateway:*",
        "s3:*",
        "logs:*"
      ],
      "Resource": "*"
    }
  ]
}
```

Install the AWS Cli and configure your credentials, in OSX.

```
brew install awscli
```

Go to mongo atlas and create a free MongoDB cluster: https://cloud.mongodb.com/.

Get the Mongo URI and update the config.json.

The start the container and run chalice deploy

```
docker-compose build && docker-compose -f docker-compose.yml up
docker exec -it todo-app-serverless-api-1 sh
chalice deploy
```

## Extra

Check `seed_users.py` for initial seed and the Postman collection for API testing.