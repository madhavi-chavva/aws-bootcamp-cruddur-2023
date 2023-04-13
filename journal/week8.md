# Week 8 — Serverless Image Processing
## New Directory

Lets contain our cdk pipeline in a new top level directory called:

```sh
cd /workspace/aws-bootcamp-cruddur-2023
mkdir thumbing-serverless-cdk
```

## Install CDK globally

This is so we can use the AWS CDK CLI for anywhere.

```sh
npm install aws-cdk -g
```
![image](https://user-images.githubusercontent.com/125069098/231881637-2c3a9c23-d9c7-407e-ba7b-59e495db6b7c.png)


We'll add the the install to our gitpod task file
```sh
  - name: cdk
    before: |
      npm install aws-cdk -g
```


## Initialize a new project

We'll initialize a new cdk project within the folder we created:

```sh
cdk init app --language typescript
```
![image](https://user-images.githubusercontent.com/125069098/231881884-76546050-896e-42eb-aab2-9baa063deb9c.png)


## Add an S3 Bucket

Add the following code to your `thumbing-serverless-cdk-stack.ts`

```ts
import * as s3 from 'aws-cdk-lib/aws-s3';

const bucketName: string = process.env.THUMBING_BUCKET_NAME as string;

createBucket(bucketName: string): s3.IBucket{
   const bucket = new s3.Bucket(this, 'ThumbingBucket', {
    bucketName: bucketName,
    removalPolicy: cdk.RemovalPolicy.DESTROY
   });
   return bucket;
  }
    
```

```sh
export THUMBING_BUCKET_NAME="cruddur-thumbs"
gp env THUMBING_BUCKET_NAME="cruddur-thumbs"
```

- [Bucket Construct](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.Bucket.html)
- [Removal Policy](https://docs.aws.amazon.com/cdk/api/v1/docs/@aws-cdk_core.RemovalPolicy.html)

## Bootstrapping

> Deploying stacks with the AWS CDK requires dedicated Amazon S3 buckets and other containers to be available to AWS CloudFormation during deployment. 
cdk bootstrap should be done once for the your account for each region.

```sh
cdk bootstrap "aws://$AWS_ACCOUNT_ID/$AWS_DEFAULT_REGION"
```
![image](https://user-images.githubusercontent.com/125069098/231882645-672ccd31-3d1a-4755-9f3f-2e3a71112ffc.png)


## Build

We can use build to catch errors prematurely.
This jsut builds tyescript

```sh
npm run build
```


## Synth

> the synth command is used to synthesize the AWS CloudFormation stack(s) that represent your infrastructure as code.

```sh
cdk synth
```
![image](https://user-images.githubusercontent.com/125069098/231881120-f3f55bee-73f7-4aed-97fa-46e5559f11bd.png)
![image](https://user-images.githubusercontent.com/125069098/231882347-3b5e7cf0-cc55-4d17-9529-cdaa0d67c11a.png)
![image](https://user-images.githubusercontent.com/125069098/231883078-4ba52b75-4e65-4ab9-9eb3-c00b6298d9b7.png)


## Deploy

```sh
cdk deploy
```
deploying the cdk into cloudformation on aws console.
![image](https://user-images.githubusercontent.com/125069098/231885664-77309d09-c218-4cbd-b71f-781e7bdc0253.png)
![cloudformation](https://user-images.githubusercontent.com/125069098/231886327-2f4b25fb-eb41-4fc2-a070-76ba75fa0f51.png)
![s3 bucket](https://user-images.githubusercontent.com/125069098/231886536-1645141d-dd20-4128-a4cd-d83a0cadc729.png)


## List Stacks

```sh
cdk ls
```
![image](https://user-images.githubusercontent.com/125069098/231886743-75d7891c-dd0c-4c99-8b81-63024e623594.png)

## Create Lambda

