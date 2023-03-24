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
![image](https://user-images.githubusercontent.com/125069098/227278586-16e14d71-4f4b-4693-84a3-115eaf1f0074.png)
![image](https://user-images.githubusercontent.com/125069098/227280043-1e4edacc-47ba-46b7-8c0b-a406872f11e0.png)
![image](https://user-images.githubusercontent.com/125069098/227282749-3d2d6b26-1dbd-48e7-a070-8d84536b212a.png)


![image](https://user-images.githubusercontent.com/125069098/227404075-0150eb5b-5694-46ba-b29d-d9ef944b714d.png)
![image](https://user-images.githubusercontent.com/125069098/227404586-4b6a687c-c8fb-4044-85fe-e99f2ca0cde7.png)

![update cognito_user_id](https://user-images.githubusercontent.com/125069098/227583290-28a5f3a9-63fa-404f-92fd-0571e90e3323.png)





