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
/app.py

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
```
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
![CruddurServiceExecutionRole](https://user-images.githubusercontent.com/125069098/229220490-29409b37-eda8-48f6-ac2b-ce9167d98378.png)
![CruddurServiceExecutionPolicy](https://user-images.githubusercontent.com/125069098/229220564-0eaf7a83-334b-4657-8560-b694d19bf7c8.png)

#### Create TaskRole

```sh
aws iam create-role \
    --role-name CruddurTaskRole \
    --assume-role-policy-document "{
  \"Version\":\"2012-10-17\",
  \"Statement\":[{
    \"Action\":[\"sts:AssumeRole\"],
    \"Effect\":\"Allow\",
    \"Principal\":{
      \"Service\":[\"ecs-tasks.amazonaws.com\"]
    }
  }]
}"
![CruddurTaskRole](https://user-images.githubusercontent.com/125069098/229221764-0d2f993e-a7d5-4882-af57-53501f30a0a0.png)

aws iam put-role-policy \
  --policy-name SSMAccessPolicy \
  --role-name CruddurTaskRole \
  --policy-document "{
  \"Version\":\"2012-10-17\",
  \"Statement\":[{
    \"Action\":[
      \"ssmmessages:CreateControlChannel\",
      \"ssmmessages:CreateDataChannel\",
      \"ssmmessages:OpenControlChannel\",
      \"ssmmessages:OpenDataChannel\"
    ],
    \"Effect\":\"Allow\",
    \"Resource\":\"*\"
  }]
}"

aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/CloudWatchFullAccess --role-name CruddurTaskRole
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess --role-name CruddurTaskRole
```
![CruddurTaskRole](https://user-images.githubusercontent.com/125069098/229221764-0d2f993e-a7d5-4882-af57-53501f30a0a0.png)
![image](https://user-images.githubusercontent.com/125069098/229228900-0fcdfb72-9df0-4d2d-bbf1-8e85be20cacb.png)


### Create Json file
Create a new folder called `aws/task-defintions` and place the following files in there:
fill all the values with your account.

`backend-flask.json`

```json
{
  "family": "backend-flask",
  "executionRoleArn": "arn:aws:iam::AWS_ACCOUNT_ID:role/CruddurServiceExecutionRole",
  "taskRoleArn": "arn:aws:iam::AWS_ACCOUNT_ID:role/CruddurTaskRole",
  "networkMode": "awsvpc",
  "containerDefinitions": [
    {
      "name": "backend-flask",
      "image": "BACKEND_FLASK_IMAGE_URL",
      "cpu": 256,
      "memory": 512,
      "essential": true,
      "portMappings": [
        {
          "name": "backend-flask",
          "containerPort": 4567,
          "protocol": "tcp", 
          "appProtocol": "http"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
            "awslogs-group": "cruddur",
            "awslogs-region": "ca-central-1",
            "awslogs-stream-prefix": "backend-flask"
        }
      },
      "environment": [
        {"name": "OTEL_SERVICE_NAME", "value": "backend-flask"},
        {"name": "OTEL_EXPORTER_OTLP_ENDPOINT", "value": "https://api.honeycomb.io"},
        {"name": "AWS_COGNITO_USER_POOL_ID", "value": ""},
        {"name": "AWS_COGNITO_USER_POOL_CLIENT_ID", "value": ""},
        {"name": "FRONTEND_URL", "value": ""},
        {"name": "BACKEND_URL", "value": ""},
        {"name": "AWS_DEFAULT_REGION", "value": ""}
      ],
      "secrets": [
        {"name": "AWS_ACCESS_KEY_ID"    , "valueFrom": "arn:aws:ssm:AWS_REGION:AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/AWS_ACCESS_KEY_ID"},
        {"name": "AWS_SECRET_ACCESS_KEY", "valueFrom": "arn:aws:ssm:AWS_REGION:AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/AWS_SECRET_ACCESS_KEY"},
        {"name": "CONNECTION_URL"       , "valueFrom": "arn:aws:ssm:AWS_REGION:AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/CONNECTION_URL" },
        {"name": "ROLLBAR_ACCESS_TOKEN" , "valueFrom": "arn:aws:ssm:AWS_REGION:AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/ROLLBAR_ACCESS_TOKEN" },
        {"name": "OTEL_EXPORTER_OTLP_HEADERS" , "valueFrom": "arn:aws:ssm:AWS_REGION:AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/OTEL_EXPORTER_OTLP_HEADERS" }
        
      ]
    }
  ]
}
```
### Register Task Defintion

```sh
aws ecs register-task-definition --cli-input-json file://aws/task-definitions/backend-flask.json
```
```sh
aws ecs register-task-definition --cli-input-json file://aws/task-definitions/frontend-react-js.json
```

![execute task definition](https://user-images.githubusercontent.com/125069098/229232724-ad7d9afb-ec79-4c4d-92a6-132c47fa8867.png)

![AWS task definition](https://user-images.githubusercontent.com/125069098/229233639-1eb5fe23-67f0-4c4b-85fd-3db011baeed1.png)
![image](https://user-images.githubusercontent.com/125069098/229234003-92c55bd6-c3ca-435e-8e72-f007f7eded3a.png)
![image](https://user-images.githubusercontent.com/125069098/229234213-baf606a5-2ab1-4ee7-aa5e-5d859b004b8f.png)

Create a cluster service in the AWS console
![image](https://user-images.githubusercontent.com/125069098/229541330-72892a86-591c-4865-a56b-753dc0157b82.png)
![image](https://user-images.githubusercontent.com/125069098/229541446-2eac26c5-b4e8-44bb-b9e9-f79f459c629b.png)
![image](https://user-images.githubusercontent.com/125069098/229543423-c73eaf80-738b-44bd-91fc-2e103eeb310c.png)

## Defaults

```sh
export DEFAULT_VPC_ID=$(aws ec2 describe-vpcs \
--filters "Name=isDefault, Values=true" \
--query "Vpcs[0].VpcId" \
--output text)
echo $DEFAULT_VPC_ID
```

```sh
export DEFAULT_SUBNET_IDS=$(aws ec2 describe-subnets  \
 --filters Name=vpc-id,Values=$DEFAULT_VPC_ID \
 --query 'Subnets[*].SubnetId' \
 --output json | jq -r 'join(",")')
