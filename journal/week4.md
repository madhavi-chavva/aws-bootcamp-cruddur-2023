# Week 4 — Postgres and RDS

## Provision RDS Instance
Create a RDS instance using AWS CLI

```sh
aws rds create-db-instance \
  --db-instance-identifier cruddur-db-instance \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version  14.6 \
  --master-username root \
  --master-user-password huEE33z2Qvl383 \
  --allocated-storage 20 \
  --availability-zone ca-central-1a \
  --backup-retention-period 0 \
  --port 5432 \
  --no-multi-az \
  --db-name cruddur \
  --storage-type gp2 \
  --publicly-accessible \
  --storage-encrypted \
  --enable-performance-insights \
  --performance-insights-retention-period 7 \
  --no-deletion-protection
```

![aws cli rds](https://user-images.githubusercontent.com/125069098/225329852-4e41a770-ac32-48b9-9bc0-862ded19cbbd.png)
![RDS AWS](https://user-images.githubusercontent.com/125069098/225331265-e0010ae2-81f9-47bb-948b-7a2ec4fda43c.png)

To connect to psql via the psql client cli tool remember to use the host flag to specific localhost.

```
psql -Upostgres --host localhost
```
![connected postgres](https://user-images.githubusercontent.com/125069098/225335023-c3790889-02f1-4cb7-bd6d-64ab7d40b8cc.png)


Common PSQL commands:

```sql
\x on -- expanded display when looking at data
\q -- Quit PSQL
\l -- List all databases
\c database_name -- Connect to a specific database
\dt -- List all tables in the current database
\d table_name -- Describe a specific table
\du -- List all users and their roles
\dn -- List all schemas in the current database
CREATE DATABASE database_name; -- Create a new database
DROP DATABASE database_name; -- Delete a database
CREATE TABLE table_name (column1 datatype1, column2 datatype2, ...); -- Create a new table
DROP TABLE table_name; -- Delete a table
SELECT column1, column2, ... FROM table_name WHERE condition; -- Select data from a table
INSERT INTO table_name (column1, column2, ...) VALUES (value1, value2, ...); -- Insert data into a table
UPDATE table_name SET column1 = value1, column2 = value2, ... WHERE condition; -- Update data in a table
DELETE FROM table_name WHERE condition; -- Delete data from a table
```
![list dbs](https://user-images.githubusercontent.com/125069098/225337018-3b240ea2-c681-488d-9244-ad574464aeb3.png)

## Create (and dropping) our database

We can use the createdb command to create our database:

https://www.postgresql.org/docs/current/app-createdb.html
 

```
createdb cruddur -h localhost -U postgres
```

```sh
psql -U postgres -h localhost
```

```sql
\l
DROP database cruddur;
```
We can create the database within the PSQL client

```sql
CREATE database cruddur;
```
![create database](https://user-images.githubusercontent.com/125069098/225338222-c0518464-cf9f-49eb-84f5-4cbcaa88325f.png)

## Import Script

We'll create a new SQL file called `schema.sql`
and we'll place it in `backend-flask/db`

The command to import:
```
psql cruddur < db/schema.sql -h localhost -U postgres
```

## Add UUID Extension

We are going to have Postgres generate out UUIDs.
We'll need to use an extension called:

```sql
CREATE EXTENSION "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```
![schemadb](https://user-images.githubusercontent.com/125069098/225349548-c697f42a-d189-426a-9d2a-79c0939443be.png)


![image](https://user-images.githubusercontent.com/125069098/225352729-d5bac9b8-03b7-4b12-bdf8-33e01aec21cd.png)

### Set Connection_url as environment variables in gitpod

```sql
export CONNECTION_URL="postgres://postgres:password@localhost:5432/cruddur"
for Prod
export PROD_CONNECTION_URL="postgres://cruddur:password123@cruddur-db-instance.ccw9zxdbnyes.us-east-1.rds.amazonaws.com:5432/cruddur"
```
![image](https://user-images.githubusercontent.com/125069098/225353890-33d1346a-91ec-4dbe-b5b4-7352d993e45d.png)

![prod connection url](https://user-images.githubusercontent.com/125069098/225356753-8215395d-a152-4d06-b708-038d6b240246.png)

![image](https://user-images.githubusercontent.com/125069098/225352910-57595186-2f96-4a4f-bfdb-817e0ed65c4a.png)

## Shell Script to Connect to DB

For things we commonly need to do we can create a new directory called `bin`

We'll create an new folder called `bin` to hold all our bash scripts.

```sh
mkdir /workspace/aws-bootcamp-cruddur-2023/backend-flask/bin
```

```sh
export CONNECTION_URL="postgresql://postgres:pssword@127.0.0.1:5433/cruddur"
gp env CONNECTION_URL="postgresql://postgres:pssword@127.0.0.1:5433/cruddur"
```

We'll create a new bash script `bin/db-connect`

```sh
#! /usr/bin/bash

psql $CONNECTION_URL
```
We'll make it executable:

```sh
chmod u+x bin/db-connect
```

To execute the script:
```sh
./bin/db-connect
```

# create bash script files in backend-flask/bin folder.
To excute the files we need to give execution permission to the files

![chmod to bash script](https://user-images.githubusercontent.com/125069098/225361048-38da90dd-28c7-48ae-8e06-c3c3e53d3b11.png)

## Shell script to drop the database

```bash
#! /usr/bin/bash

echo "db-drop"
NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")
psql $NO_DB_CONNECTION_URL -c "DROP database cruddur;"
```

![bash script drop](https://user-images.githubusercontent.com/125069098/225364349-66446e13-c5ec-45f3-8fb0-e4be51df9e52.png)

![create & drop db](https://user-images.githubusercontent.com/125069098/225366721-2892e0a8-667c-4720-8cf3-d139a4504edb.png)

## Shell script to create the database

```bash
#! /usr/bin/bash

echo "db-create"

NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")
psql $NO_DB_CONNECTION_URL -c "Create database cruddur;"
```
![bash script create](https://user-images.githubusercontent.com/125069098/225366105-a5cacf52-e797-4ee0-93b5-90d03212d78a.png)

## Shell script to load the schema

`bin/db-schema-load`

```sh
#! /usr/bin/bash

schema_path="$(realpath .)/db/schema.sql"

echo $schema_path

NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")
psql $NO_DB_CONNECTION_URL cruddur < $schema_path
```
```bash
#! /usr/bin/bash

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-schema-load"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"
schema_path="$(realpath .)/db/schema.sql"
echo $schema_path

if [ "$1" = "prod" ]; then
  echo "Running in production mode"
  URL=$PROD_CONNECTION_URL
else
  URL=$CONNECTION_URL
fi

psql $URL cruddur < $schema_path
```
![image](https://user-images.githubusercontent.com/125069098/225372809-a5ba578e-6dc2-490e-b581-49d1f7fbe3de.png)
![image](https://user-images.githubusercontent.com/125069098/225374880-0338a50a-eef7-4a11-aa9e-4cecef7af0cb.png)
![image](https://user-images.githubusercontent.com/125069098/225375445-d674c700-2be3-4a41-8c9d-39dbbecbe301.png)

## Shell script to connect to postgres

```bash
#! /usr/bin/bash

psql $CONNECTION_URL
```

![image](https://user-images.githubusercontent.com/125069098/225382454-6c9265d2-9955-47df-b046-4ce5477e3465.png)


## Create our tables

https://www.postgresql.org/docs/current/sql-createtable.html

```sql
CREATE TABLE public.users (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  display_name text,
  handle text,
  cognito_user_id text,
  created_at TIMESTAMP default current_timestamp NOT NULL
);
```
```sql
CREATE TABLE public.activities (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_uuid UUID NOT NULL,
  message text NOT NULL,
  replies_count integer DEFAULT 0,
  reposts_count integer DEFAULT 0,
  likes_count integer DEFAULT 0,
  reply_to_activity_uuid integer,
  expires_at TIMESTAMP,
  created_at TIMESTAMP default current_timestamp NOT NULL
);
```
```sql
DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.activities;
```
![image](https://user-images.githubusercontent.com/125069098/225381281-316cbcb2-7278-43c2-9e32-195eca4c2092.png)

![tables in cruddur db](https://user-images.githubusercontent.com/125069098/225383662-45c00296-ebf8-4e3c-af1a-434e696f945f.png)

## Shell script to insert rows to tables

'backend-flask\db\d\seed.sql
```sql
INSERT INTO public.users (display_name, handle, cognito_user_id)
VALUES
  ('Andrew Brown', 'andrewbrown' ,'MOCK'),
  ('Andrew Bayko', 'bayko' ,'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'andrewbrown' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )
 ``` 
## Shell script to seed data to tables

```bash
#! /usr/bin/bash

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-seed"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

seed_path="$(realpath .)/db/seed.sql"
echo $seed_path

if [ "$1" = "prod" ]; then
  echo "Running in production mode"
  URL=$PROD_CONNECTION_URL
else
  URL=$CONNECTION_URL
fi

psql $URL cruddur < $seed_path
```
![image](https://user-images.githubusercontent.com/125069098/225387659-55d0e92f-e6d9-4cc7-912a-d36a21ea1e6a.png)

https://askubuntu.com/questions/595269/use-sed-on-a-string-variable-rather-than-a-file

## See what connections we are using
```sh
NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")
psql $NO_DB_CONNECTION_URL -c "select pid as process_id, \
       usename as user,  \
       datname as db, \
       client_addr, \
       application_name as app,\
       state \
from pg_stat_activity;"
```
```bash
#! /usr/bin/bash

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-sessions"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

if [ "$1" = "prod" ]; then
  echo "Running in production mode"
  URL=$PROD_CONNECTION_URL
else
  URL=$CONNECTION_URL
fi


NO_DB_URL=$(sed 's/\/cruddur//g' <<<"$URL")
psql $NO_DB_URL -c "select pid as process_id, \
       usename as user,  \
       datname as db, \
       client_addr, \
       application_name as app,\
       state \
from pg_stat_activity;"
```
![sessions](https://user-images.githubusercontent.com/125069098/225635231-bbfa7801-8151-41f8-a6f7-430a7b0b1ee5.png)

Do the Docker-compose down and up again to see only the active session

![image](https://user-images.githubusercontent.com/125069098/225637577-df99e4b5-86e8-4b3f-b6d0-7df57713c222.png)

## Easily setup (reset) everything for our database


```sh
#! /usr/bin/bash
-e # stop if it fails at any point

#echo "==== db-setup"

bin_path="$(realpath .)/bin"

source "$bin_path/db-drop"
source "$bin_path/db-create"
source "$bin_path/db-schema-load"
source "$bin_path/db-seed"
```
![db-setup](https://user-images.githubusercontent.com/125069098/225639536-206724a9-5bbb-4167-b589-3d46d4ef01ba.png)

## Make prints nicer

We we can make prints for our shell scripts coloured so we can see what we're doing:

https://stackoverflow.com/questions/5947742/how-to-change-the-output-color-of-echo-in-linux

## Install postgres drivers for python

https://www.psycopg.org/psycopg3/

We'll add the following to our `requirments.txt`

```
psycopg[binary]
psycopg[pool]
```

```
pip install -r requirements.txt
```

## DB Object and Connection Pool

`lib/db.py`
```py
from psycopg_pool import ConnectionPool
import os

def query_wrap_object(template):
  sql = f"""
  (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
  {template}
  ) object_row);
  """
  return sql

def query_wrap_array(template):
  sql = f"""
  (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
  {template}
  ) array_row);
  """
  return sql

connection_url = os.getenv("CONNECTION_URL")
pool = ConnectionPool(connection_url)
```
In our home activities we'll replace our mock endpoint with real api call

```py
from lib.db import pool, query_wrap_array
       
      sql = query_wrap_array("""
      SELECT
        activities.uuid,
        users.display_name,
        users.handle,
        activities.message,
        activities.replies_count,
        activities.reposts_count,
        activities.likes_count,
        activities.reply_to_activity_uuid,
        activities.expires_at,
        activities.created_at
      FROM public.activities
      LEFT JOIN public.users ON users.uuid = activities.user_uuid
      ORDER BY activities.created_at DESC
      """)
      print(sql)
      with pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(sql)
          # this will return a tuple
          # the first field being the data
          json = cur.fetchone()
      return json[0]
```  
![sql query working](https://user-images.githubusercontent.com/125069098/225669198-3683e65c-c5fa-4701-9af7-8b037a8f7bea.png)

![driver sql working](https://user-images.githubusercontent.com/125069098/225668309-e8e954a6-3df6-457c-93d9-c1c234b90a0e.png)

Connect to RDS

> This will take about 10-15 mins

We can temporarily stop an RDS instance for 4 days when we aren't using it.

## Connect to RDS via Gitpod

![Hanging to connnect RDS](https://user-images.githubusercontent.com/125069098/225678794-f7caddc8-b3ff-4a87-a169-d9eb3b09c94d.png)


In order to connect to the RDS instance we need to provide our Gitpod IP and whitelist for inbound traffic on port 5432.

```sh
GITPOD_IP=$(curl ifconfig.me)
```

We'll create an inbound rule for Postgres (5432) and provide the GITPOD ID.

We'll get the security group rule id so we can easily modify it in the future from the terminal here in Gitpod.

![edit inbound rule to gitpod ip for postgres](https://user-images.githubusercontent.com/125069098/225686008-c852b412-e7b4-4462-818b-082777a87d9a.png)

![connect to RDS](https://user-images.githubusercontent.com/125069098/225685872-649c4291-460e-4024-8cfd-c38243350f94.png)

cruddur: \l To list the databases

![image](https://user-images.githubusercontent.com/125069098/225686462-bcbbd038-2e8e-464c-b83b-0e26757ec382.png)

```sh 
export DB_SG_ID="sg-09a083de1a3d3ba3e"
gp env DB_SG_ID="sg-09a083de1a3d3ba3e"

export DB_SG_RULE_ID="sgr-08525ddf8e5afbe53"
gp env DB_SG_RULE_ID="sgr-08525ddf8e5afbe53"
```
Whenever we need to update our security groups we can do this for access.

```sh
aws ec2 modify-security-group-rules \
    --group-id $DB_SG_ID \
    --security-group-rules "SecurityGroupRuleId=$DB_SG_RULE_ID,SecurityGroupRule={Description=GITPOD,IpProtocol=tcp,FromPort=5432,ToPort=5432,CidrIpv4=$GITPOD_IP/32}"
```


![image](https://user-images.githubusercontent.com/125069098/225689873-a1e2d3e9-3b90-4fde-b9ea-b3211a20ceee.png)
![image](https://user-images.githubusercontent.com/125069098/225690785-33ed38c7-9b51-4bc5-aa0a-d7b643209fa1.png)

 Add the command to postgres to add the gitpod ip when you login to gitpod
```docker 
command: |
      export GITPOD_IP=$(curl ifconfig.me)
      source  "$THEIA_WORKSPACE_ROOT/backend-flask/db-update-sg-rule"
```

![image](https://user-images.githubusercontent.com/125069098/225698193-bc88e8c1-1efa-4b6c-8618-0416fc971fd5.png)

![image](https://user-images.githubusercontent.com/125069098/225700357-08c871be-7cb1-43f9-8e23-627753c7f601.png)

Create lambda fucntion in AWS console
## Setup Cognito post confirmation lambda

### Create the handler function

- Create lambda in same vpc as rds instance Python 3.8
- Add a layer for psycopg2 with one of the below methods for development or production 

ENV variables needed for the lambda environment.
```
PG_HOSTNAME='cruddur-db-instance.czz1cuvepklc.ca-central-1.rds.amazonaws.com'
PG_DATABASE='cruddur'
PG_USERNAME='root'
PG_PASSWORD='huEE33z2Qvl383'
```

The function
```
import json
import psycopg2

def lambda_handler(event, context):
    user = event['request']['userAttributes']
    try:
        conn = psycopg2.connect(
            host=(os.getenv('PG_HOSTNAME')),
            database=(os.getenv('PG_DATABASE')),
            user=(os.getenv('PG_USERNAME')),
            password=(os.getenv('PG_SECRET'))
        )
        cur = conn.cursor()
        cur.execute("INSERT INTO users (display_name, handle, cognito_user_id) VALUES(%s, %s, %s)", (user['name'], user['email'], user['sub']))
        conn.commit() 

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if conn is not None:
            cur.close()
            conn.close()
            print('Database connection closed.')

    return event
```
### Development
https://github.com/AbhimanyuHK/aws-psycopg2

`
This is a custom compiled psycopg2 C library for Python. Due to AWS Lambda missing the required PostgreSQL libraries in the AMI image, we needed to compile psycopg2 with the PostgreSQL libpq.so library statically linked libpq library instead of the default dynamic link.
`

`EASIEST METHOD`

Some precompiled versions of this layer are available publicly on AWS freely to add to your function by ARN reference.

https://github.com/jetbridge/psycopg2-lambda-layer

- Just go to Layers + in the function console and add a reference for your region

`arn:aws:lambda:ca-central-1:898466741470:layer:psycopg2-py38:1`


Alternatively you can create your own development layer by downloading the psycopg2-binary source files from https://pypi.org/project/psycopg2-binary/#files

- Download the package for the lambda runtime environment: [psycopg2_binary-2.9.5-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl](https://files.pythonhosted.org/packages/36/af/a9f06e2469e943364b2383b45b3209b40350c105281948df62153394b4a9/psycopg2_binary-2.9.5-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl)

- Extract to a folder, then zip up that folder and upload as a new lambda layer to your AWS account

### Production

Follow the instructions on https://github.com/AbhimanyuHK/aws-psycopg2 to compile your own layer from postgres source libraries for the desired version.

![image](https://user-images.githubusercontent.com/125069098/225702312-a103a0c2-d975-424a-8687-eb9145a76cf4.png)

## Add the function to Cognito 

Under the user pool properties add the function as a `Post Confirmation` lambda trigger.


```py
import json
import psycopg2
import os

def lambda_handler(event, context):
    user = event['request']['userAttributes']
    print("userAttributes")
    print(user)

    user_display_name = user['name']
    user_email        = user['email']
    user_handle       = user['preferred_username']
    user_cognito_id   = user['sub']

    try:
      print('entered-try')  
      sql = f"""
         INSERT INTO public.users (
          display_name, 
          email,
          handle, 
          cognito_user_id
          ) 
        VALUES(
          '{user_display_name}', 
          '{user_email}',
          '{user_handle}',
          '{user_cognito_id}'
        )
      """ 
      print("SQL statement ---------")
      print(sql)
      conn = psycopg2.connect(os.getenv('CONNECTION_URL'))
      cur = conn.cursor()
      cur.execute(sql)
      conn.commit() 

    except (Exception, psycopg2.DatabaseError) as error:
      print(error)
        
    finally:
      if conn is not None:
          cur.close()
          conn.close()
          print('Database connection closed.')
    return event
```
![connected prod](https://user-images.githubusercontent.com/125069098/226068489-7dff01ea-025c-4e79-ab9d-ee2abcb15f45.png)

![user data prod](https://user-images.githubusercontent.com/125069098/226069027-208d1b46-7abe-468b-91e7-ed621d320c89.png)

![crud](https://user-images.githubusercontent.com/125069098/226069243-a3da65c1-c769-4824-b452-39eb8fb67bfc.png)
























