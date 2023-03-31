# Week 6 — Deploying Containers
## Test RDS Connecetion

Add this `test` script into `db` so we can easily check our connection from our container.

```sh
#!/usr/bin/env python3

import psycopg
import os
import sys

connection_url = os.getenv("CONNECTION_URL")

conn = None
try:
  print('attempting connection')
  conn = psycopg.connect(connection_url)
  print("Connection successful!")
except psycopg.Error as e:
  print("Unable to connect to the database:", e)
finally:
  conn.close()
```
![connection to RDS](https://user-images.githubusercontent.com/125069098/229158230-2aa75030-923a-4762-af23-3179e4ce4c6e.png)

## Task Flask Script

We'll add the following endpoint for our flask app:
backend-flask/app.py

```py
@app.route('/api/health-check')
def health_check():
  return {'success': True}, 200
```

We'll create a new bin script at `bin/flask/health-check`

```py
#!/usr/bin/env python3

import urllib.request

try:
  response = urllib.request.urlopen('http://localhost:4567/api/health-check')
  if response.getcode() == 200:
    print("[OK] Flask server is running")
    exit(0) # success
  else:
    print("[BAD] Flask server is not running")
    exit(1) # false
# This for some reason is not capturing the error....
#except ConnectionRefusedError as e:
# so we'll just catch on all even though this is a bad practice
except Exception as e:
  print(e)
  exit(1) # false
```
![health-check](https://user-images.githubusercontent.com/125069098/229163202-67729059-13ae-4a23-a41f-47b0c1c5ec19.png)


## Create CloudWatch Log Group

```sh
aws logs create-log-group --log-group-name cruddur
aws logs put-retention-policy --log-group-name cruddur --retention-in-days 1
```
![cloudwatch logs](https://user-images.githubusercontent.com/125069098/229163072-d5937259-592a-4ac6-9c1b-90beb318610b.png)
![aws cloudwatch](https://user-images.githubusercontent.com/125069098/229163345-603be40d-d5be-4968-a0f6-4d1f6c1a46f0.png)

## Create ECS Cluster

```sh
aws ecs create-cluster \
--cluster-name cruddur \
--service-connect-defaults namespace=cruddur

![aws cli ecs creation](https://user-images.githubusercontent.com/125069098/229165475-8862ff64-d0a1-4c58-8916-a99cd4a706e1.png)
![aws console](https://user-images.githubusercontent.com/125069098/229165691-96f031aa-ddf8-4a01-a923-c674e96bd9cb.png)
![image](https://user-images.githubusercontent.com/125069098/229165931-532bc0a4-e45a-4fd2-8837-f8c9f75ddb81.png)


## Gaining Access to ECS Fargate Container

## Create ECR repo and push image

### For Base-image python

```sh
aws ecr create-repository \
  --repository-name cruddur-python \
  --image-tag-mutability MUTABLE
```
![ecr](https://user-images.githubusercontent.com/125069098/229171243-9aaffa5f-7c12-4a06-ac02-c6fe5d0a8c6c.png)
![aws ecr](https://user-images.githubusercontent.com/125069098/229171474-8ab6883e-fa3b-47d5-b4e7-f5b500714663.png)


### Login to ECR

```sh
aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com"
```
![login ecr](https://user-images.githubusercontent.com/125069098/229172613-5fd6063d-a8d3-4a45-bfaa-8bb58ac82d6c.png)

#### Set URL

```sh
export ECR_PYTHON_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/cruddur-python"
echo $ECR_PYTHON_URL
```
![image](https://user-images.githubusercontent.com/125069098/229172967-67fbfc48-af6f-4b64-a826-8e4ee7f50a52.png)


#### Pull Image

```sh
docker pull python:3.10-slim-buster
```
![docker pull](https://user-images.githubusercontent.com/125069098/229173406-7446f105-4750-4e41-b4cb-696ec5f7ec04.png)

#### Tag Image

```sh
docker tag python:3.10-slim-buster $ECR_PYTHON_URL:3.10-slim-buster
```
![image tag](https://user-images.githubusercontent.com/125069098/229173672-37e21833-2fa8-45d4-bab2-bce7296e0baf.png)

#### Push Image

```sh
docker push $ECR_PYTHON_URL:3.10-slim-buster
```
![docker push](https://user-images.githubusercontent.com/125069098/229173870-3f70eecc-0b7b-4889-915d-c980ab26e890.png)
![aws ecr](https://user-images.githubusercontent.com/125069098/229174052-739f9ce4-ea88-4007-91fb-3a16891c9659.png)

Replace the python image in the Dockerfile of backend-flask
```docker
FROM 480134889878.dkr.ecr.us-east-1.amazonaws.com/cruddur-python:3.10-slim-buster

WORKDIR /backend-flask

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_ENV=development

EXPOSE ${PORT}
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]
```
remove the local image 

![image](https://user-images.githubusercontent.com/125069098/229175299-ac54d344-c6ba-4828-a6ce-c49a7381ff3f.png)

### Test the Dockerfile is executable

 Login to ECR
```sh
aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com"
```
Do the **Docker compose up backend-flask db**

![image](https://user-images.githubusercontent.com/125069098/229176666-487eb03c-2c2a-4c8b-8c67-9aff4a7f1a15.png)

Open the backend port and do the health check of the backend app

![backend health-check](https://user-images.githubusercontent.com/125069098/229177022-cb862b97-d444-4055-acd1-da944a0416e8.png)

Later do the docker compose down to stop the docker compose

### For Flask

In your flask dockerfile update the from to instead of using DockerHub's python image
you use your own eg.

> remember to put the :latest tag on the end

#### Create Repo
```sh
aws ecr create-repository \
  --repository-name backend-flask \
  --image-tag-mutability MUTABLE
```
![repo for backend-flask](https://user-images.githubusercontent.com/125069098/229178831-14985b2e-b1f7-44b2-b107-2303b5b71f26.png)
![aws ecr](https://user-images.githubusercontent.com/125069098/229179223-a19a99fe-3848-4ce0-b11d-492292ee2176.png)


#### Set URL

```sh
export ECR_BACKEND_FLASK_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/backend-flask"
echo $ECR_BACKEND_FLASK_URL
```
![image](https://user-images.githubusercontent.com/125069098/229179149-f639d37d-cbbd-46d4-95a9-32d6cce169df.png)

Make sure you are in the backend-flask directory 
if get error make you login to ecr

#### Build Image
```sh
docker build -t backend-flask .
```
![image](https://user-images.githubusercontent.com/125069098/229179726-d053faa0-8fdb-468e-b9c1-0451f055e34c.png)
![image](https://user-images.githubusercontent.com/125069098/229180013-4c6719c2-e9a9-4f0f-91e3-243e2942fef7.png)

#### Tag Image

```sh
docker tag backend-flask:latest $ECR_BACKEND_FLASK_URL:latest
```

#### Push Image

```sh
docker push $ECR_BACKEND_FLASK_URL:latest
```
![docker push backend-flask](https://user-images.githubusercontent.com/125069098/229180363-9eb5040c-8aa7-41c5-9437-64776463dfb2.png)
![aws backend flask push](https://user-images.githubusercontent.com/125069098/229180490-fb936d11-074a-4789-9e7a-a0917fd6c188.png)

### For Frontend React

#### Create Repo
```sh
aws ecr create-repository \
  --repository-name frontend-react-js \
  --image-tag-mutability MUTABLE
```

#### Set URL

```sh
export ECR_FRONTEND_REACT_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/frontend-react-js"
echo $ECR_FRONTEND_REACT_URL
```

#### Build Image

```sh
docker build \
--build-arg REACT_APP_BACKEND_URL="https://4567-$GITPOD_WORKSPACE_ID.$GITPOD_WORKSPACE_CLUSTER_HOST" \
--build-arg REACT_APP_AWS_PROJECT_REGION="$AWS_DEFAULT_REGION" \
--build-arg REACT_APP_AWS_COGNITO_REGION="$AWS_DEFAULT_REGION" \
--build-arg REACT_APP_AWS_USER_POOLS_ID="ca-central-1_CQ4wDfnwc" \
--build-arg REACT_APP_CLIENT_ID="5b6ro31g97urk767adrbrdj1g5" \
-t frontend-react-js \
-f Dockerfile.prod \
.
```

#### Tag Image

```sh
docker tag frontend-react-js:latest $ECR_FRONTEND_REACT_URL:latest
```

#### Push Image

```sh
docker push $ECR_FRONTEND_REACT_URL:latest
```


If you want to run and test it

```sh
docker run --rm -p 3000:3000 -it frontend-react-js 
```

## Register Task Defintions

### Passing Senstive Data to Task Defintion
store the sensitive data in the AWS Systems Manager->Parameter Store

https://docs.aws.amazon.com/AmazonECS/latest/developerguide/specifying-sensitive-data.html
https://docs.aws.amazon.com/AmazonECS/latest/developerguide/secrets-envvar-ssm-paramstore.html

```sh
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/AWS_ACCESS_KEY_ID" --value $AWS_ACCESS_KEY_ID
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/AWS_SECRET_ACCESS_KEY" --value $AWS_SECRET_ACCESS_KEY
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/CONNECTION_URL" --value $PROD_CONNECTION_URL
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/ROLLBAR_ACCESS_TOKEN" --value $ROLLBAR_ACCESS_TOKEN
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/OTEL_EXPORTER_OTLP_HEADERS" --value "x-honeycomb-team=$HONEYCOMB_API_KEY"
```
![export OTEL_EXPORTER_OTLP_HEADERS](https://user-images.githubusercontent.com/125069098/229193969-784fbe69-ea25-41ce-92d7-9336007c76d1.png)
![paramstore](https://user-images.githubusercontent.com/125069098/229194796-610b7cd8-b045-4cdb-8dad-88114b1b4940.png)
![aws parameter store](https://user-images.githubusercontent.com/125069098/229195212-21760551-3e1e-46f0-90f0-385f752c7e99.png)

### Create Task and Exection Roles for Task Defintion


#### Create ExecutionRole
Create a file under aws/policies/service-execution-policy.json

```aws
aws iam create-role \
    --role-name CruddurServiceExecutionRole \
    --assume-role-policy-document
    file://aws/policies/service-execution-policy.json
```


```json
{
    "Version":"2012-10-17",
    "Statement":[{
      "Action":["sts:AssumeRole"],
      "Effect":"Allow",
      "Principal":{
        "Service":["ecs-tasks.amazonaws.com"]
      }
    }]
  }
```
```sh
aws iam create-role \    
--role-name CruddurServiceExecutionPolicy  \   
--assume-role-policy-document "file://aws/policies/service-assume-role-execution-policy.json"
```
![create role ](https://user-images.githubusercontent.com/125069098/229199730-14aa7d40-7d36-4d12-9939-8e087a258101.png)

```sh
aws iam put-role-policy \
  --policy-name CruddurServiceExecutionPolicy \
  --role-name CruddurServiceExecutionRole \
  --policy-document file://aws/policies/service-execution-policy.json
"
```
![image](https://user-images.githubusercontent.com/125069098/229200572-e94b932e-d08d-4669-b62a-c5c6697a3456.png)
![image](https://user-images.githubusercontent.com/125069098/229200976-31684082-50ae-47e4-babc-2838e5e786a6.png)
![image](https://user-images.githubusercontent.com/125069098/229201262-bd2a0796-acf5-457a-b46d-2ea288a76dc8.png)



```sh
aws iam attach-role-policy --policy-arn POLICY_ARN --role-name CruddurServiceExecutionRole
```



```json

       {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "ssm:GetParameter",
            "Resource": "arn:aws:ssm:ca-central-1:387543059434:parameter/cruddur/backend-flask/*"
        }
```
```sh
aws iam attach-role-policy \
    --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy \
    --role-name CruddurServiceExecutionRole
```

```json
{
  "Sid": "VisualEditor0",
  "Effect": "Allow",
  "Action": [
    "ssm:GetParameters",
    "ssm:GetParameter"
  ],
  "Resource": "arn:aws:ssm:ca-central-1:387543059434:parameter/cruddur/backend-flask/*"
}
```