echo $DEFAULT_SUBNET_IDS
```

### Create Security Group
```sh
export CRUD_SERVICE_SG=$(aws ec2 create-security-group \
  --group-name "crud-srv-sg" \
  --description "Security group for Cruddur services on ECS" \
  --vpc-id $DEFAULT_VPC_ID \
  --query "GroupId" --output text)
echo $CRUD_SERVICE_SG
```
```sh
aws ec2 authorize-security-group-ingress \
  --group-id $CRUD_SERVICE_SG \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0
```
![export default vpc subnet sg sg ingress](https://user-images.githubusercontent.com/125069098/229538081-8755eb88-73c6-42d4-8d3c-9791754b3c86.png)


Edit more permission to ECR to execute ECS

![edit CruddurServiceExecutionPolicy](https://user-images.githubusercontent.com/125069098/229241613-8b184c9f-b2bc-4e48-9f64-ec5e6fea8e3d.png)

![ECS cluster backendflask](https://user-images.githubusercontent.com/125069098/229568419-bc6e376b-5d12-4479-adb2-7595d4008c74.png)

### Connection via Sessions Manaager (Fargate)
 
 https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html#install-plugin-linux
 https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html#install-plugin-verify
 
 Install for Ubuntu
 ```sh
 curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb" -o "session-manager-plugin.deb"
 sudo dpkg -i session-manager-plugin.deb
 ```
 
 Verify its working
 ```sh
 session-manager-plugin
 ```
 ![image](https://user-images.githubusercontent.com/125069098/229573754-6cbe0eb4-9bd2-405e-96a5-a25cb5db52d6.png)

Connect to the container
 ```sh
