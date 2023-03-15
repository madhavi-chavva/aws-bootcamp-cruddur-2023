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












