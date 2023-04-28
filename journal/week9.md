# Week 9 — CI/CD with CodePipeline, CodeBuild and CodeDeploy

## PreParation
Create the following two scripts:
- Backend-flask/buildspec.yml, change the env variables to your owns
- aws/policies/ecr-codebuild-backend-role.json

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

 
 


 
 

