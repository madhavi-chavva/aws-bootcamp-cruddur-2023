# Week 1 — App Containerization
## Docker Architecture
 - Docker Architecture consist of docker client,docker deamon(Docker Host), and Registry(Docker hub).
 - Docker client send the command line instructions (like docker pull,docker push,docker run,docker build) to the docker deamon. Docker deamon is the heart of the docker
   which execute the docker commands using the **DOCKERFILE** instructions and build the images in the container.
 - Hub is a public/private storage for images. Images are used to run the containers.
 - Each container has a unique writable layer.This keeps container isolated while using the same image.Writable layer uses the union filesystem which does have a            performance  and they are tightly coupled to the host. Wriable layers are linked to the life cycle of the container.
 - Docker Image is a collection of file system layers.
 
 ## Dockerfile
 Docker can build images automatically by reading the instructions from a Dockerfile. A Dockerfile is a text document that contains all the commands a user could call on   the command line to assemble an image.Docker runs instructions in a Dockerfile in order.The instruction is not case-sensitive. However, convention is for them to be     UPPERCASE to distinguish them from arguments more easily. 
 Dockerfile contains the following instructions.
 
 - **FROM**: Set the base image for the build.
 - **LABEL**: Add metadata to an image.
 - **RUN**: Runs commands on the new layer like install or configuration.
 - **COPY**: Copies new files/folders from source(client machine) to destination(new image layer).
 - **ADD**: Add from a remote URL and do extration etc(adding application/web files)
 - **CMD**: Set the default execution of a container and arguments. Can be overridden via docker run parameter.
 - **ENTRYPOINT**: Same as CMD but can't be overridden. creates single purpose image.
 - **EXPOSE**: Informs docker what port the container app is running on.
 - **WORKDIR**: Sets the working directory for any RUN,CMD,ADD,ENTRYPOINT,COPY instructions that follow it in the Dockerfile. If it doesn't exists it will create            one,even it is not present in subsequent Dockerfile instruction. The WORKDIR can be used multiple times in Dockerfile.
 
 ## Containerize Backend
 ### Run python
 ```sh
cd backend-flask
export FRONTEND_URL="*"
export BACKEND_URL="*"
python3 -m flask run --host=0.0.0.0 --port=4567
cd ..
```
- make sure to unlock the port on the port tab
- open the link for 4567 in your browser
- append to the url to `/api/activities/home`
- you should get back json

### Add Dockerfile

Create a file here: `backend-flask/Dockerfile`

```dockerfile
FROM python:3.10-slim-buster

WORKDIR /backend-flask

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_ENV=development

EXPOSE ${PORT}
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]
```
### Build Container

```sh
docker build -t  backend-flask ./backend-flask
```

### Run Container
Run 
```sh
docker run --rm -p 4567:4567 -it backend-flask
FRONTEND_URL="*" BACKEND_URL="*" docker run --rm -p 4567:4567 -it backend-flask
export FRONTEND_URL="*"
export BACKEND_URL="*"
docker run --rm -p 4567:4567 -it -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask
docker run --rm -p 4567:4567 -it  -e FRONTEND_URL -e BACKEND_URL backend-flask
unset FRONTEND_URL="*"
unset BACKEND_URL="*"
```
Run in background
```sh
docker container run --rm -p 4567:4567 -d backend-flask
```
Return the container id into an Env Vat
```sh
CONTAINER_ID=$(docker run --rm -p 4567:4567 -d backend-flask)
```

## Get Container Images or Running Container Ids

```
docker ps
docker images
```
## Get container Images which are in exited state.
```
docker ps -a
```

### Send Curl to Test Server

```sh
curl -X GET http://localhost:4567/api/activities/home -H "Accept: application/json" -H "Content-Type: application/json"
```

### Check Container Logs

```sh
docker logs CONTAINER_ID -f
docker logs backend-flask -f
docker logs $CONTAINER_ID -f
```
###  Debugging  adjacent containers with other containers