aws ecs execute-command  \
--region $AWS_DEFAULT_REGION \
--cluster cruddur \
--task b48a8ba003c54582bd40806040067118 \
--container backend-flask \
--command "/bin/bash" \
--interactive
```
### Create ECS cluster Service using json aws cli
create a new file under aws/json/service-backend-flask.json

```json
{
    "cluster": "cruddur",
    "launchType": "FARGATE",
    "desiredCount": 1,
    "enableECSManagedTags": true,
    "enableExecuteCommand": true,
    "networkConfiguration": {
      "awsvpcConfiguration": {
        "assignPublicIp": "ENABLED",
        "securityGroups": [
          "sg-0a9faf8a5b6cebc28"
        ],
        "subnets": [
          "subnet-016ecab3f1da8fb43",
          "subnet-0e4e64945affecd2f",
          "subnet-0b065d59d38f227f9",
          "subnet-0ac5fc3e0dbde243f",
          "subnet-0901ddcc3e5892f8e",
          "subnet-096fd3a9b88f1017f"
        ]
      }
    },
    "serviceConnectConfiguration": {
      "enabled": true,
      "namespace": "cruddur",
      "services": [
        {
          "portName": "backend-flask",
          "discoveryName": "backend-flask",
          "clientAliases": [{"port": 4567}]
        }
      ]
    },
    "propagateTags": "SERVICE",
    "serviceName": "backend-flask",
    "taskDefinition": "backend-flask"
  }
 ``` 
### Create Services

```sh
aws ecs create-service --cli-input-json file://aws/json/service-backend-flask.json
```

```sh
aws ecs create-service --cli-input-json file://aws/json/service-frontend-react-js.json
```
![ecs service backend-flask](https://user-images.githubusercontent.com/125069098/229582539-9cc3f97b-ee86-4e4f-99bf-ca1772588d55.png)

![ecs execute command ](https://user-images.githubusercontent.com/125069098/229586470-651bbfc8-dfa4-4b47-ac49-890511ee24f3.png)

![backend-flask health-check](https://user-images.githubusercontent.com/125069098/229586980-1bb0d5a3-eeb2-4cec-b0a9-b53f29c85c33.png)

### Create a bash script to connect-to-service of ECS cluster
backend-flask/bin/ecs/connect-to-service

```bash
#! /usr/bin/bash
if [ -z "$1" ]; then
  echo "No TASK_ID argument supplied eg ./bin/ecs/connect-to-service b48a8ba003c54582bd40806040067118 backend-flask"
  exit 1
fi
TASK_ID=$1

if [ -z "$2" ]; then
  echo "No CONTAINER_NAME argument supplied eg ./bin/ecs/connect-to-service b48a8ba003c54582bd40806040067118 backend-flask"
  exit 1
fi
CONTAINER_NAME=$2

echo "TASK ID : $TASK_ID"
echo "Container Name: $CONTAINER_NAME"

aws ecs execute-command  \
--region $AWS_DEFAULT_REGION \
--cluster cruddur \
--task $TASK_ID \
--container $CONTAINER_NAME \
--command "/bin/bash" \
--interactive
```

![image](https://user-images.githubusercontent.com/125069098/229591783-347e7d6c-41b0-430c-988e-f6486d50324d.png)

Update the security group for the backend-flask for port 4567

![image](https://user-images.githubusercontent.com/125069098/229593342-1a8c77c4-6bc9-49cc-8996-8e0d8de342d0.png)

![image](https://user-images.githubusercontent.com/125069098/229594144-8d608db2-5344-4e44-a5ce-5bb46f399db3.png)
![test connection](https://user-images.githubusercontent.com/125069098/229594600-50b5bb59-5a94-441f-a75d-5290bd852fdf.png)

![backend-flask](https://user-images.githubusercontent.com/125069098/229596647-ccbf909e-4acc-4584-9ffc-1169ef39b5f0.png)

Create a backend-flask service in ECS service with service connection using aws console
![aws console with service connection](https://user-images.githubusercontent.com/125069098/229603568-f7222f7a-f718-48ec-b529-4ca7706dad21.png)
![image](https://user-images.githubusercontent.com/125069098/229603751-6b3b9d9d-b0b7-4cb8-a5b9-63736cf52530.png)
![image](https://user-images.githubusercontent.com/125069098/229605370-62657e0d-1175-415b-ad9b-ec6c95666c2d.png)

Create a backend-flask service in ECS service with service connection using aws cli
update the json file with serviceConnectConfiguration
```json
 "serviceConnectConfiguration": {
      "enabled": true,
      "namespace": "cruddur",
      "services": [
        {
          "portName": "backend-flask",
          "discoveryName": "backend-flask",
          "clientAliases": [{"port": 4567}]
        }
      ]
    },
 ```   
![serviceConnectConfiguration](https://user-images.githubusercontent.com/125069098/229606907-bc34afb3-4056-446e-bb9f-af5e63fc8731.png)
![image](https://user-images.githubusercontent.com/125069098/229607642-1f447711-7865-470c-b015-51cb9f6bdae3.png)
![backend-flask](https://user-images.githubusercontent.com/125069098/229608003-91a1a8b1-06cf-42d1-8cc5-c8c93242eaf1.png)

**Create a LOAD BALANCER on the AWS console**

 Create Application Load Balancer
 ![image](https://user-images.githubusercontent.com/125069098/229609142-62fca93c-e8b6-44ac-ac04-ded17bbb420a.png)
![image](https://user-images.githubusercontent.com/125069098/229609241-a8ee1388-b02b-4e23-8063-bd2ae5e676d1.png)

create a new security group
![image](https://user-images.githubusercontent.com/125069098/229609925-8620c437-b5c9-4d45-a79b-e498ea434ba2.png)

create a target group for ALB one for backend-flask and one for frontend-react-js
![image](https://user-images.githubusercontent.com/125069098/229611444-60d073ef-7759-4217-a433-1340f6b9ebfa.png)
![image](https://user-images.githubusercontent.com/125069098/229611711-12e62e90-7cbb-4a2e-9aa9-d0a20897d0b2.png)
![image](https://user-images.githubusercontent.com/125069098/229611948-8a55e744-844f-4ee3-8e77-7bcf9f06e8cf.png)

frontend
![image](https://user-images.githubusercontent.com/125069098/229613040-d2c26925-b301-451b-954f-e780cfb9c1cb.png)
![image](https://user-images.githubusercontent.com/125069098/229613139-0d10b8d8-ff6f-4dbd-8d79-b2d7a5ba3c9c.png)


![image](https://user-images.githubusercontent.com/125069098/229612249-a9614c0e-7ef0-47d4-8a91-143a7cf1b627.png)
![image](https://user-images.githubusercontent.com/125069098/229613444-b9e2cf1c-8698-4815-bb6d-e2e9b44d69c9.png)

![image](https://user-images.githubusercontent.com/125069098/229613784-b9223eb9-d06f-494b-87b5-57ea103c99a8.png)

### To create the skeleton for the aws ecs create service
use the command
```aws
aws ecs create-service --generate-cli-skeleton
```
Add the Load balancer to the service-backend-flask.json

```json
"loadBalancers": [
      {
          "targetGroupArn": "arn:aws:elasticloadbalancing:us-east-1:480134889878:targetgroup/cruddur-backend-flask-tg/b9b86436516addaa",
          "containerName": "backend-flask",
          "containerPort": 4567
      }
    ],
