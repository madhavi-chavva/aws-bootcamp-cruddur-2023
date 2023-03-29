# Week 5 — DynamoDB and Serverless Caching

## Creaate Dynamodb table using the python script to load the schema

```py
#!/usr/bin/env python3

import boto3
import sys

attrs = {
  'endpoint_url': 'http://localhost:8000'
}

if len(sys.argv) == 2:
  if "prod" in sys.argv[1]:
    attrs = {}

ddb = boto3.client('dynamodb',**attrs)

table_name = 'cruddur-messages'


response = ddb.create_table(
  TableName=table_name,
  AttributeDefinitions=[
    {
      'AttributeName': 'pk',
      'AttributeType': 'S'
    },
    {
      'AttributeName': 'sk',
      'AttributeType': 'S'
    },
  ],
  KeySchema=[
    {
      'AttributeName': 'pk',
      'KeyType': 'HASH'
    },
    {
      'AttributeName': 'sk',
      'KeyType': 'RANGE'
    },
  ],
  #GlobalSecondaryIndexes=[
  #],
  BillingMode='PROVISIONED',
  ProvisionedThroughput={
      'ReadCapacityUnits': 5,
      'WriteCapacityUnits': 5
  }
)

print(response)
```
![ddb schema load](https://user-images.githubusercontent.com/125069098/226788990-aa662b14-c36f-4b22-9b7f-b2421bf8d2de.png)

## Bash script to list the dynamobd tables

```bash
#! /usr/bin/bash
set -e # stop if it fails at any point

if [ "$1" = "prod" ]; then
  ENDPOINT_URL=""
else
  ENDPOINT_URL="--endpoint-url=http://localhost:8000"
fi

aws dynamodb list-tables $ENDPOINT_URL \
--query TableNames \
--output table
```
![list table](https://user-images.githubusercontent.com/125069098/226789534-92882c79-47fe-4c25-8735-cc465e597110.png)


## Bash script to delete the dynamodb tables

```bash
#! /usr/bin/bash

set -e # stop if it fails at any point

if [ -z "$1" ]; then
  echo "No TABLE_NAME argument supplied eg ./bin/ddb/drop cruddur-messages prod "
  exit 1
fi
TABLE_NAME=$1

if [ "$2" = "prod" ]; then
  ENDPOINT_URL=""
else
  ENDPOINT_URL="--endpoint-url=http://localhost:8000"
fi

echo "deleting table: $TABLE_NAME"

aws dynamodb delete-table $ENDPOINT_URL \
  --table-name $TABLE_NAME
```
![delete dynamodb table](https://user-images.githubusercontent.com/125069098/226790002-6b117a7a-f43e-486a-9d3b-613159694bb9.png)
![image](https://user-images.githubusercontent.com/125069098/226790108-a9a145b6-22c2-496d-aca4-226208cd157b.png)

![rds seed](https://user-images.githubusercontent.com/125069098/226791223-3c0cf085-a31f-43a9-b3e0-e7d7e4ed1c1b.png)



## python script to seed data into tables


![image](https://user-images.githubusercontent.com/125069098/226792555-835d42e8-fe4c-400c-ad66-41805f2d98d2.png)
![image](https://user-images.githubusercontent.com/125069098/226792804-93fcf8e8-7280-4627-bda4-5adf71a6f21e.png)

## python script to scan data from tables
```py
#!/usr/bin/env python3

import boto3

attrs = {
  'endpoint_url': 'http://localhost:8000'
}
ddb = boto3.resource('dynamodb',**attrs)
table_name = 'cruddur-messages'

table = ddb.Table(table_name)
response = table.scan()

items = response['Items']
for item in items:
  print(item)
```  

![scan](https://user-images.githubusercontent.com/125069098/226793155-13e2cabc-9a15-4b29-9812-8db78742a9c5.png)

## python script to get-conversation data from tables
```py
#!/usr/bin/env python3

import boto3
import sys
import json
import datetime

attrs = {
  'endpoint_url': 'http://localhost:8000'
}

if len(sys.argv) == 2:
  if "prod" in sys.argv[1]:
    attrs = {}

dynamodb = boto3.client('dynamodb',**attrs)
table_name = 'cruddur-messages'

message_group_uuid = "5ae290ed-55d1-47a0-bc6d-fe2bc2700399"

# define the query parameters
current_year = datetime.datetime.now().year
query_params = {
  'TableName': table_name,
  'ScanIndexForward': False,
  'Limit': 20,
  'ReturnConsumedCapacity': 'TOTAL',
  'KeyConditionExpression': 'pk = :pk AND begins_with(sk,:year)',
  #'KeyConditionExpression': 'pk = :pk AND sk BETWEEN :start_date AND :end_date',
  'ExpressionAttributeValues': {
    ':year': {'S': '2023'},
    #":start_date": { "S": "2023-03-01T00:00:00.000000+00:00" },
    #":end_date": { "S": "2023-03-19T23:59:59.999999+00:00" },
    ':pk': {'S': f"MSG#{message_group_uuid}"}
  }
}


# query the table
response = dynamodb.query(**query_params)

# print the items returned by the query
print(json.dumps(response, sort_keys=True, indent=2))

# print the consumed capacity
print(json.dumps(response['ConsumedCapacity'], sort_keys=True, indent=2))

items = response['Items']
reversed_array = items[::-1]
#items.reverse()

for item in reversed_array:
  sender_handle = item['user_handle']['S']
  message       = item['message']['S']
  timestamp     = item['sk']['S']
  dt_object = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
  formatted_datetime = dt_object.strftime('%Y-%m-%d %I:%M %p')
  print(f'{sender_handle: <12}{formatted_datetime: <22}{message[:40]}...')
```  
![get conversation](https://user-images.githubusercontent.com/125069098/226793681-b20afd92-eeda-495a-983d-d6004609176c.png)
![get conversation1](https://user-images.githubusercontent.com/125069098/226793820-065babb1-3526-4880-bfc8-d73697b79b2d.png)

##  python script to list-conversation data from tables
```py
#!/usr/bin/env python3

import boto3
import sys
import json
import os
import datetime

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, '..', '..', '..'))
sys.path.append(parent_path)
from lib.db import db

attrs = {
  'endpoint_url': 'http://localhost:8000'
}

if len(sys.argv) == 2:
  if "prod" in sys.argv[1]:
    attrs = {}

dynamodb = boto3.client('dynamodb',**attrs)
table_name = 'cruddur-messages'

def get_my_user_uuid():
  sql = """
    SELECT 
      users.uuid
    FROM users
    WHERE
      users.handle =%(handle)s
  """
  uuid = db.query_value(sql,{
    'handle':  'andrewbrown'
  })
  return uuid

my_user_uuid = get_my_user_uuid()
print(f"my-uuid: {my_user_uuid}")

current_year = datetime.datetime.now().year
# define the query parameters
query_params = {
  'TableName': table_name,
      'KeyConditionExpression': 'pk = :pk AND begins_with(sk,:year)',
  'ScanIndexForward': False,
  'ExpressionAttributeValues': {
    ':year': {'S': str(current_year) },
    ':pk': {'S': f"GRP#{my_user_uuid}"}
  },
  'ReturnConsumedCapacity': 'TOTAL'
}

# query the table
response = dynamodb.query(**query_params)

# print the items returned by the query
print(json.dumps(response, sort_keys=True, indent=2))
```

![list conversation](https://user-images.githubusercontent.com/125069098/226796490-85bb6ce8-3df7-4b86-a53f-9212bd30e9bf.png)
![image](https://user-images.githubusercontent.com/125069098/226796564-c0ed5bf7-a043-4ad7-b4c2-12786b807878.png)

##  Implement Conversations with DynamoDB

- Update your /backend-flask/db/seed.sql with records and change the users.handle = **your handler**.
- Run the script file ./bin/db/setup It has to run without errors.
- Run the script file  ./bin/db/update_cognito_user_ids. It has to update the cognito-user-id in the user table
- Connect to your postgres and check the rows are updated with your cognito-user-id.
- Run the script file ./bin/ddb/schema-load. It will create a dynamoDB table Cruddur-message
- Run the script file ./bin/ddb/seed before you run change the my_handle =**your handler** and other_handle =**other handler** 
- Run the script file ./bin/ddb/scan 
- Run the script file  ./bin/ddb/patterns/get-conversation. It has to run without error and has to get the conversation in the my-user and other-user in the reverse order
- Run the script file  ./bin/ddb/patterns/list-conversation. It has to run without error and has to give you the scannedcount=1

  once the above steps are successful. implement the conversation code for dynamoDB.
 
![image](https://user-images.githubusercontent.com/125069098/227278586-16e14d71-4f4b-4693-84a3-115eaf1f0074.png)
![image](https://user-images.githubusercontent.com/125069098/227280043-1e4edacc-47ba-46b7-8c0b-a406872f11e0.png)


===
![db_setup](https://user-images.githubusercontent.com/125069098/228560214-1f87ff05-5811-4dc7-a47a-08621fc1ddf2.png)
![ddb_schema-load](https://user-images.githubusercontent.com/125069098/228560751-c5169a31-9433-48c1-8e2e-4fc28e19f3dd.png)
![ddb_seed](https://user-images.githubusercontent.com/125069098/228561249-d5dac021-8225-4b8c-9924-0846a6429dbb.png)
![ddb_scan](https://user-images.githubusercontent.com/125069098/228562192-a6597bbd-d3f0-4920-bfe7-1d9161454ccf.png)
![ddb_pattern_get-conversations](https://user-images.githubusercontent.com/125069098/228562601-d4836a03-86e7-4e00-bed7-242de1a96c1e.png)
![ddb_pattern_get-conversations1](https://user-images.githubusercontent.com/125069098/228562853-aefc7a21-6df5-44d1-a385-7beb26cceb3f.png)
![ddb_pattern_list-conversations](https://user-images.githubusercontent.com/125069098/228563849-5b113c7d-76b5-4e48-9389-eb480c8561a8.png)
![ddb_pattern_list-conversations1](https://user-images.githubusercontent.com/125069098/228564102-d22979db-bb55-4fb2-80a2-b8bff53b4fec.png)
![update bayko with cognito_user_id](https://user-images.githubusercontent.com/125069098/228564816-4a35d6ec-f790-41ae-8eb5-15ec1159f2f9.png)
![users table](https://user-images.githubusercontent.com/125069098/228565153-405c492e-eefb-4ab3-98e5-84fd65bb5aa4.png)

![message_5ae290ed-55d1-47a0-bc6d-fe2bc2700399](https://user-images.githubusercontent.com/125069098/228566214-47492b15-c74a-4f06-a975-3ac5d630f094.png)
![Post message](https://user-images.githubusercontent.com/125069098/228593886-a5c75545-342f-41d0-9d6b-b73798c6cbbd.png)
![posted message](https://user-images.githubusercontent.com/125069098/228594067-1ecc8050-61fd-4ba6-b0a3-56575da10e3b.png)

![image](https://user-images.githubusercontent.com/125069098/228593606-8eec499b-0e9a-49c4-a05e-ce52eec855c0.png)
![new_handler_londo](https://user-images.githubusercontent.com/125069098/228570145-e64602e6-77e1-4750-b168-a0ab0a938dfe.png)


### DynamoDB Stream trigger to update message groups

- create a VPC endpoint for dynamoDB service on your VPC
- create a Python lambda function in your vpc
- enable streams on the table with 'new image' attributes included
- add your function as a trigger on the stream
- grant the lambda IAM role permission to read the DynamoDB stream events

`AWSLambdaInvocation-DynamoDB`

- grant the lambda IAM role permission to update table items

### Create dynamodb using the python script
```py
#!/usr/bin/env python3

import boto3
import sys

attrs = {
  'endpoint_url': 'http://localhost:8000'
}

if len(sys.argv) == 2:
  if "prod" in sys.argv[1]:
    attrs = {}

ddb = boto3.client('dynamodb',**attrs)

table_name = 'cruddur-messages'


response = ddb.create_table(
  TableName=table_name,
  AttributeDefinitions=[
    {
      'AttributeName': 'message_group_uuid',
      'AttributeType': 'S'
    },
    {
      'AttributeName': 'pk',
      'AttributeType': 'S'
    },
    {
      'AttributeName': 'sk',
      'AttributeType': 'S'
    },
  ],
  KeySchema=[
    {
      'AttributeName': 'pk',
      'KeyType': 'HASH'
    },
    {
      'AttributeName': 'sk',
      'KeyType': 'RANGE'
    },
  ],
  GlobalSecondaryIndexes= [{
    'IndexName':'message-group-sk-index',
    'KeySchema':[{
      'AttributeName': 'message_group_uuid',
      'KeyType': 'HASH'
    },{
      'AttributeName': 'sk',
      'KeyType': 'RANGE'
    }],
    'Projection': {
      'ProjectionType': 'ALL'
    },
    'ProvisionedThroughput': {
      'ReadCapacityUnits': 5,
      'WriteCapacityUnits': 5
    },
  }],
  BillingMode='PROVISIONED',
  ProvisionedThroughput={
      'ReadCapacityUnits': 5,
      'WriteCapacityUnits': 5
  }
)

print(response)
```

![ddb schema-load](https://user-images.githubusercontent.com/125069098/228620087-12bcea0a-d224-4ee6-a167-5bbdaf6a58a5.png)

![Turn on Newimage](https://user-images.githubusercontent.com/125069098/228620933-7753bd22-963e-46fd-b15e-43ca8fc79a85.png)
![image](https://user-images.githubusercontent.com/125069098/228621146-29889ae1-d6de-46c0-862d-70c7711ab460.png)

### create a VPC ENDPOINT in aws

![image](https://user-images.githubusercontent.com/125069098/228622937-3f9578b3-508c-496e-aa53-1ed6cae30d62.png)
![image](https://user-images.githubusercontent.com/125069098/228623082-caf4d3e9-7f08-4f35-8f5b-1a96f37af635.png)
![image](https://user-images.githubusercontent.com/125069098/228623204-50fd3c02-4425-4ee7-916d-42b5aa2f266f.png)
![image](https://user-images.githubusercontent.com/125069098/228623269-da4b6ff7-5473-435c-ab41-7adea6527c77.png)

**Create a Lambda funnction**

![lambda function](https://user-images.githubusercontent.com/125069098/228625727-5072d635-bdc0-4c62-8b8e-bae7d4c70adc.png)
![lambda function](https://user-images.githubusercontent.com/125069098/228626314-7ebbd4a2-c735-4af9-8c62-71969529b36e.png)
![image](https://user-images.githubusercontent.com/125069098/228626806-1daa7282-1a89-4ee4-b866-275f9f525b24.png)

**create a trigger in dynamodb**
![image](https://user-images.githubusercontent.com/125069098/228629233-47ff4575-d02e-4318-9252-a539218d045e.png)

**The Function**

```.py
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource(
 'dynamodb',
 region_name='us-east-1',
 endpoint_url="http://dynamodb.us-east-1.amazonaws.com"
)

def lambda_handler(event, context):
  print('event-data',event)

  eventName = event['Records'][0]['eventName']
  if (eventName == 'REMOVE'):
    print("skip REMOVE event")
    return
  pk = event['Records'][0]['dynamodb']['Keys']['pk']['S']
  sk = event['Records'][0]['dynamodb']['Keys']['sk']['S']
  if pk.startswith('MSG#'):
    group_uuid = pk.replace("MSG#","")
    message = event['Records'][0]['dynamodb']['NewImage']['message']['S']
    print("GRUP ===>",group_uuid,message)

    table_name = 'cruddur-messages'
    index_name = 'message-group-sk-index'
    table = dynamodb.Table(table_name)
    data = table.query(
      IndexName=index_name,
      KeyConditionExpression=Key('message_group_uuid').eq(group_uuid)
    )
    print("RESP ===>",data['Items'])

    # recreate the message group rows with new SK value
    for i in data['Items']:
      delete_item = table.delete_item(Key={'pk': i['pk'], 'sk': i['sk']})
      print("DELETE ===>",delete_item)

      response = table.put_item(
        Item={
          'pk': i['pk'],
          'sk': sk,
          'message_group_uuid':i['message_group_uuid'],
          'message':message,
          'user_display_name': i['user_display_name'],
          'user_handle': i['user_handle'],
          'user_uuid': i['user_uuid']
        }
      )
      print("CREATE ===>",response)
```

 Do the docker compose up and open the frontend app
 ![image](https://user-images.githubusercontent.com/125069098/228629925-ec24dfa3-8c75-4b47-b1d0-be2a42333026.png)
![image](https://user-images.githubusercontent.com/125069098/228630548-33507155-2c4d-4039-b06a-cbcc0b54e7f5.png)

**Create inline policy for the Lambda function**
![image](https://user-images.githubusercontent.com/125069098/228635683-3891b61a-617c-492c-8c2c-71e1bf5615a1.png)
![image](https://user-images.githubusercontent.com/125069098/228635843-8de44059-0e30-4370-8c85-30481a56b74b.png)
![image](https://user-images.githubusercontent.com/125069098/228635955-446992ff-19af-4882-a725-287fdf1eae6c.png)

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem",
                "dynamodb:DeleteItem",
                "dynamodb:Query"
            ],
            "Resource": [
                "arn:aws:dynamodb:us-east-1:480134889878:table/cruddur-messages",
                "arn:aws:dynamodb:us-east-1:480134889878:table/cruddur-messages/index/message-group-sk-index"
            ]
        }
    ]
}
```
![image](https://user-images.githubusercontent.com/125069098/228636926-8564eb92-d080-4138-afad-65c5835d60f1.png)
![image](https://user-images.githubusercontent.com/125069098/228637954-b530c0ec-95e0-495d-933a-25eed535f4e4.png)





