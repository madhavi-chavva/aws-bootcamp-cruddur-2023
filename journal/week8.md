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
![image](https://user-images.githubusercontent.com/125069098/232148093-42e92829-4048-4dd9-96c6-99b35be0c23b.png)

![image](https://user-images.githubusercontent.com/125069098/231881884-76546050-896e-42eb-aab2-9baa063deb9c.png)

## Create Environment Variables
You can create your own environment variable right in the Node REPL by appending a variable to the `process.env` object directly.

To use DotEnv, first install it using the command: `npm i dotenv`. 

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

## Deploy

```sh
cdk destroy
```
To destroy cdk stack destroy.

## Create .env file for the environment variables
```sh
THUMBING_BUCKET_NAME="assets.madhavi27.xyz"
THUMBING_S3_FOLDER_INPUT="avatars/original"
THUMBING_S3_FOLDER_OUTPUT="avatars/processed"
THUMBING_WEBHOOK_URL="https://api.madhavi27.xyz/webhooks/avatar"
THUMBING_TOPIC_NAME="cruddur-assets"
THUMBING_FUNCTION_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/lambda/process-images"
```

## Create Lambda

```ts
import * as lambda from 'aws-cdk-lib/aws-lambda';
const functionPath: string = process.env.THUMBING_FUNCTION_PATH as string;
const folderInput: string = process.env.THUMBING_S3_FOLDER_INPUT as string;
const folderOutput: string = process.env.THUMBING_S3_FOLDER_OUTPUT as string;

const lambda = this.createLambda(functionPath, bucketName, folderInput, folderOutput);
createLambda(functionPath: string, bucketName: string, folderInput: string, folderOutput: string): lambda.IFunction{
    const lambdaFunction = new lambda.Function(this, 'ThumbLambda', {
     runtime: lambda.Runtime.NODEJS_18_X,
     handler: 'index.handler',
     code: lambda.Code.fromAsset(functionPath),
     environment: {
      DEST_BUCKET_NAME: bucketName,
      FOLDER_INPUT: folderInput,
      FOLDER_OUTPUT: folderOutput,
      PROCESS_WIDTH: '512',
      PROCESS_HEIGHT: '512'
    }
    });
    return lambdaFunction;
   }
```   
![image](https://user-images.githubusercontent.com/125069098/232153031-b8c61c66-ec79-4078-a01a-316038ad5caa.png)
![image](https://user-images.githubusercontent.com/125069098/232153122-4a2ab5da-083d-466e-a54c-842dd170ccdb.png)
![lambda](https://user-images.githubusercontent.com/125069098/232153679-f818d789-a7af-4144-a1a6-7a2cc61df3e3.png)

## create bash script
`bin/serverless/build
```sh
#! /usr/bin/bash

ABS_PATH=$(readlink -f "$0")
SERVERLESS_PATH=$(dirname $ABS_PATH)
BIN_PATH=$(dirname $SERVERLESS_PATH)
PROJECT_PATH=$(dirname $BIN_PATH)
SERVERLESS_PROJECT_PATH="$PROJECT_PATH/thumbing-serverless-cdk"

cd $SERVERLESS_PROJECT_PATH

npm install
rm -rf node_modules/sharp
SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install --arch=x64 --platform=linux --libc=glibc sharp
```
![image](https://user-images.githubusercontent.com/125069098/232156799-a543348a-0f78-4028-9d08-02f0c44175b6.png)

## Create S3 Event Notification to Lambda

```ts
import * as s3n from 'aws-cdk-lib/aws-s3-notifications';
this.createS3NotifyToLambda(folderInput,laombda,bucket)

createS3NotifyToLambda(prefix: string, lambda: lambda.IFunction, bucket: s3.IBucket): void {
  const destination = new s3n.LambdaDestination(lambda);
    bucket.addEventNotification(s3.EventType.OBJECT_CREATED_PUT,
    destination,
    {prefix: prefix}
  )
}
```
![image](https://user-images.githubusercontent.com/125069098/232156758-64912447-3da1-4b24-acc3-f5f388a95c19.png)

![image](https://user-images.githubusercontent.com/125069098/232159412-1f5937c3-afae-46db-8c5a-3141e7be82a9.png)


`cdk deploy` to deploy the changeset
## create a bucket manually in aws console with bucket name `assets.madhavi27.xyz`. import the bucket into the cdk stack.
```js
const bucket = this.importBucket(bucketName);

importBucket(bucketName: string): s3.IBucket {
    const bucket = s3.Bucket.fromBucketName(this,"AssetsBucket",bucketName);
    return bucket;
  }
```  
![image](https://user-images.githubusercontent.com/125069098/232159028-41d4f247-a807-4976-b771-a3c8b3018f99.png)
![image](https://user-images.githubusercontent.com/125069098/232159485-d69a7859-4133-4383-a496-a314f5ecee63.png)

## create a bash script for upload and clear
```sh
#! /usr/bin/bash

ABS_PATH=$(readlink -f "$0")
SERVERLESS_PATH=$(dirname $ABS_PATH)
DATA_FILE_PATH="$SERVERLESS_PATH/files/data.jpg"

aws s3 cp "$DATA_FILE_PATH" "s3://assets.$DOMAIN_NAME/avatars/original/data.jpg"
```
```sh
#! /usr/bin/bash

ABS_PATH=$(readlink -f "$0")
SERVERLESS_PATH=$(dirname $ABS_PATH)
DATA_FILE_PATH="$SERVERLESS_PATH/files/data.jpg"

aws s3 rm "s3://assets.$DOMAIN_NAME/avatars/original/data.jpg"
aws s3 rm "s3://assets.$DOMAIN_NAME/avatars/processed/data.jpg"
```
## export the env var of domain name
```sh
export DOMAIN_NAME="madhavi27.com"
gp env DOMAIN_NAME="madhavi27.com"
```
![image](https://user-images.githubusercontent.com/125069098/232162869-6a194924-d2b9-4061-8e1a-634198809bb7.png)
![image](https://user-images.githubusercontent.com/125069098/232162964-bd7e0858-eb82-4faa-8d8c-edf16acead2a.png)
![image](https://user-images.githubusercontent.com/125069098/232163100-0eb1079f-8f53-451c-b0a5-9f12eb8af81d.png)

delete the Image
![image](https://user-images.githubusercontent.com/125069098/232163227-81886b40-75cb-49b7-8989-249c1abaefdc.png)

![image](https://user-images.githubusercontent.com/125069098/232163198-cd0b632a-14f8-4ab7-9d8c-c4134c251578.png)
![image](https://user-images.githubusercontent.com/125069098/232163688-812f6767-121e-445c-a715-06a8871db66b.png)

![s3 notification](https://user-images.githubusercontent.com/125069098/232163621-76e4b210-8ee1-4359-b942-72f2a953b32c.png)

![lambda](https://user-images.githubusercontent.com/125069098/232163756-1f463d88-0893-4e40-8265-34477feddcb8.png)

## Create Policy for Bucket Access

```ts
import * as iam from 'aws-cdk-lib/aws-iam';
const s3ReadWritePolicy = this.createPolicyBucketAccess(bucket.bucketArn)
// attach policies for permissions
lambda.addToRolePolicy(s3ReadWritePolicy);
createPolicyBucketAccess(bucketArn: string){
    const s3ReadWritePolicy = new iam.PolicyStatement({
      actions: [
        's3:GetObject',
        's3:PutObject',
      ],
      resources: [
        `${bucketArn}/*`,
      ]
    });
    return s3ReadWritePolicy;
  }
```
`cdk deploy`
![image](https://user-images.githubusercontent.com/125069098/232165513-59037b37-6959-43ce-a25c-7444c04bcd89.png)
![image](https://user-images.githubusercontent.com/125069098/232165553-84aed64f-666e-4e82-82a9-64ed483cd7b9.png)
![image](https://user-images.githubusercontent.com/125069098/232165450-e5d94b8d-8911-4c8e-85cf-43d8c98bdf68.png)
![cloudlogs](https://user-images.githubusercontent.com/125069098/232166865-04685356-6f6b-4bcd-9210-6460204f82ab.png)

![image](https://user-images.githubusercontent.com/125069098/232167568-41c95f7d-54c1-43fe-9e6f-fd30d3f7f4af.png)

## Create SNS Topic

```ts
import * as sns from 'aws-cdk-lib/aws-sns';

const snsTopic = this.createSnsTopic(topicName)

createSnsTopic(topicName: string): sns.ITopic{
  const logicalName = "Topic";
  const snsTopic = new sns.Topic(this, logicalName, {
    topicName: topicName
  });
  return snsTopic;
}
```

## Create an SNS Subscription

```ts
import * as s3n from 'aws-cdk-lib/aws-s3-notifications';

this.createSnsSubscription(snsTopic,webhookUrl)

createSnsSubscription(snsTopic: sns.ITopic, webhookUrl: string): sns.Subscription {
  const snsSubscription = snsTopic.addSubscription(
    new subscriptions.UrlSubscription(webhookUrl)
  )
  return snsSubscription;
}
```

## Create S3 Event Notification to SNS

```ts
this.createS3NotifyToSns(folderOutput,snsTopic,bucket)

createS3NotifyToSns(prefix: string, snsTopic: sns.ITopic, bucket: s3.IBucket): void {
  const destination = new s3n.SnsDestination(snsTopic)
  bucket.addEventNotification(
    s3.EventType.OBJECT_CREATED_PUT, 
    destination,
    {prefix: prefix}
  );
}
```
![image](https://user-images.githubusercontent.com/125069098/232168746-5a56a74c-2edd-4283-9910-a77283b5fab0.png)
![image](https://user-images.githubusercontent.com/125069098/232168780-e7b0eaba-effb-4e19-a044-7d344e46cb13.png)

![image](https://user-images.githubusercontent.com/125069098/232168898-d2abb1d6-edbf-46b4-b007-b7c6dc6c23ba.png)
![image](https://user-images.githubusercontent.com/125069098/232168942-64c49109-960e-487f-837a-470c6596a3cc.png)

## Setting up the cloudfront for Serving Avatars.

- Goto cloudfront on aws console
- click on create a cloudfront distribution
- select the origin domain name from drop down list, origin access to origin access control setting 
![image](https://user-images.githubusercontent.com/125069098/232503033-d8e26f0f-c00e-4ee9-89f3-ee91268d3cc5.png)
- create control settings
![image](https://user-images.githubusercontent.com/125069098/232503418-45682dd6-7421-4aa0-8a27-9fdad2a7eebc.png)
click create
![image](https://user-images.githubusercontent.com/125069098/232503731-6ec53aa5-9c40-4e5d-8c33-aa33f3e84c76.png)
![image](https://user-images.githubusercontent.com/125069098/232504243-a6240649-06b2-4bfb-a9c6-00a445a4443b.png)
![image](https://user-images.githubusercontent.com/125069098/232505836-dee38c79-8c90-4a61-af67-8ee65c57f0e0.png)
![image](https://user-images.githubusercontent.com/125069098/232506560-5658f151-ec73-4ac7-a4ec-b836796a9a27.png)
![image](https://user-images.githubusercontent.com/125069098/232507663-bae17479-3230-4bfc-bcb8-11b879efa917.png)
![image](https://user-images.githubusercontent.com/125069098/232508103-aa1bcb63-34f6-4980-9b71-563c73bd9378.png)
click on create distrbution
![image](https://user-images.githubusercontent.com/125069098/232508565-abab09fc-9e18-44cb-a0b8-fb1031dfd154.png)
- Create a new record for the cloudfront in the Route 53 hostedzone.
![image](https://user-images.githubusercontent.com/125069098/232513696-118fa0b3-0742-4cd2-ab47-09ff5867c2db.png)
![image](https://user-images.githubusercontent.com/125069098/232513878-7c81c753-d850-433a-870d-fda6e8c4cfa3.png)
-Test cloudfront is working in the bowser
![image](https://user-images.githubusercontent.com/125069098/232514770-b4f8e991-d562-4d15-974d-88684fc9fd29.png)
- Add a bucket policy to the s3 bucket (assets.madhavi27.xyz)
```json
{
        "Version": "2008-10-17",
        "Id": "PolicyForCloudFrontPrivateContent",
        "Statement": [
            {
                "Sid": "AllowCloudFrontServicePrincipal",
                "Effect": "Allow",
                "Principal": {
                    "Service": "cloudfront.amazonaws.com"
                },
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::assets.madhavi27.xyz/*",
                "Condition": {
                    "StringEquals": {
                      "AWS:SourceArn": "arn:aws:cloudfront::480134889878:distribution/E2ISHVF5HNPBX7"
                    }
                }
            }
        ]
      }
 ```     
![image](https://user-images.githubusercontent.com/125069098/232517608-4c3d1606-990d-4e17-941a-c8b6ded35e96.png)

-Test it in the browser.
![image](https://user-images.githubusercontent.com/125069098/232518463-e5b16097-fcd7-4ffe-9865-5c77751b4d28.png)

Modify the the cdk stack to create a bucket to uploaded-avartars and it has to upload the image into uploaded-avatar and assets bucket.

## Things to remember:
when you open the gitpod workspace first run the script./bin/avatar/build to install the sharp. Then perform cdk deploy then upload the image to the uploaded bucket then it has be copied into assets bucket. Otherwise you will get an error
![image](https://user-images.githubusercontent.com/125069098/232793877-5a2b0049-a73e-4e32-8919-7de46f36c3b8.png)





















