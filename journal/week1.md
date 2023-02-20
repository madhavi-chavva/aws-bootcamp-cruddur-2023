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