```
Run the create service command
```aws
aws ecs create-service --cli-input-json file://aws/json/service-backend-flask.json
```
![image](https://user-images.githubusercontent.com/125069098/229619061-d1883440-00bb-44b1-ba2d-c22b562cb736.png)

![image](https://user-images.githubusercontent.com/125069098/229621188-be325cb0-ecad-4953-baa0-ff219bd391f1.png)

![ALB health-check](https://user-images.githubusercontent.com/125069098/229621523-3c76d5e4-169f-4edc-8210-b55d771162a2.png)

### Build the frontend-react-js
Create a dockerfile.prod
```docker
# Base Image ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
FROM node:16.18 AS build

ARG REACT_APP_BACKEND_URL
ARG REACT_APP_AWS_PROJECT_REGION
ARG REACT_APP_AWS_COGNITO_REGION
ARG REACT_APP_AWS_USER_POOLS_ID
ARG REACT_APP_CLIENT_ID

ENV REACT_APP_BACKEND_URL=$REACT_APP_BACKEND_URL
ENV REACT_APP_AWS_PROJECT_REGION=$REACT_APP_AWS_PROJECT_REGION
ENV REACT_APP_AWS_COGNITO_REGION=$REACT_APP_AWS_COGNITO_REGION
ENV REACT_APP_AWS_USER_POOLS_ID=$REACT_APP_AWS_USER_POOLS_ID
ENV REACT_APP_CLIENT_ID=$REACT_APP_CLIENT_ID

COPY . ./frontend-react-js
WORKDIR /frontend-react-js
RUN npm install
RUN npm run build

# New Base Image ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
FROM nginx:1.23.3-alpine

# --from build is coming from the Base Image
COPY --from=build /frontend-react-js/build /usr/share/nginx/html
COPY --from=build /frontend-react-js/nginx.conf /etc/nginx/nginx.conf