```sh
docker run --rm -it curlimages/curl "-X GET http://localhost:4567/api/activities/home -H \"Accept: application/json\" -H \"Content-Type: application/json\""
```
busybosy is often used for debugging since it install a bunch of thing

```sh
docker run --rm -it busybosy
```

### Gain Access to a Container

```sh
docker exec CONTAINER_ID -it /bin/bash
```

> You can just right click a container and see logs in VSCode with Docker extension

### Delete an Image

```sh
docker image rm backend-flask --force
```
> docker rmi backend-flask is the legacy syntax, you might see this is old docker tutorials and articles.

> There are some cases where you need to use the --force

### Overriding Ports

```sh
FLASK_ENV=production PORT=8080 docker run -p 4567:4567 -it backend-flask
```

> Look at Dockerfile to see how ${PORT} is interpolated

## Containerize Frontend

## Run NPM Install

We have to run NPM Install before building the container since it needs to copy the contents of node_modules

```
cd frontend-react-js
npm i
```

### Create Docker File

Create a file here: `frontend-react-js/Dockerfile`

```dockerfile
FROM node:16.18

ENV PORT=3000

COPY . /frontend-react-js
WORKDIR /frontend-react-js
RUN npm install
EXPOSE ${PORT}
CMD ["npm", "start"]
```
### Build Container

```sh
docker build -t frontend-react-js ./frontend-react-js
```

### Run Container

```sh
docker run -p 3000:3000 -d frontend-react-js
```
## Multiple Containers

### Create a docker-compose file

Compose is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML file to configure your application’s services. Then, with a single command, you create and start all the services from your configuration.Compose works in all environments: production, staging, development, testing, as well as CI workflows. 
It also has commands for managing the whole lifecycle of your application:
 - Start, stop, and rebuild services
 - View the status of running services
 - Stream the log output of running services
 - Run a one-off command on a service
 
The **key features** of Compose that make it effective are:
 - Have multiple isolated environments using a single host.
 - Preserves volume data when containers are created.
 - Only recreate containers that have changed.
 - Supports variables and moving a compositon between environments.
 
 Create `docker-compose.yml` at the root of your project.

