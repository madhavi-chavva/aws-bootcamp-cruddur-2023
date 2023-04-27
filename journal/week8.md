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
Amazon CloudFront is designed to work seamlessly with S3 to serve your S3 content in a faster way. Also, using CloudFront to serve s3 content 
gives you a lot more flexibility and control. To create a CloudFront distribution, a certificate in the us-east-1 zone for *.<your_domain_name> is required.
If you don't have one yet, create one via AWS Certificate Manager, and click "Create records in Route 53" after the certificate is issued.

Create a distribution by:

- set the Origin domain to point to assets.<your_domain_name>
- choose Origin access control settings (recommended) and create a control setting
- select Redirect HTTP to HTTPS for the viewer protocol policy
- choose CachingOptimized, CORS-CustomOrigin as the optional Origin request policy, and SimpleCORS as the response headers policy
- set Alternate domain name (CNAME) as assets.<your_domain_name>
- choose the previously created ACM for the Custom SSL certificate.

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

##  Implement Users Profile Page
Implement a user profile page to show the avatar, banner, user displayname and number of cruds and edit button.
we need to modify some files ActivityFeed.js, CrudButton.js,HomeFeedPage.js,NotificationsFeedPage.js,UserFeedPage.js 
Add some new files EditProfileButton.css, EditProfileButton.js,ProfileHeading.css,ProfileHeading.js
create show.sql to get the handler from users