EXPOSE 3000
```
create a task-definitions/frontend-react-js.json
```json
{
    "family": "frontend-react-js",
    "executionRoleArn": "arn:aws:iam::480134889878:role/CruddurServiceExecutionRole",
    "taskRoleArn": "arn:aws:iam::480134889878:role/CruddurTaskRole",
    "networkMode": "awsvpc",
    "cpu": "256",
    "memory": "512",
    "requiresCompatibilities": [ 
      "FARGATE" 
    ],
    "containerDefinitions": [
      {
        "name": "frontend-react-js",
        "image": "480134889878.dkr.ecr.us-east-1.amazonaws.com/frontend-react-js",
        "essential": true,
        "portMappings": [
          {
            "name": "frontend-react-js",
            "containerPort": 3000,
            "protocol": "tcp", 
            "appProtocol": "http"
          }
        ],

        "logConfiguration": {
          "logDriver": "awslogs",
          "options": {
              "awslogs-group": "cruddur",
              "awslogs-region": "us-east-1",
              "awslogs-stream-prefix": "frontend-react-js"
          }
        }
      }
    ]
  }
```
Once the dockerfile.prod is created with multi-stage 
change in frontend-react-js/ do npm run build
once it is successful.
![image](https://user-images.githubusercontent.com/125069098/229628425-1c4d86e3-026f-4870-a8dc-d41cad271e5b.png)
![image](https://user-images.githubusercontent.com/125069098/229628492-d8f101d8-2013-4a3c-a507-d3e4db29558e.png)

### For Frontend React

#### Create Repo
```sh
aws ecr create-repository \
  --repository-name frontend-react-js \
  --image-tag-mutability MUTABLE
```
![image](https://user-images.githubusercontent.com/125069098/229630442-97edc22d-1736-494d-8db5-4addda43bef7.png)
![image](https://user-images.githubusercontent.com/125069098/229630485-5d528b8a-e1db-401e-962a-8671bec9f7f6.png)

#### Set URL

```sh
export ECR_FRONTEND_REACT_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/frontend-react-js"
echo $ECR_FRONTEND_REACT_URL
```

#### Build Image
Before you run the docker build change the USER_POOLS_ID and APP_CLIENT_ID with the values in the docker compose file.

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
![image](https://user-images.githubusercontent.com/125069098/229630659-9f9be4c0-bfc4-41b2-9986-2951d23be686.png)


#### Tag Image

```sh
docker tag frontend-react-js:latest $ECR_FRONTEND_REACT_URL:latest
```
![image](https://user-images.githubusercontent.com/125069098/229633677-48bbfc5e-3551-426c-a36f-fbcc6f7a77fb.png)

#### Push Image

```sh
docker push $ECR_FRONTEND_REACT_URL:latest
```
To push into the **ECR** first login the ecr repo then push
![image](https://user-images.githubusercontent.com/125069098/229635702-35f1c051-af44-46a5-917d-0985b6349dbe.png)
![image](https://user-images.githubusercontent.com/125069098/229635753-5dac892a-ec8f-4eb0-b7fc-25e40e25a5f0.png)


If you want to run and test it

```sh
docker run --rm -p 3000:3000 -it frontend-react-js 
```
### Register Task Defintion

```aws
aws ecs register-task-definition --cli-input-json file://aws/task-definitions/frontend-react-js.json
```
go up a directory before you copy and paste the above command.
![image](https://user-images.githubusercontent.com/125069098/229636429-7ec2837d-ef89-49e0-9ac6-f0a1145c0b55.png)

### Create Services
```aws
aws ecs create-service --cli-input-json file://aws/json/service-frontend-react-js.json
```
![create-service](https://user-images.githubusercontent.com/125069098/229638842-f1bb2bbe-ab3e-4e3c-992b-ffc181fb948f.png)

**Change the task definition to add the health-check for the frontend-react-js**
```json
{
    "family": "frontend-react-js",
    "executionRoleArn": "arn:aws:iam::480134889878:role/CruddurServiceExecutionRole",
    "taskRoleArn": "arn:aws:iam::480134889878:role/CruddurTaskRole",
    "networkMode": "awsvpc",
    "cpu": "256",
    "memory": "512",
    "requiresCompatibilities": [ 
      "FARGATE" 
    ],
    "containerDefinitions": [
      {
        "name": "frontend-react-js",
        "image": "480134889878.dkr.ecr.us-east-1.amazonaws.com/frontend-react-js",
        "essential": true,
        "healthCheck": {
          "command": [
            "CMD-SHELL",
            "curl -f http://localhost:3000 || exit 1"
          ],
          "interval": 30,
          "timeout": 5,
          "retries": 3
        },
        "portMappings": [
          {
            "name": "frontend-react-js",
            "containerPort": 3000,
            "protocol": "tcp", 
            "appProtocol": "http"
          }
        ],

        "logConfiguration": {
          "logDriver": "awslogs",
          "options": {
              "awslogs-group": "cruddur",
              "awslogs-region": "us-east-1",
              "awslogs-stream-prefix": "frontend-react-js"
          }
        }
      }
    ]
  }