```yaml
version: "3.8"
services:
  backend-flask:
    environment:
      FRONTEND_URL: "https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
      BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
    build: ./backend-flask
    ports:
      - "4567:4567"
    volumes:
      - ./backend-flask:/backend-flask
  frontend-react-js:
    environment:
      REACT_APP_BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
    build: ./frontend-react-js
    ports:
      - "3000:3000"
    volumes:
      - ./frontend-react-js:/frontend-react-js

# the name flag is a hack to change the default prepend folder
# name when outputting the image names
networks: 
  internal-network:
    driver: bridge
    name: cruddur
```
![cruddur app](https://user-images.githubusercontent.com/125069098/220158475-d32ffbda-935e-405a-b57e-6f1fc6f2f2cd.png)

# Create the notification feature (Backend and Front)
Watched the video and did changes accordingly in the frontend app and backend app. I have encounted some issues but able to fix them.Finally able to get the proper out come out of it. 

![notification cruddur](https://user-images.githubusercontent.com/125069098/220436857-88ae5002-7cc0-4351-9f45-58bc389a5205.png)



## Adding DynamoDB Local and Postgres

We are going to use Postgres and DynamoDB local in future labs
We can bring them in as containers and reference them externally

Lets integrate the following into our existing docker compose file:
### Postgres

```yaml
services:
  db:
    image: postgres:13-alpine
    restart: always
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    ports:
      - '5432:5432'
    volumes: 
      - db:/var/lib/postgresql/data
volumes:
  db:
    driver: local
```

To install the postgres client into Gitpod

```sh
  - name: postgres
    init: |
      curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc|sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
      echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" |sudo tee  /etc/apt/sources.list.d/pgdg.list
      sudo apt update
      sudo apt install -y postgresql-client-13 libpq-dev
```
### DynamoDB Local

```yaml
services:
  dynamodb-local:
    # https://stackoverflow.com/questions/67533058/persist-local-dynamodb-data-in-volumes-lack-permission-unable-to-open-databa
    # We needed to add user:root to get this working.
    user: root
    command: "-jar DynamoDBLocal.jar -sharedDb -dbPath ./data"
    image: "amazon/dynamodb-local:latest"
    container_name: dynamodb-local
    ports:
      - "8000:8000"
    volumes:
      - "./docker/dynamodb:/home/dynamodblocal/data"
    working_dir: /home/dynamodblocal
```

Example of using DynamoDB local
https://github.com/100DaysOfCloud/challenge-dynamodb-local

## Volumes

directory volume mapping

```yaml
volumes: 
- "./docker/dynamodb:/home/dynamodblocal/data"
```

named volume mapping

```yaml
volumes: 
  - db:/var/lib/postgresql/data

volumes:
  db:
    driver: local
```

# Create a DynamoDB table
![create dynamodb table](https://user-images.githubusercontent.com/125069098/220440382-e23b9439-d61d-47ef-b916-7ca3ab417236.png)

# Create an item
![create an item](https://user-images.githubusercontent.com/125069098/220440623-717a6288-96d8-416a-ba4e-b48dae489c9a.png)

# List the tables:
![list tables](https://user-images.githubusercontent.com/125069098/220440928-c450ff64-5399-49e1-baad-dd8c4fcf8d8b.png)

# Get Records:
![get records](https://user-images.githubusercontent.com/125069098/220441168-e8e21d67-5e88-4577-92e4-c180b6924e94.png)

# Connecting to Postgres database
To connect to the Postgres Database client use
```postgres
psql -Upostgres --host localhost
```
![connecting to postgres client](https://user-images.githubusercontent.com/125069098/220447715-70985730-1b6b-4107-8698-5541a978cb5e.png)

# Homework Challenges
## Learn how to install a docker on your local machine and get the same containers running outside of gitpod/codespaces

 I have refer to the link [docker desktop on windows](https://docs.docker.com/desktop/install/windows-install/)
 I have already installed docker desktop before bootcamp while was self learning about the docker container.
 1. Clone the repository using git bash to your local machine.
 2. Build the image using the command
   ```docker
   docker build -t frontend-react-js ./frontend-react-js
   ```
 ![build frontend image](https://user-images.githubusercontent.com/125069098/220703245-7662210f-cde1-484b-a607-c71f1cc6787c.png)
 
 3. Run the docker container using the command:
   ```docker
   docker run -p 3000:3000 -d frontend-react-js
   ```
   ![run frontend container](https://user-images.githubusercontent.com/125069098/220704034-c7afbb45-39a8-47e5-9a02-421319d41943.png)
  4. Open a browser and enter http://localhost:3000/
  ![view container app](https://user-images.githubusercontent.com/125069098/220704466-f3859598-227f-4b87-b1af-67dc5ec082f0.png)
  
  ## push and tag a image to docker hub.
  1. build an **HellWorld** app in the app.py
  2. create a docker file.
  ```docker
  # syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /app

COPY requirements.txt /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT ["python3"]
CMD ["app.py"]

FROM builder as dev-envs

RUN <<EOF
apk update
apk add git
EOF

RUN <<EOF
addgroup -S docker
adduser -S --shell /bin/bash --ingroup docker vscode
EOF

# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /
```
3. build the docker image using docker build
```docker
docker image build -t flask_docker .
```
4. Run the docker image using the docker run
```
docker run -p 5000:8000 -d flask_docker
```
5.Tag the docker image using docker tag
```
docker tag flask_docker madhu2023/release0.0.1
```
6. Push the image into the docker hub
```
docker push madhu2023/release0.0.1 
```
![push dockerhub](https://user-images.githubusercontent.com/125069098/220719117-2b75d71e-6ac6-40f6-a0d8-5ddb7dc0da90.png)

## Research on Best practices for writing Dockerfiles
refered from the link [best practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
1.Create **ephemeal** containers. ephemeal means containers can be stoped and destroyed and rebuilt and replaced with minimum set up and configuration.
2.Build from a remote build context,using dockerfile from **stdin**
3.Exclude with **.dockerignore** :exclude the file not relevant to docker build, without reconstructing source repository, use .dockerignore similar to .gitignore files
4.Use **multi-stage** build: it allows to reduce the size of your final image,without struggling to reduce number of intermediate layers and files.
5.Don't install unnecessary packages.
6.Decoupling the application
7.Minimixe the number of layers
8.Sort multi-line arguments.

## Use nulti-stage building for a dockerfile build.

One excellent benefit of multi-stage Docker builds is that it reduces the number of dependencies and unnecessary packages in the image, 
reducing the attack surface and improving security. In addition, it keeps the build clean and lean by having only the things required to run your application in production.

```docker
  # syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /app

COPY requirements.txt /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT ["python3"]
CMD ["app.py"]

FROM builder as dev-envs

RUN <<EOF
apk update
apk add git
EOF

RUN <<EOF
addgroup -S docker
adduser -S --shell /bin/bash --ingroup docker vscode
EOF

# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /

## RUN the dockerfile CMD as an external script
1. Create a bash script file in backend-flask folder
```bash script
#!bin/bash
"python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"
```
![script](https://user-images.githubusercontent.com/125069098/220822927-7f508a57-be16-41bf-a573-7fd878ea6757.png)

2. Modify the dockerfile to include the script file.
```docker
FROM python:3.10-slim-buster

WORKDIR /backend-flask

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_ENV=development

EXPOSE ${PORT}
COPY script.sh /
RUN chmod +x script.sh
ENTRYPOINT [ "/script.sh" ]
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]
```
![dockerfile backend-flask](https://user-images.githubusercontent.com/125069098/220823279-e0d8954b-b142-4752-86bf-24f8ab5f7c4e.png)

3. Build the image using the docker build command.
```docker
docker build -t  backend-flask ./backend-flask
```
4. Run the container using the docker run command
```
docker run --rm -p 4567:4567 -it -e FRONTEND_URL='*' -e BACKEND_URL='*' -d backend-flask
```
![build run backend-flask](https://user-images.githubusercontent.com/125069098/220824026-05b0cb86-eeca-4ecb-b646-582d651c47f1.png)

**Do the same with frontend-react-js
1.  Create a bash script file in frontend-react-js folder
```bash script
#!bin/bash
npm start
```
```
![image](https://user-images.githubusercontent.com/125069098/220825269-43998478-1786-41![image](https://user-images.githubusercontent.com/125069098/220825343-59168246-d551-4446-8464-16de68fad739.png)
2.Modify the dockerfile to include the script file.
```docker
FROM node:16.18

ENV PORT=3000

COPY . /frontend-react-js
WORKDIR /frontend-react-js
RUN npm install
EXPOSE ${PORT}
COPY myscript.sh /
RUN chmod +x myscript.sh
ENTRYPOINT [ "/myscript.sh" ]
#CMD [ "npm", "start" ]
```
3. Build the image using the docker build command.
```docker
docker build -t frontend-react-js ./frontend-react-js
```
4. Run the container using the docker run command.
```docker
docker run -p 3000:3000 -d frontend-react-js
```
![build run frontend-react-js](https://user-images.githubusercontent.com/125069098/220825853-d2a328c2-f8b9-4235-8c14-d449d0e9fde6.png)

![localhost:3000](https://user-images.githubusercontent.com/125069098/220825601-7d52d335-5220-4b71-9403-771e738c59f7.png)


## Implement a healthcheck on the docker compose file
Health checks are exactly what they sound like - a way of checking the health of some resource. In the case of Docker, a health check is a command used to determine the health of a running container.When a health check command is specified, it tells Docker how to test the container to see if it's working. With no health check specified, Docker has no way of knowing whether or not the services running within your container are actually up or not.
In Docker, health checks can be specified in the Dockerfile as well as in a compose file.
A health check is configured in the Dockerfile using the **HEALTHCHECK** instruction.
```
HEALTHCHECK [OPTIONS] CMD command
```



   
    
    
  


 