![Users Profile Page](https://user-images.githubusercontent.com/125069098/232868291-9705347e-4816-4247-8833-ce2e0734eebe.png)

## Implement Migrations Backend Endpoint and Profile Form

### DB Migration
Since our previous postgres database didn't have the column for saving bio, migration is required. We also need to update some backend scripts 
in order to let users edit bio and save the updated bio in the database.

Create an empty `backend-flask/db/migrations/.keep`, and an executable script `bin/generate/migration.
Run ./bin/generate/migration add_bio_column, a python script such as backend-flask/db/migrations/1681742424_add_bio_column.py will be generated. 
Edit the generated python script with SQL commands ALTER TABLE public.users to add column bio to the table and ALTER TABLE public.users to drop column bio 
From the table.

Update `backend-flask/db/schema.sql`, and update `backend-flask/lib/db.py` with verbose option.

Create executable scripts `bin/db/migrate` and `bin/db/rollback`. If we run `./bin/db/migrate`, a new column called bio will be created in the db table of users.


![image](https://user-images.githubusercontent.com/125069098/233137017-22f14503-e6bf-4fb3-8a29-6d7bfb119d53.png)

![generate add_bio_column file](https://user-images.githubusercontent.com/125069098/233137301-7a1ebbf6-a41c-4446-a210-abd3bbba6e60.png)

`Create a table for schema_information'

![image](https://user-images.githubusercontent.com/125069098/233140328-eca90d31-3582-4c10-a975-a591062166a7.png)

![image](https://user-images.githubusercontent.com/125069098/233147264-3053a47e-3ae4-4298-a079-4a63577de332.png)

![image](https://user-images.githubusercontent.com/125069098/233147461-a727aba3-17b4-468c-8ab4-09f9f5f55037.png)

![image](https://user-images.githubusercontent.com/125069098/233149649-70f079ae-6444-49e1-bbfc-1b26473268dc.png)

![image](https://user-images.githubusercontent.com/125069098/233162648-8f3600a3-12dc-4c73-8eb9-eeb7dc147540.png)

Unable to update the profile it is throwing an error 400

![image](https://user-images.githubusercontent.com/125069098/233166365-a4ffa889-1455-417f-86d3-178e8ff19c30.png)

![image](https://user-images.githubusercontent.com/125069098/233166409-00f47aa6-b9d7-44f7-8448-73bd8d89a582.png)

`Able to resolve the issue above 404 handle.` This issue was occuring because of the hardcoded value of andrewbrown in the DesktopNavigation.js file for the
handler unable to process the handler properly. I have replace the handler with my_handler then it is resolved and able to update the bio column in the postgres db.
![image](https://user-images.githubusercontent.com/125069098/233195505-d260b8df-233a-44e2-80b6-be76796bff73.png)

![image](https://user-images.githubusercontent.com/125069098/233195933-81d74a08-681a-492d-bc0e-435b117ff2a2.png)

![image](https://user-images.githubusercontent.com/125069098/233196388-d8a12cdf-8b27-4dfa-83d2-185c499863fb.png)
![image](https://user-images.githubusercontent.com/125069098/233196570-e1064894-873c-4cca-bcb8-274300d5848e.png)
![image](https://user-images.githubusercontent.com/125069098/233197016-16ff8ec4-c2f5-4151-98bf-96ad429a5869.png)

### Implement Avatar Uploading 
Firstly we need to create an API endpoint, which invoke a presigned URL like https://<API_ID>.execute-api.<AWS_REGION>.amazonaws.com. This presigned URL can give access to the S3 bucket (madhavi27-uploaded-avatars), and can deliver the uploaded image to the bucket.

We will call https://<API_ID>.execute-api.<AWS_REGION>.amazonaws.com/avatars/key_upload to do the upload, where the /avatars/key_upload resource is manipulated by the POST method. We will also create a Lambda function named CruddurAvatarUpload to decode the URL and the request. In addition, we need to implement authorization with another Lambda function named CruddurApiGatewayLambdaAuthorizer, which is important to control the data that is allowed to be transmitted from our gitpod workspace using the APIs.

- create a API Gateway endpoint with Http API in AWS console (To create a this we need a lambda function. So we create one lambda function)
  `create Lambda Function Name `cruddurAvatarUpload` Runtime ruby 2.7 and create a role for the lambda`
![image](https://user-images.githubusercontent.com/125069098/233452943-15ca4366-2737-4e7e-a180-79bd083cd1fa.png)
![image](https://user-images.githubusercontent.com/125069098/233453918-b52d23d0-d64a-4e5d-b89b-49341aba4a53.png)
![lambda](https://user-images.githubusercontent.com/125069098/233454179-ca731ddf-a83f-4732-b75e-b80f24aa421a.png)

- Create a Gemfile to libraries for ruby
![image](https://user-images.githubusercontent.com/125069098/233456101-8cecf4aa-fe34-499b-b577-85eaf0b86deb.png)
- install gem "aws-sdk-s3" and gem "ox"

![image](https://user-images.githubusercontent.com/125069098/233456582-9dad864a-21f2-4a32-980a-6d7b8fcfb404.png)

![image](https://user-images.githubusercontent.com/125069098/233457856-09ec27cc-4d1d-420f-a651-0c63d62d553b.png)

`Set environment variable bucketname in the gitpod`
```sh
export UPLOADS_BUCKET_NAME="madhavi27-uploaded-avatars"
gp env UPLOADS_BUCKET_NAME="madhavi27-uploaded-avatars"
```

```ruby
require 'aws-sdk-s3'
require 'json'

def handler(event:, context:)
  puts event
  s3 = Aws::S3::Resource.new
  bucket_name = ENV["UPLOADS_BUCKET_NAME"]
  object_key = 'mock.jpg'

  obj = s3.bucket(bucket_name).object(object_key)
  url = obj.presigned_url(:put, expires_in: 60 * 5)
  url # this is the data that will be returned
  body = {url: url}.to_json
  { statusCode: 200, body: body }
end
``` 
- Execute the ruby function to generate presignedUrl
![image](https://user-images.githubusercontent.com/125069098/233459312-9819eb12-4c0f-4220-bb4f-3df7f70d1726.png)

- Install the extension for vs code thunder client
![image](https://user-images.githubusercontent.com/125069098/233460398-d6a014d2-de36-4fc2-a8cd-7458fe92276e.png)

- upload a image and test it in the thunder client select PUT instead of get
![image](https://user-images.githubusercontent.com/125069098/233461806-0918863e-95e2-45ac-9e5f-7a914743e2f1.png)

![s3bucket](https://user-images.githubusercontent.com/125069098/233462002-7e2cbf5e-721e-48d0-b3eb-9919da219d1e.png)

### At AWS Lambda, create the corresponding two functions:

`CruddurAvatarUpload`

code source as seen in aws/lambdas/cruddur-upload-avatar/function.rb with your own gitpod frontend URL as Access-Control-Allow-Origin
rename Handler as function.handler
add environment variable UPLOADS_BUCKET_NAME
create a new policy PresignedUrlAvatarPolicy as seen in aws/policies/s3-upload-avatar-presigned-url-policy.json (code), and then attach this policy to the role of this Lambda

`CruddurApiGatewayLambdaAuthorizer`

upload lambda_authorizer.zip into the code source
add environment variables USER_POOL_ID and CLIENT_ID

Copy and paste the lambda function to into the lambda function(function.rb) and add permissions and environments variables to it.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::madhavi27-uploaded-avatars/*"
        }
    ]
}
```

![image](https://user-images.githubusercontent.com/125069098/233465520-a1f642d8-09af-4bd0-bfba-05efcf6e208a.png)

![image](https://user-images.githubusercontent.com/125069098/233465285-470840af-9afc-4fd9-85ff-0b267d0f1b51.png)
![image](https://user-images.githubusercontent.com/125069098/233465744-e722c781-513e-468a-88c4-17bef3e5b518.png)
![image](https://user-images.githubusercontent.com/125069098/233467622-788082ff-8400-42be-90a7-e7fceaa57697.png)

![image](https://user-images.githubusercontent.com/125069098/233468764-1058a891-40e3-42f9-b3f1-d79257e777bf.png)

### Verify the JWTs signed by Amazon Cognito

JavaScript library for verifying JWTs signed by Amazon Cognito, and any OIDC-compatible IDP that signs JWTs

- install the 
```json
npm install aws-jwt-verify
```
![image](https://user-images.githubusercontent.com/125069098/233481853-19f90c77-e492-42a3-a706-2a60070a6455.png)
![image](https://user-images.githubusercontent.com/125069098/233481952-5d8a543b-213a-47c1-b034-52509675e9dc.png)

This library can be used with Node.js 14 or higher. If used with TypeScript, TypeScript 4 or higher is required.
This library can also be used in Web browsers.

Download the node modules folder,index.js,package-lock.json,package.json from the gitpod and zip all the files. create a new lambda and upload the zip file.

- Create a new lambda function called CrudderApiGatewayLambdaAuthorizer with runtime Node.js.18x
![image](https://user-images.githubusercontent.com/125069098/233484499-f034a7e3-d08f-4985-b8c3-d3bbd9632faf.png)
![image](https://user-images.githubusercontent.com/125069098/233484695-b564f698-8135-42cb-8d27-15e06233c03f.png)

![image](https://user-images.githubusercontent.com/125069098/233484882-d84fb681-3d9c-430f-8d7a-080d33569666.png)
![image](https://user-images.githubusercontent.com/125069098/233485437-45554e63-a18a-459a-adea-a7878223bbe5.png)

Create API Gateway using HTTP API
![image](https://user-images.githubusercontent.com/125069098/233486111-d9523ae0-bce3-4d94-bd1a-c63de25cedc4.png)
![image](https://user-images.githubusercontent.com/125069098/233486739-e4a1b2ad-fee5-4db9-b018-edc6315162e5.png)
![image](https://user-images.githubusercontent.com/125069098/233487048-9069b22d-cbe5-47b1-96a2-c753543a8d6a.png)
![image](https://user-images.githubusercontent.com/125069098/233487115-b75e5a33-f43c-4864-85c1-077530eb4f2e.png)
![image](https://user-images.githubusercontent.com/125069098/233487216-55e38247-70fd-45e6-8c1c-1df049626864.png)
![image](https://user-images.githubusercontent.com/125069098/233488025-54a7f502-9f73-4e54-b4af-acead7fd9fbe.png)

set Authorization in the API Gateway
![image](https://user-images.githubusercontent.com/125069098/233488687-126dd56a-fc06-4628-9e35-922e50cc0820.png)
![image](https://user-images.githubusercontent.com/125069098/233488999-e39f9c33-da5a-4209-96a0-801ec64d8e80.png)
![image](https://user-images.githubusercontent.com/125069098/233489105-587b994b-4e52-4e8f-8e79-546f22d6750e.png)
![image](https://user-images.githubusercontent.com/125069098/233489306-483722f7-7243-4347-8ba1-df70a4a507c3.png)
![image](https://user-images.githubusercontent.com/125069098/233489405-5672439c-f291-48ee-8c17-98aa2db850db.png)
![image](https://user-images.githubusercontent.com/125069098/233489692-cdd61344-98ea-4b44-8ee5-2bfd05422341.png)

use the API gateway https://xikvwz17th.execute-api.us-east-1.amazonaws.com/avatars/key_upload in the browser

![image](https://user-images.githubusercontent.com/125069098/233490140-ef294a5e-4d71-4599-bbeb-6a1039b3c56f.png)

Add the code to profileform.js and profileForm.css 
![image](https://user-images.githubusercontent.com/125069098/233494918-da94667b-7e31-4335-898d-81d2a1acea34.png)

add the CORS to the API Gateway.
![image](https://user-images.githubusercontent.com/125069098/233495461-e89efd5f-df1b-4dcb-a9ee-bb2e67b37b2e.png)
![image](https://user-images.githubusercontent.com/125069098/233495759-c7e7009a-05fa-46d2-a1f2-831386990ce9.png)

## Fix CORS for API Gateway
- Lambda CruddurAvatarUpload: code source as seen in ./aws/lambdas/cruddur-upload-avatar/function.rb with my gitpod frontend url as Access-Control-Allow-Origin; renamed Handler as function.handler; environment variable UPLOADS_BUCKET_NAME has value <my_name>-cruddur-uploaded-avatars; its role attached the policy PresignedUrlAvatarPolicy.
- Lambda CruddurApiGatewayLambdaAuthorizer: code source as seen in zipped ./aws/lambdas/lambda-authorizer; add environment variables USER_POOL_ID and CLIENT_ID.
- API Gateway api.<my_domain>: route POST /avatars/key_upload with authorizer CruddurJWTAuthorizer which invoke Lambda CruddurApiGatewayLambdaAuthorizer, also with integration CruddurAvatarUpload; route OPTIONS /{proxy+} with no authorizer, and with integration CruddurAvatarUpload; No configuration for CORS.

`Create a {proxy+} with method option and attach a lambda to it`

![image](https://user-images.githubusercontent.com/125069098/233537220-931d8374-c739-4053-a384-806b7127fb17.png)
![image](https://user-images.githubusercontent.com/125069098/233536935-27b41e0a-b050-48c7-8552-133a1f2c2d89.png)
![image](https://user-images.githubusercontent.com/125069098/233537144-17a1e879-8dee-4eff-8eac-183d59e56021.png)

![image](https://user-images.githubusercontent.com/125069098/234720226-137339f7-5139-4a88-8dbd-e2d44ec1df9f.png)


`Create  custom domain name`

![image](https://user-images.githubusercontent.com/125069098/233535003-3c209dbe-2e8f-48ff-a210-f09a20006710.png)
![image](https://user-images.githubusercontent.com/125069098/233535062-21a730ab-75de-4b0e-9338-85381ebdba3c.png)


```python
"use strict";
const { CognitoJwtVerifier } = require("aws-jwt-verify");
//const { assertStringEquals } = require("aws-jwt-verify/assert");

const jwtVerifier = CognitoJwtVerifier.create({
  userPoolId: process.env.USER_POOL_ID,
  tokenUse: "access",
  clientId: process.env.CLIENT_ID//,
  //customJwtCheck: ({ payload }) => {
  //  assertStringEquals("e-mail", payload["email"], process.env.USER_EMAIL);
  //},
});

exports.handler = async (event) => {
  console.log("request:", JSON.stringify(event, undefined, 2));
  
  const auth = event.headers.authorization;
  const jwt = auth.split(" ")[1]
  try {
    const payload = await jwtVerifier.verify(jwt);
    console.log("Access allowed. JWT payload:", payload);
  } catch (err) {
    console.error("Access forbidden:", err);
    return {
      isAuthorized: false,
    };
  }
  return {
    isAuthorized: true,
  };
};
```

## Fix CORS Final AWS Lambda Layers
Edit the bucket policy for 

```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["PUT"],
        "AllowedOrigins": [
            "https://*.gitpod.io"
        ],
        "ExposeHeaders": [
            "x-amz-server-side-encryption",
            "x-amz-request-id",
            "x-amz-id-2"
        ],  
        "MaxAgeSeconds": 30000
    }
]
```

### Create a lambda layer to function cruddurAvatarUpload

Create a bash script file to generate a zip file for the JWT to add to the lambda layer.

![image](https://user-images.githubusercontent.com/125069098/234408534-b31b7fac-d899-4892-8889-82b8d5338aa8.png)

![image](https://user-images.githubusercontent.com/125069098/234408158-1fa60c4c-753b-444e-8c58-6b5dabb07d20.png)

![image](https://user-images.githubusercontent.com/125069098/234408394-3aaac22b-9126-457e-8dd9-ce11cdb1b2db.png)

Modify the code in the function.rb to get the access token, extension and cognito_user_uuid

```ruby
require 'aws-sdk-s3'
require 'json'
require 'jwt'

def handler(event:, context:)
  puts event
  if event['routeKey'] == "OPTIONS /{proxy+}"
    puts({step: 'preflight', message: 'preflight CORS check'}.to_json)
    { 
      headers: {
        "Access-Control-Allow-Headers": "*, Authorization",
        "Access-Control-Allow-Origin": "https://3000-madhavichav-awsbootcamp-csefsb1geah.ws-us95.gitpod.io",
        "Access-Control-Allow-Methods": "OPTIONS,GET,POST"
      },
      statusCode: 200
    }
  else
    token = event['headers']['authorization'].split(' ')[1]
    puts({step: 'presignedurl', access_token: token}.to_json)
    body_hash = JSON.parse(event["body"])
    extension = body_hash["extension"]

    decoded_token = JWT.decode token, nil, false
    cognito_user_uuid = decoded_token[0]['sub']

    s3 = Aws::S3::Resource.new
    bucket_name = ENV["UPLOADS_BUCKET_NAME"]
    object_key = "#{cognito_user_uuid}.#{extension}"

    puts({object_key: object_key}.to_json)
 
    obj = s3.bucket(bucket_name).object(object_key)
    url = obj.presigned_url(:put, expires_in: 60 * 5)
    url # this is the data that will be returned
    body = {url: url}.to_json
    { 
      headers: {
        "Access-Control-Allow-Headers": "*, Authorization",
        "Access-Control-Allow-Origin": "https://3000-madhavichav-awsbootcamp-csefsb1geah.ws-us95.gitpod.io",
        "Access-Control-Allow-Methods": "OPTIONS,GET,POST"
      },
      statusCode: 200, 
      body: body 
    }
  end # if 
end # def handler
```
Test the lambda function is triggered when you load a image into upload avatar in the frontend app

![image](https://user-images.githubusercontent.com/125069098/234409724-0f4f01eb-eedb-4697-bdad-491e712565cc.png)

This throwing an error of 404. I did a minor mistake in routes of API Gateway  (/avatar/key_upload/post) instead of /  mistypeed .
It was giving error. I have changed in the API Gateway 

![image](https://user-images.githubusercontent.com/125069098/234720799-58d5a614-2f93-4e5e-9e09-672c3540747b.png)
 
 After that I am able to generate logs for the `CrudderApiGatewayLambdaAuthorizer` lambda function but I still have some issues 404 and 500
 ![image](https://user-images.githubusercontent.com/125069098/234721015-f35e5b40-d7fa-41e3-9572-f1d4847a7738.png)

### Double Check Environment Variables
There are some environment variables and setups worth double checking:

- function.rb in CruddurAvatarUpload: set Access-Control-Allow-Origin as your own frontend URL.
- index.js in CruddurApiGatewayLambdaAuthorizer: make sure that token can be correctly extracted from the authorization header.
- Environment variables in the above two Lambdas were added.
- erb/frontend-react-js.env.erb: REACT_APP_API_GATEWAY_ENDPOINT_URL equals to the Invoke URL shown in the API Gateway.
- frontend-react-js/src/components/ProfileForm.js: gateway_url and backend_url are correctly set.
- Pay attention to variable name inconsistency in some scripts, e.g., cognito_user_uuid vs. cognito_user_id.

**RESOLUTION:** I have deleted the API GATEWAY and recreated it and change the Api gateway in the frontend-react-js.env.erb file and changed the frontend url 
of the gitpod in the lambda function `cruddurAvatarUpload`. Test it whether it is working or not this time it worked as excepted and able to upload the avatar 
in the s3 buckets `assets.madhavi27.xyz` and `madhavi27-uploaded-avatars`  

![triggers in lambda](https://user-images.githubusercontent.com/125069098/234939188-7fdd279d-12dd-4e1b-8fb1-6d77c90bc027.png)

![image](https://user-images.githubusercontent.com/125069098/234917596-df2b8330-d6f6-4ba3-9cc8-273d6cedd6b2.png)
![image](https://user-images.githubusercontent.com/125069098/234918386-89f760b7-d9f5-4ee2-8558-99ae08796f21.png)

![madhavi27-uploaded-avatars](https://user-images.githubusercontent.com/125069098/234918212-e2d6d5df-046e-4d17-852f-7adfddd68930.png)

![assets.madhavi27.xyz](https://user-images.githubusercontent.com/125069098/234919429-654c1351-efcf-48e4-9863-4f0a44e4205f.png)

## Render Avatar from CloudFront
create a cloudfront invalidation for the Object paths to avatars(like /avatars/*)

![image](https://user-images.githubusercontent.com/125069098/234950761-e1502e7f-5a64-4d35-8298-47f5cf99b17e.png)

create a file for profileAvatar.js to get the avatar from the s3 bucket via cloudfront. modify the in the following files.

- backend-flask/db/sql/users/show.sql
- frontend-react-js/src/components/ProfileAvatar.css
- frontend-react-js/src/components/ProfileAvatar.js
- frontend-react-js/src/components/ProfileHeading.css
- frontend-react-js/src/components/ProfileHeading.js
- frontend-react-js/src/components/ProfileInfo.js
- frontend-react-js/src/lib/CheckAuth.js
- frontend-react-js/src/pages/UserFeedPage.js

![image](https://user-images.githubusercontent.com/125069098/234930871-b6f6c4cc-3f45-4a27-abd2-f41bc8516c74.png)
















