```
Rerun the task definition again
```aws
aws ecs register-task-definition --cli-input-json file://aws/task-definitions/frontend-react-js.json
```
**Edit the security group of sg-0a9faf8a5b6cebc28 - crud-srv-sg to include the frontend port**
![image](https://user-images.githubusercontent.com/125069098/229855524-a3a5c115-99d4-4528-a1d5-74794290b867.png)

**Create service**
```aws
aws ecs create-service --cli-input-json file://aws/json/service-frontend-react-js.json
```
![image](https://user-images.githubusercontent.com/125069098/229855020-7b07d65b-d3d2-4cce-8ddf-cf1f8404dcbf.png)
![image](https://user-images.githubusercontent.com/125069098/229855700-2ea9873b-b53b-48f8-941d-5868aa893147.png)
![targetgroup health check](https://user-images.githubusercontent.com/125069098/229857003-68aa504c-68d4-4952-a2cb-4f607f7d817c.png)

Where view the frontend app on the browser it is not loading the data

change the  docker build command with the ALB for the REACT_APP_BACKEND_URL:4567
```docker
docker build \
--build-arg REACT_APP_BACKEND_URL="https://cruddur-alb-683537449.us-east-1.elb.amazonaws.com:4567" \
--build-arg REACT_APP_AWS_PROJECT_REGION="$AWS_DEFAULT_REGION" \
--build-arg REACT_APP_AWS_COGNITO_REGION="$AWS_DEFAULT_REGION" \
--build-arg REACT_APP_AWS_USER_POOLS_ID="<us-east-1_xxxxxxxxR>" \
--build-arg REACT_APP_CLIENT_ID="<324xxxxxxxxxxpuii>" \
-t frontend-react-js \
-f Dockerfile.prod \
.
```
then create the ECS service 
```aws
aws ecs create-service --cli-input-json file://aws/json/service-frontend-react-js.json
```
**Make sure your RDS should be up and running(PROD-CONNECTION_URL)**

### Create a Hosted domain name for your domainname

![hosted domainname](https://user-images.githubusercontent.com/125069098/230158556-0672bf15-c6d5-4057-a685-01e396c2652e.png)
Update the nameserver in the website of the domainname you purchased. I have used godaddy.com 

![godaddy](https://user-images.githubusercontent.com/125069098/230158903-1f2260f7-d0b9-4944-a4ac-77e5abe24c11.png)


### Create a certficate manager to request for SSL certificate

![certificate Manager](https://user-images.githubusercontent.com/125069098/230159375-d62c49d3-447e-4660-a39a-09383282122c.png)

click on the create a record in Route53

![image](https://user-images.githubusercontent.com/125069098/230160954-077f1682-1ca4-4beb-9f57-6e162f994bc4.png)

![Record for ceritificate in route53](https://user-images.githubusercontent.com/125069098/230161280-02f9099a-b282-427f-ad6b-311b6b55a7a7.png)
![image](https://user-images.githubusercontent.com/125069098/230161953-27f190b9-377b-4436-b146-690688a35e2c.png)
**EDIT the ALB to manage the rules**

![ALB](https://user-images.githubusercontent.com/125069098/230162992-d863ab5e-1d0a-4cf5-a366-79f6ed052acb.png)
**add a listener for redirecting to 443**
![image](https://user-images.githubusercontent.com/125069098/230164275-cc7b1ece-8c82-4d9a-aa75-ab96bae74c20.png)

![image](https://user-images.githubusercontent.com/125069098/230167709-83e8c8e3-8b2d-4148-9a55-b2403f1f1205.png)

**Add a listener for 443 to forward to frontend-react-js app with certificate add**

![image](https://user-images.githubusercontent.com/125069098/230169287-be4e4eaa-adf2-4250-a812-8c19fe50b855.png)
![image](https://user-images.githubusercontent.com/125069098/230169408-45c47016-3953-42d6-829d-af98e9f5634b.png)
![image](https://user-images.githubusercontent.com/125069098/230169609-e8a37683-fc94-44ea-a36d-bcde5ee12b3c.png)
remove the other listeners for port 4567 and 3000
![image](https://user-images.githubusercontent.com/125069098/230179645-6e91d5d0-a555-4b48-ba41-b08d6f82d1bd.png)

**Add Manage rule for HTTPS:443:**
![image](https://user-images.githubusercontent.com/125069098/230180481-2407bb9b-d356-4093-8a43-d486692b7dc5.png)
![image](https://user-images.githubusercontent.com/125069098/230180692-ccf5dcc6-36c5-4275-a950-11a1806f58a9.png)

**Create a record in the Route53 for a ALB**

![image](https://user-images.githubusercontent.com/125069098/230181765-b88a8e18-5059-4ccf-a9a9-819e775703e7.png)
Create a record for api.domainname for the ALB
![image](https://user-images.githubusercontent.com/125069098/230182394-a7f84b1e-2ec2-4720-b1cf-419a0a7a6761.png)

**curl the dns and see whether it is working or not**

![image](https://user-images.githubusercontent.com/125069098/230183350-8598223e-13ae-4a61-a5ad-94494571723d.png)

**Test in the edge browser**

![image](https://user-images.githubusercontent.com/125069098/230183829-6e1c2d08-9884-4afc-b562-892f1da02920.png)

**Edit the task definition for backend-flask with dns names
```json
"environment": [
          {"name": "OTEL_SERVICE_NAME", "value": "backend-flask"},
          {"name": "OTEL_EXPORTER_OTLP_ENDPOINT", "value": "https://api.honeycomb.io"},
          {"name": "AWS_COGNITO_USER_POOL_ID", "value": "us-east-1_eMMMwKxYR"},
          {"name": "AWS_COGNITO_USER_POOL_CLIENT_ID", "value": "324mfino7qkho2jbqis665puii"},
          {"name": "FRONTEND_URL", "value": "madhavi27.xyz"},
          {"name": "BACKEND_URL", "value": "api.madhavi27.xyz"},
          {"name": "AWS_DEFAULT_REGION", "value": "us-east-1"}
        ],
