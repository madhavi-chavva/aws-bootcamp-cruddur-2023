# Week 9 — CI/CD with CodePipeline, CodeBuild and CodeDeploy

## PreParation
Create the following two scripts:
- Backend-flask/buildspec.yml, change the env variables to your owns
```yaml
# Buildspec runs in the build stage of your pipeline.
version: 0.2
phases:
  install:
    runtime-versions:
      docker: 20
    commands:
      - echo "cd into $CODEBUILD_SRC_DIR/backend"
      - cd $CODEBUILD_SRC_DIR/backend-flask
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $IMAGE_URL
  build:
    commands:
      - echo Build started on `date`
      - echo Building the Docker image...          
      - docker build -t backend-flask .
      - "docker tag $REPO_NAME $IMAGE_URL/$REPO_NAME"
  post_build:
    commands:
      - echo Build completed on `date`
      - echo Pushing the Docker image..
      - docker push $IMAGE_URL/$REPO_NAME
      - cd $CODEBUILD_SRC_DIR
      - echo "imagedefinitions.json > [{\"name\":\"$CONTAINER_NAME\",\"imageUri\":\"$IMAGE_URL/$REPO_NAME\"}]" > imagedefinitions.json
      - printf "[{\"name\":\"$CONTAINER_NAME\",\"imageUri\":\"$IMAGE_URL/$REPO_NAME\"}]" > imagedefinitions.json

env:
  variables:
    AWS_ACCOUNT_ID: 480134889878
    AWS_DEFAULT_REGION: us-east-1
    CONTAINER_NAME: backend-flask
    IMAGE_URL: 480134889878.dkr.ecr.us-east-1.amazonaws.com
    REPO_NAME: backend-flask:latest
artifacts:
  files:
    - imagedefinitions.json
```    
- aws/policies/ecr-codebuild-backend-role.json (For the newly created service role).
```json
{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "VisualEditor0",
        "Effect": "Allow",
        "Action": [
          "ecr:BatchCheckLayerAvailability",
          "ecr:CompleteLayerUpload",
          "ecr:GetAuthorizationToken",
          "ecr:InitiateLayerUpload",
          "ecr:PutImage",
          "ecr:UploadLayerPart",
          "ecr:BatchGetImage",
          "ecr:GetDownloadUrlForLayer"
        ],
        "Resource": "*"
      }
    ]
  }
 ``` 

Create a branch named prod, which will be used for AWS CodeBuild and CodePipeline later.

At AWS ECS, update desired tasks in the service to 1, if this was set to 0 before.

Before this week, if our backend is updated and needed to be deployed into production, we need to run 
- ./bin/backend/build, 
- ./bin/backend/push, 
- ./bin/backend/deploy. With the following setup, this can be done in a CI/CD fashion.

## AWS CodePipeline

Create a pipeline:
 #### Step1:
 - Login to your AWS console and select codepipeline.
 - Name it as `cruddur-backend-fargate` and new service role it automatically fill the role `AWSCodePipelineServiceRole-us-east-1-cruddur-backend-fargate`
 In the advanced setting select the `Default location` and `Default AWS Managed key`
 ![image](https://user-images.githubusercontent.com/125069098/235212747-7e2c12b6-6d03-4557-a2a8-28fe99266452.png)
 - click on next
 ### Step2:Add Source stage
 - Add the Source stage. Select the source provider as `GitHub(Version 2.0)` from the up-down list. click on `Connect to Github`set connection name as cruddur, 
   install a new app, select the cruddur repo, in the end finish "Connect to GitHub" and back to the pipeline page.
   select the cruddur repo and select branch `prod`, select `start the pipeline on source code change` and default output artifact format as `Codepipeline default` 
 ![image](https://user-images.githubusercontent.com/125069098/235213716-b5fdb71d-f27a-4485-977a-8691721b0f22.png)
 ### Step3: Skip this step for now we will build it later.
 ### Step4: 
 - For deploy stage, select deploy provide as `Amazon ECS`, choose cluster name as `cruddur`,service name as `backend-flask`
 ![image](https://user-images.githubusercontent.com/125069098/235217198-837ef26f-6bc2-40e0-9bef-a7c27e56f6f8.png)
### Review the Pipeline 
![image](https://user-images.githubusercontent.com/125069098/235217409-97b113eb-19d6-4ec9-9026-c6241642f5e4.png)
### Click on Create pipeline
![image](https://user-images.githubusercontent.com/125069098/235217633-36590f01-9a1e-45b0-a872-0721111e9d3e.png)

 ## AWS CodeBuild
 Create a build project:
 - Name as `cruddur-backend-flask-bake-image`, enable build badge
 - Source:
    - choose source provider as GitHub, repository in my GitHub account, select the cruddur repo, set source version to prod
    - select rebuild every time a code change is pushed to this repository, select single build, select event type as PULL_REQUEST_MERGED
 ![image](https://user-images.githubusercontent.com/125069098/235470897-982ba1a2-ad8c-4b5e-9861-6dd3b2ff7fc5.png)
 ![image](https://user-images.githubusercontent.com/125069098/235472149-e04aa2d1-4b0f-4099-9369-5a1f46a56b0c.png)
 ![image](https://user-images.githubusercontent.com/125069098/235473140-63075dac-8c97-44c3-a05b-8a83b3dd6e13.png)

- Environment:
    - Select managed image, select operating system as Amazon Linux 2, select standard runtime, select the latest image (4.0), select environment type as Linux, 
    tick privileged (for docker images we need to choose privileges)
    - Create a new service role automatically named as codebuild-cruddur-backend-flask-bake-image-service-role
    - Decrease timeout to 20 min, don't select any certificate nor VPC, select compute as 3 GB memory and 2 vCPUs
![image](https://user-images.githubusercontent.com/125069098/235473959-33485af3-06da-4152-b6a6-976af2e85d3a.png)
![image](https://user-images.githubusercontent.com/125069098/235474574-e960018b-6ff8-4262-9d3b-6456f71b959e.png)

- use a buildspec file `backend-flask/buildspec.yml`
![image](https://user-images.githubusercontent.com/125069098/235477745-eaa80f1c-82f6-4656-a474-8f5f9d9b1474.png)

- no artifects
![image](https://user-images.githubusercontent.com/125069098/235477911-eba7c0ed-e347-4740-a102-1201d1ae5a6a.png)

- select cloudwatch logs, set group name as `/cruddur/build/backend-flask`, stream name as `backend-flask`
![image](https://user-images.githubusercontent.com/125069098/235478761-1790bf8a-eba9-4cc0-9dcd-093467e4e469.png)
- Click create build project button
![image](https://user-images.githubusercontent.com/125069098/235479133-8758f01b-2df9-4d05-8746-0459f0833dba.png)
![image](https://user-images.githubusercontent.com/125069098/235479197-d7b027ef-1582-46b7-b3b8-96f9d07b3052.png)

For the newly created service role, attach a policy as shown in aws/policies/ecr-codebuild-backend-role.json in order to grant more permissions. 
Then click "Start build" (or triggered by a merge to the prod branch). If succeeded, you can check the build history for details.
![image](https://user-images.githubusercontent.com/125069098/235481843-df85b4f8-0d29-4f97-aabc-c8e9dd356084.png)