```
![image](https://user-images.githubusercontent.com/125069098/230188083-9deafb3b-ca4b-42ff-b71a-1cb71d72a14f.png)

### Login to ECR to push the new frontend image
```aws
aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com"
```
### Set URL
```sh
export ECR_FRONTEND_REACT_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/frontend-react-js"
echo $ECR_FRONTEND_REACT_URL
```
![image](https://user-images.githubusercontent.com/125069098/230191364-2cded522-64de-4f9c-847e-365d98fc4e09.png)

### Build the Image for frontend
```docker
docker build \
--build-arg REACT_APP_BACKEND_URL="https://api.madhavi27.xyz" \
--build-arg REACT_APP_AWS_PROJECT_REGION="$AWS_DEFAULT_REGION" \
--build-arg REACT_APP_AWS_COGNITO_REGION="$AWS_DEFAULT_REGION" \
--build-arg REACT_APP_AWS_USER_POOLS_ID="us-east-1_eMMMwKxYR" \
--build-arg REACT_APP_CLIENT_ID="324mfino7qkho2jbqis665puii" \
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
Do the force deploy services

Test it on the edge browser with https://api.madhavi27.xyz/api/health-check

![image](https://user-images.githubusercontent.com/125069098/230199238-6586e0ec-b5ff-4390-903d-b513ca5080a0.png)

Test the https://madhavi27.xyz

![image](https://user-images.githubusercontent.com/125069098/230199799-783fbcce-114b-4c18-aab5-ce52fcca0faa.png)

Update the environment variable in task-definition in backend-flask.json
```json
"environment": [
          {"name": "OTEL_SERVICE_NAME", "value": "backend-flask"},
          {"name": "OTEL_EXPORTER_OTLP_ENDPOINT", "value": "https://api.honeycomb.io"},
          {"name": "AWS_COGNITO_USER_POOL_ID", "value": "us-east-1_eMMMwKxYR"},
          {"name": "AWS_COGNITO_USER_POOL_CLIENT_ID", "value": "324mfino7qkho2jbqis665puii"},
          {"name": "FRONTEND_URL", "value": "https://madhavi27.xyz"},
          {"name": "BACKEND_URL", "value": "https://api.madhavi27.xyz"},
          {"name": "AWS_DEFAULT_REGION", "value": "us-east-1"}
        ],
```
Do force deploy the ecs service for the backend-flask

Test the cruddur app again in the browser https://madhavi27.xyz

![image](https://user-images.githubusercontent.com/125069098/230208423-62a9eb4f-d3f0-40e6-bbf6-b64ca92a5933.png)

# Securing Flask
Remove the inbound rules for the sg-0c7290dbbfb33ed8d - cruddur-alb-sg for ports 3000 and 4567

change the ports 443 and 80 to access only my ip

![image](https://user-images.githubusercontent.com/125069098/230420171-65d0b96d-ef64-4ef1-9b33-b43080e01a04.png)

### Create script file for the ECR Login
'backend-flask/bin/ecr/login'
```sh
#! /usr/bin/bash

aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com"
```
![image](https://user-images.githubusercontent.com/125069098/230427963-2a898174-eb8b-4954-bce3-51a910483b00.png)

### Build docker build for the backend with Dockerfile.prod
```sh
docker build -f Dockerfile.prod -t backend-flask-prod .
```
![image](https://user-images.githubusercontent.com/125069098/230428755-79910eb4-3a40-4a49-9f28-c8a4c921f22c.png)

 ```sh
docker run --rm \
-p 4567:4567 \
-e AWS_ENDPOINT_URL="http://dynamodb-local:8000" \
-e CONNECTION_URL="postgresql://postgres:password@db:5432/cruddur" \
-e FRONTEND_URL="https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}" \
-e BACKEND_URL="https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}" \
-e OTEL_SERVICE_NAME='backend-flask' \
-e OTEL_EXPORTER_OTLP_ENDPOINT="https://api.honeycomb.io" \
-e OTEL_EXPORTER_OTLP_HEADERS="x-honeycomb-team=${HONEYCOMB_API_KEY}" \
-e AWS_XRAY_URL="*4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}*" \
-e AWS_XRAY_DAEMON_ADDRESS="xray-daemon:2000" \
-e AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" \
-e AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
-e AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
-e ROLLBAR_ACCESS_TOKEN="${ROLLBAR_ACCESS_TOKEN}" \
-e AWS_COGNITO_USER_POOL_ID="${AWS_COGNITO_USER_POOL_ID}" \
-e AWS_COGNITO_USER_POOL_CLIENT_ID="324mfino7qkho2jbqis665puii" \   
-it backend-flask-prod
 ```
# Implement Refresh Token Cognito

First Login into the ecr by running ./bin/ecr/login
![image](https://user-images.githubusercontent.com/125069098/230454311-63092731-b506-40c7-b1f3-39163973781f.png)

Do the docker compose up
![image](https://user-images.githubusercontent.com/125069098/230454446-b2a725b4-61a6-4e3c-9710-cbfc839c705b.png)

setup postgres by running ./bin/db/setup file
![image](https://user-images.githubusercontent.com/125069098/230454714-678c87f1-8f45-41bb-9a83-661e814cd92d.png)

Run dynamodb schema-load ./bin/ddb/schema-load
![image](https://user-images.githubusercontent.com/125069098/230454876-797e129e-5f6b-4ab5-a2e1-d6d925a60697.png)

Run the dynamodb seed file ./bin/ddb/seed
![image](https://user-images.githubusercontent.com/125069098/230455818-f5f21808-6a6f-43eb-8a85-2b01f1deddd4.png)

Test the app is working fine
![image](https://user-images.githubusercontent.com/125069098/230455637-7c0a68dc-aaf1-49c1-9d45-bd4aad09f51d.png)

modify the code in the CheckAuth.js in frontend-react-js 
```js
export async function getAccessToken () {
  Auth.currentSession() 
  .then((cognito_user_session) => {
    const access_token = cognito_user_session.accessToken.jwtToken
    localStorage.setItem("access_token", access_token)
  })
  .catch((err) => console.log(err)); 
}
export async function checkAuth (setUser) {
.then((cognito_user) => {
    console.log('cognito_user',cognito_user);
    setUser({
      display_name: cognito_user.attributes.name,
      handle: cognito_user.attributes.preferred_username
    })
    return Auth.currentSession()
  }).then((cognito_user_session) => {
    console.log('cognito_user_session',cognito_user_session);
    localStorage.setItem("access_token", cognito_user_session.accessToken.jwtToken)  
  })
```  
Modify the code in other files where the CheckAuth.js library is imported.
Messagefeed.js,Homefeedpage.js,messagegroupsPage.js, messagegrouppage.js, messagegroupsNewPage.js

Then test the frontend App is able to refresh the token properly.




























