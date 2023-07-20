# Week X  — Cleanup

## CFN Static Website Hosting Frontend
Create a cloudformation stack to create frontend
  - CloudFront Distribution
  - S3 Bucket for www.
  - S3 Bucket for naked domain
  - Bucket Policy
-create a config.toml 
```toml
[deploy]
bucket = 'cfn-artifacts-m'
region = 'us-east-1'
stack_name = 'CrdFrontend'

[parameters]
CertificateArn = 'arn:aws:acm:us-east-1:480134889878:certificate/8a62223d-469e-4094-8c9d-bbecb01bba5d'
WwwBucketName = 'www.madhavi27.xyz'
RootBucketName = 'madhavi27.xyz'
HostedZoneId = 'Z06037502PLIZIZKMQMI1'
```
- Run to provision the CFN stack resources `./bin/cfn/frontend `
- Remove the Type A record from the Route53 for the rootdomainname.
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/f00d90bc-cd2e-4cad-9f49-0f969a7f6ac8)

![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/d5c2553b-7eca-4f6e-88c8-1802792f405d)
For this we have to block public access for the 
```yaml
Reource:
RootBucket:
      PublicAccessBlockConfiguration:
        BlockPublicPolicy: false
 ```       
 ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/c9aeed4f-bc18-46d4-bbed-c8fc2f398486)
 
 I forgot to change the cruddur.com , www.cruddur.com in the  Distribution: resource of frontend
/template.yaml I changed and reprovision again this time I got different error.

 ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/bc7c5419-2a6d-445b-a124-fa5098fdaa88)
 
 To resolve this issue we have to edit the `HostedZoneId: Z2FDTNDATAQYW2` and hardcode for both the WwwBucketDomain and RootBucketDomain
 ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/4f6e620a-0868-421f-bdf0-2cdea7379f40)

 ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/b6cdea3f-4997-4bbb-9e6b-ddafe1c69b99)
 ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/51d7a3bb-049e-48af-a904-af5f78066ee1)
 ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/2a4bd025-d66d-4700-827e-13d35dc66140)
 
 ## CFN Diagramming Static Frontend
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/089f966b-d7f7-4c70-aa7e-1828c20dfa8a)

## Sync tool for static website hosting
- create a separate static build bash script file to run npm build.
Run it manually in the frontend-react-js path.
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/14618c71-4d31-4e40-b9e0-219ba0030263)
correct the warning for some of the file.
- Rerun the bash script file `bin/frontend/static-build`
- Once the static build is done zip the content of the build folder and upload into s3 bucket (madhavi.xyz)
 use the command `zip -r build.zip build/` to zip the contents of the folder build into the folder(frontend-react-js)
 ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/06ce0988-8745-4b72-8c17-5740f64c7e01)
- Download the build.zip into your laptop.
- Upload the files into your `s3 bucket (madhavi27.xyz which is public)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/bd152098-7993-4f45-966c-739deb24487d)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/d03a019a-f8c6-4c15-afb1-3361c2f1ea0a)
- Click to upload to s3.
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/4c3c4dfe-62fd-41d9-b79c-d85a811db0c4)
- Open the browser and open `madhavi27.xyz`
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/a8cfe341-8821-464e-a545-519b62215843)
Now it is showing us the web application.
**Install the sync tool to sync the changes in the s3 bucket.**
- Create new bash script file in bin/frontend/sync
- Install the aws_s3_website_sync using the command `gem install aws_s3_website_sync` to install the package aws_s3_website_sync 
  which we use in the bash script above.In your gitpod root folder.
  ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/4f41b2db-b6b8-4756-8ec8-956b436d4522)
- create a temp directory and create a file .keep
  use the command `git add -f temp/.keep`  - to add a file to the gitpod repo
  ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/13751fb4-744d-4364-8074-6238013e0938)

- create a file for sync-env to specify the evn vars in folder erb `erb/sync.env.erb` for the bash script file `bin/frontend/sync`
```ruby
SYNC_S3_BUCKET=madhavi27.xyz
SYNC_CLOUDFRONT_DISTRUBTION_ID=<cloudfront ID>
SYNC_BUILD_DIR=<%= ENV['THEIA_WORKSPACE_ROOT'] %>/frontend-react-js/build
SYNC_OUTPUT_CHANGESET_PATH=<%=  ENV['THEIA_WORKSPACE_ROOT'] %>/tmp/sync-changeset.json 
SYNC_AUTO_APPROVE=false
```
- modify the bash script file `bin/frontend/generate-env` to generate the env var for both the files frontend-react-js.env.erb and sync.env.erb
```sh
#!/usr/bin/env ruby

require 'erb'

template = File.read 'erb/frontend-react-js.env.erb'
content = ERB.new(template).result(binding)
filename = "frontend-react-js.env"
File.write(filename, content)

template = File.read 'erb/sync.env.erb'
content = ERB.new(template).result(binding)
filename = "sync.env"
File.write(filename, content)
```
- Generate the both the env files for frontend-react-js. using command `./bin/frontend/generate-env`
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/b8118686-1f92-4149-a919-09ac95e456b7)
- install package dotenv to upload the env files. 'gem install dotenv`
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/50764a26-6773-42cf-b656-ea807a160297)
-Run the sync bash script file '././bin/frontend/sync`
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/935f6349-c0eb-4485-bc91-8d0e7dbd5e1d)

**To Test the sync tool**
- Do a change to a file in the frontend app file like DesktopSidebar.js.
- Run the npm install build  by running bash script file `./bin/frontend/static-build` 
  once it is build.
  ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/0bed7e7a-8193-4cff-ad31-34b47cb41234)

- run the sync tool ruby script file `./bin/frontend/sync` to test whether it picked up our changes.
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/2064694c-97f8-4f3e-90eb-3d0b9391409a)
- type yes to apply the plan
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/fc36940c-0966-44c9-a2a8-885d5ce71f06)
- After the apply it will generate invalidation on the cloudfornt.
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/8cb4deb9-9383-4646-86d3-164b971b6ca9)
- Test the frontend app has picked up the changes in the browser madhavi27.xyz
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/a8087f29-1579-48d3-bbf3-4906925237f8)

**Github actions to build and deploy the sync**
- Create a new folder under the root .github/workflows and create a new file sync.yml(`.github/workflows/sync.yaml`)
```yaml
name: Sync-Prod-Frontend

on:
  push:
    branches: [ prod ]
  pull_request:
    branches: [ prod ]

jobs:
  build:
    name: Statically Build Files
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [ 18.x]
    steps:
      - uses: actions/checkout@v3
      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
      - run: cd frontend-react-js
      - run: npm ci
      - run: npm run build
  deploy:
    name: Sync Static Build to S3 Bucket
    runs-on: ubuntu-latest
    # These permissions are needed to interact with GitHub's OIDC Token endpoint.
    permissions:
      id-token: write
      contents: read
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Configure AWS credentials from Test account
        uses: aws-actions/configure-aws-credentials@v2
        with:
          role-to-assume: arn:aws:iam::387543059434:role/CrdSyncRole-Role-1N0SLA7KGVS8E
          aws-region: ca-central-1
      - uses: actions/checkout@v3
      - name: Set up Ruby
        uses: ruby/setup-ruby@ec02537da5712d66d4d50a0f33b7eb52773b5ed1
        with:
          ruby-version: '3.1'
      - name: Install dependencies
        run: bundle install
      - name: Run tests
        run: bundle exec rake sync
```
- Create a gemfile under `.github`  to install the dependencies like aws_s3_website_sync,dotenv,rake using the command `bundle update --bundler`
```gem
source 'https://rubygems.org'

git_source(:github) do |repo_name|
  repo_name = "#{repo_name}/#{repo_name}" unless repo_name.include?("/")
  "https://github.com/#{repo_name}.git"
end

gem 'rake'
gem 'aws_s3_website_sync', tag: '1.0.1'
gem 'dotenv', groups: [:development, :test]
```
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/ddb7c757-6838-4185-bcf6-1a5e8f869534)
it will generate the gemfile.lock file
- Create a rake file under the '.github' folder to sync the frontend-react-js files changes into the s3 bucket.
```ruby
require 'aws_s3_website_sync'
require 'dotenv'

task :sync do
  puts "sync =="
  AwsS3WebsiteSync::Runner.run(
    aws_access_key_id:     ENV["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key: ENV["AWS_SECRET_ACCESS_KEY"],
    aws_default_region:    ENV["AWS_DEFAULT_REGION"],
    s3_bucket:             ENV["S3_BUCKET"],
    distribution_id:       ENV["CLOUDFRONT_DISTRUBTION_ID"],
    build_dir:             ENV["BUILD_DIR"],
    output_changset_path:  ENV["OUTPUT_CHANGESET_PATH"],
    auto_approve:          ENV["AUTO_APPROVE"],
    silent: "ignore,no_change",
    ignore_files: [
      'stylesheets/index',
      'android-chrome-192x192.png',
      'android-chrome-256x256.png',
      'apple-touch-icon-precomposed.png',
      'apple-touch-icon.png',
      'site.webmanifest',
      'error.html',
      'favicon-16x16.png',
      'favicon-32x32.png',
      'favicon.ico',
      'robots.txt',
      'safari-pinned-tab.svg'
    ]
  )
end
```
- Create a cloudformation stack to create resources IAM role, OIDCProvider in the aws.
- create a file for the config.toml to pass the parameters.
- Create a bash script file to provision the changeset stack `aws/cfn/sync/template.yaml`.
- Run the bash script file `./bin/cfn/sync`
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/0592416f-1dc6-4231-8e0d-dba32ba91719)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/3c76508d-5cd1-439f-a841-6f40b7e2dda0)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/c1162158-9734-474d-aa69-ac38a929b534)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/b1478598-fab7-4c63-b021-658644a0a5aa)
- In aws console after the role is created add the inline permissions -getobject,putobject,listbucket,deleteobject
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/6ffe5bbe-4230-482b-9dd0-5b7fdda97dbc)
- Click on `Add Permissions`
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/62d29c09-171c-4633-b45a-582f4ccc9f75)
-Select `Create inline Policy`
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/3dc05a12-f7ac-41e9-af8c-940be7e952e0)
  - In service choose s3
  - In Actions select `GetObject,PutObject,ListBucket,DeleteObject
  ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/b0533b64-7fbe-4d8f-9fca-de05d066a7d8)
  - In Resources add the bucket ARN and objects
  ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/8d4df270-ec3b-4310-8345-11646eb359a0)
  ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/c70ea30d-3c3a-4885-aa99-c0d260980e13)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/69c6f11a-ed90-4039-b6df-c22944e0eef9)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/ab7ddd35-a617-4d1f-9895-72fac001a5ae)
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::madhavi27.xyz",
                "arn:aws:s3:::madhavi27.xyzI/*"
            ]
        }
    ]
}
```
  - Click on `Review policy` and give a name to the policy 's3AccessForSync` and Click on `Create Policy`
  ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/4b50fd72-9d7c-4581-a666-1075f32717e5)
  ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/e18357d1-7aed-4e02-8c6a-6ab860c182f8)
- Copy and paste the Role ARN `arn:aws:iam::480134889878:role/CrdSyncRole-Role-8AN0R7B0BZFS` in the sync.yaml file which you have created in 
 `.github/workflows/sync.yaml`
 Referenced documents:
 [github actions](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-nodejs)
 [github_action_configure-aws-credentials](https://github.com/aws-actions/configure-aws-credentials)
 
 ## Reconnect Database and Post Confirmation Lambda
 - Modify the CFN for the CICD to take `serviceName:backend-flask` and  decided not use a cross-stack name.
 - Provision the CFN cicd by running the bash script file. `./bin/cfn/cicd` once it is done
 - Provision the CFN-satck service  by running the bash script file `./bin/cfn/service`. Once it is provisioned
 - Now test it locally.
   -now change docker-compose.yaml file to point to the `Dockerfile.prod` for the build in service: backend-flask
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/444cfb0d-4393-431e-a17f-56dd419d7be7)
   - Do docker-compose up 
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/5cebef6a-2f1f-47f3-83db-301d94e29616)
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/7d1775b0-bd00-4545-89b1-9f46ece36332)
   check the backend-flask `api/activities/home` in the browser
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/b2fad7eb-86da-4f60-a65d-0392530bebe6)
   connect to the database by using the script file `./bin/db/connect`
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/a4e92052-9c1b-4b8d-a441-683cca50c85a)
   Now build the backend-flask docker file by the script `./bin/backend/build`
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/9e575ce2-9079-4d65-8c8b-f03709e2365a)
   Now push the image to the ecr.
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/20d4d5aa-feee-4823-bdc4-258d31e5eae6)
   provision the CFN service script run `./bin/cfn/service`
   then the backend-flask service is up and running 
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/df083c80-8afc-462b-80eb-3bfeb041487b)
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/5e2762c1-067f-4ac4-93fd-d9c93b79e733)
   check the backend-flask in the browser.
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/7747e3cb-902a-4a12-b671-d97af48ac0a5)
   check for the env| grep PROD in the gitpod local as it is connected to the older database.
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/2cde97a9-25d0-4e65-bb96-56ad906aed16)
   now change the prod_connectionurl to newer database.
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/a606c765-b79b-4be6-8b4c-ef9c0ccb429a)
   Add an InBound Rule to the rds security group `sg-0073f2378d229a436 - CrdDbRDSSG`
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/a9ebc727-f5dc-450c-ae19-09b89a086f99)
   Run the script to update the gitpod ip address in the security group '`sg-0073f2378d229a436 - CrdDbRDSSG` of rds. `./bin/rds/update-sg-rule` 
   In order to run the above script we need to export `securitygroup inbound rule` and `securitygroup ID` of the rds. 
   ```sh
   export DB_SG_RULE_ID="sgr-0f56b911f67bf1ce6"
   gp env DB_SG_RULE_ID="sgr-0f56b911f67bf1ce6"
   ```
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/084ee305-6623-41b7-aa54-c1baa84e12e2)
   
   ```sh
   export DB_SG_ID="sg-0073f2378d229a436"
   gp env DB_SG_ID="sg-0073f2378d229a436"
   ```
   export the gitpod ip address by executing curl ifconfig.me
   ```sh
   export GITPOD_IP=$(curl ifconfig.me)
   ```
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/7590bae9-75d3-4633-b6da-074ab689cca4)
   now execute the script `./bin/rds/update-sg-rule`
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/27fc8ba9-178c-4d6f-a85f-bcda64a63559)
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/6e7220df-b978-467b-95a6-086a2b50ca07)
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/15c6891c-459b-47ef-8f66-48555a916df9)
   Connect to the rds using the script file `./bin/db/connect prod`
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/6cd56a50-20d1-48a3-9c7d-cc62fa2d2ab1)
   Do a schema-load for the prod by running `./bin/db/schema-load prod`
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/d834377d-96e8-460c-bebc-3da0bb61a909)
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/2551f0a0-866b-4fc6-8877-e54f2bab7f64)
   Override the connection_url to Prod_connectionurl to run the migrate script.
   `CONNECTION_URL=$PROD_CONNECTION_URL ./bin/db/migrate`
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/b769ceb1-dee4-451c-8630-7dec20406deb)
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/d68c9244-5417-4f31-b3a8-003e6b84ec0e)
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/8ef6b3e3-4568-409b-9cc2-ff8681ceea14)
   - Edit the CFN stack frontend to through an error message. and redeploy the cfn stack using script `./bin/cfn/frontend ` 
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/9987f7bf-e44f-47b9-a866-560543dfb1a6)
   **Modify the changes to lambda function `cruddur-post-confirmation` **
   - Modify the lambda function `cruddur-post-confirmation` to trigger when you signin to the app and changed the connection url in env var from      cruddur-db-instance to cruddur-instance.
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/9c63e875-c649-4031-8fc8-c164fd9afb33)
   - create new security group CognitoLambdaSG it should contain outbound rule with `ALLTRAFFIC` 0.0.0.0/0 but no inbound rule.
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/46e771fe-a155-4a2f-b44b-a06cea7ce097)
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/369d7f77-9ddf-4480-a768-2132d81ba688)
   - change lambda `cruddur-post-confirmation`  -> configuration -> vpc change to new vpc and subnets and sg CognitoLambdaSG
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/0f5ebfa7-ff8a-465f-8424-3179694f0609)
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/09e2bcd4-f149-46e5-b2e8-d61280e864cd)
   - delete the cognitoUser and signup again
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/e3c6da2c-4177-438f-8aab-bf0072872e9e)
   - But the data is not inserted into the rds. modified the code in lambda function `cur.execute(sql,*params) to cur.execute(sql,params)`.
   ```py
   import json
import psycopg2
import os

def lambda_handler(event, context):
    user = event['request']['userAttributes']
    print('userAttributes')
    print(user)

    user_display_name  = user['name']
    user_email         = user['email']
    user_handle        = user['preferred_username']
    cognito_user_id    = user['sub']
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
          %(display_name)s,
          %(email)s,
          %(handle)s,
          %(cognito_user_id)s
        )
      """
      print('SQL Statement ----')
      print(sql)
      conn = psycopg2.connect(os.getenv('CONNECTION_URL'))
      cur = conn.cursor()
      params = {
        'display_name': user_display_name,
        'email': user_email,
        'handle': user_handle,
        'cognito_user_id': cognito_user_id
      }
      cur.execute(sql,params)
      conn.commit() 

    except (Exception, psycopg2.DatabaseError) as error:
      print('error:')
      print(error)
    finally:
      if conn is not None:
          cur.close()
          conn.close()
          print('Database connection closed.')
    return event
    ```
   
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/cbf58a19-3410-4675-9a17-34f62858ff3b)
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/ca2bf82a-c50e-4ec3-a5e2-e0e1bef8cd0b)
   ### post a crud
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/2d627ccf-3099-4ff1-ae1c-66d22c7fec7a)
   ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/91abb17b-00a8-4c55-bc79-927e72f25547)
   
   ## Use CORS for Service
   -Update the config.toml of the CFN stack aws/cfn/service/config.toml to pass the parameters for the 
   
   ```toml
   EnvFrontendUrl = 'https://madhavi27.xyz'
   EnvBackendUrl = 'https://api.madhavi27.xyz'
   ```
   - Also update the bash script file to pass the parameters into the CFN stack service in `bin/cfn/service`
   ```sh
   #! /usr/bin/env bash
set -e # stop the execution of the script if it fails

CFN_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/service/template.yaml"
CONFIG_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/service/config.toml"
echo $CFN_PATH

cfn-lint $CFN_PATH

BUCKET=$(cfn-toml key deploy.bucket -t $CONFIG_PATH)
REGION=$(cfn-toml key deploy.region -t $CONFIG_PATH)
STACK_NAME=$(cfn-toml key deploy.stack_name -t $CONFIG_PATH)
PARAMETERS=$(cfn-toml params v2 -t $CONFIG_PATH)

aws cloudformation deploy \
  --stack-name $STACK_NAME \
  --s3-bucket $BUCKET \
  --s3-prefix backend-service \
  --region $REGION \
  --template-file "$CFN_PATH" \
  --no-execute-changeset \
  --tags group=cruddur-backend-flask \
  --parameter-overrides $PARAMETERS \
  --capabilities CAPABILITY_NAMED_IAM
  ```
Reprovision the service stack cfn by running the script file `./bin/cfn/service`

![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/fcc329f8-e286-47ca-85fb-56a0415bed0f)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/36f93a29-a4b0-4112-b499-59b0f11a2d97)
when you do the crud it has to work with out errors. 
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/beaf5a44-456c-474f-9493-d6c1e2cbbfaf)

## CICD Pipeline and Create Activity
signup with another account and create another cognito user and signin with new user and make a crud request.
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/7ff5fda1-7517-47d9-800c-2d458bebc578)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/5b28c79b-f422-4535-8cc1-e3e2540ad555)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/64c0791d-a84e-41d9-a23a-720807f851ac)

Test the another cognito user in the development with the local postgres db.
Make sure the backend service in the docker-compose.yaml file is pointing to Dockerfile of local.
Run the docker-compose up once it is up and running.
seed the data into the local db. by running the script `./bin/db/setup`
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/48bf6fec-b81d-4bcb-85d1-c420ae480a4a)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/b792d3dc-acb1-4818-94ca-121af3036d5e)
Now run the script to update the cognito_user_id './bin/db/update_cognito_user_ids`
open the forntend app and signin with the new cognito user id and make a message post to crud. if the message post crud is not working make a
change in the `ActivityForm.js` to pass the bearer token.
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/b0407828-f911-42c9-863e-ee9aa38ec99e)

## Refactor JWT to use a decorator
- Modify the replyform.js to close the reply_popup onclick 
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/3bbed3c0-561d-4762-bcea-a0324b88b947)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/3311f433-b637-4c92-a62d-3afd84078acb)

-create a decorator that will handle JWT verification
Modify the code in app.py in backend-flask/app.py and backend-flask/lib/cognito_jwt_token.py
once it is done check the frontend app is working as expected.
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/c6a73fc7-1af7-47dd-87b5-94c53aeb9bc8)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/730ae70b-225d-464b-afe1-54d7ee970c14)

## Refactor app.py
By creating separate python files for the honeycomb,xray,cloudwatch,cors,rollbar and make sure all the errors are fixed and apps(backend & frontend apps) are working as expected.

## Refactor Flask Routes
creating separate python files for the routes based on activities, messages, general and users and import the files and load the route in the appy.py.
Make sure that the frontend and backend should be out of errors and work as expected.

## Impliment Reply is working for the app.

![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/43ec638c-7d12-4afe-8b40-1e1bf44bcf5c)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/7f183106-2bbe-472f-b544-1b88f9581cb2)

unable to post the reply due to mismatch of the type in the field.
Generate a migration file to change the field `reply_to_activity_uuid` from integer to string in the db schema  by running the script
`./bin/generate/migration reply_activity_uuid_to_string`
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/5d478b77-79d5-4602-a180-d28495d42deb)

![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/23d89829-8a53-4fe5-b208-4c807f26089f)
Run migrate to Alter table with field `reply_to_activity_uuid` to convert type integer to uuid
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/5ee2a8ee-ca49-41b1-b6bf-ae19bf9875d1)



![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/1a831548-da8e-43e3-b53d-30d478ded169)
Run migrate
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/032d156a-f9b0-4a81-8a3b-9be88f267983)
Make a new crud
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/48c9a83a-245d-4201-88c2-3c85ab6bb317)
when you refresh the browser the data should be persisted by it didn't
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/4ead8c30-8d29-425d-9d15-c9ff90366885)

Manually update the activities table to drop the column `reply_to_activity_uuid` and add a cloumn 'reply_to_activity_uuid` as `uuid`
using the commands.
```
ALTER TABLE activities DROP COLUMN reply_to_activity_uuid;
ALTER TABLE activities ADD COLUMN reply_to_activity_uuid uuid;
```
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/1efe4bec-d0f9-4598-82d4-4aab1d08a6d8)

![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/d088809e-4460-422e-a8b8-d4d2bbc4ec75)

![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/2ca35a3e-edc1-493d-87c4-c35d8d48b18d)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/678870ab-5af4-46c0-a36d-7168666d0f2d)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/bab8d1ac-29ed-4095-9984-3f3e0cbdfd54)

![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/f1ef7d11-11d4-4eb8-ace6-5b30a067ff38)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/f76c7369-7dfe-4036-b4d2-28ea9a19c2b4)

## Activity Show Page
Change the display name  and handler from div to links, also change the text docoration and underline for the display name and handler
in the files 
 - frontend-react-js/src/components/ActivityContent.js
 - frontend-react-js/src/components/ActivityContent.css

![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/1e8092bc-17cd-46f0-82a8-75bde3f4bac8)

Change the repost, share,like and reply to 
change the behaviour of the reply focus onclick
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/5b9b66b1-c26b-4ad6-868b-f8b46fd623d0)

- frontend-react-js/src/components/ActivityItem.css
- frontend-react-js/src/components/ActivityItem.js
- frontend-react-js/src/components/ActivityActionLike.js
- frontend-react-js/src/components/ActivityActionReply.js
- frontend-react-js/src/components/ActivityActionRepost.js
- frontend-react-js/src/components/ActivityActionShare.js
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/065e1da6-1de9-4eeb-aae2-85d3f16a179c)

## Week- X Cleanup
Insert other user values into the seed.sql manually by using the connect to rds script `./bin/db/connect 
```sql
INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'madhu' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  ),
  (
    (SELECT uuid from public.users WHERE users.handle = 'sunrise' LIMIT 1),
    'I am the other!',
    current_timestamp + interval '10 day'
  );
```
Seed other user into the postgres sql. and modify the files accordingly.
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/7bee7584-896a-4ad6-b1d1-3b150d474ba1)

Profile page with 2 users
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/2fbc7e63-3bf9-4d7c-85ae-162eb316e35d)

Implement back button on the `frontend-react-js/src/pages/ActivityShowPage.js` and stying on `frontend-react-js/src/pages/ActivityShowPage.css`
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/9e891465-76de-4d92-8917-6c48d5db5257)

Change the background color to black for the profile avatar
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/554cdf1a-c911-4405-a9cb-f8e362694c32)

Make a reply 
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/9f25d790-98f0-4bfa-8cf3-aaccbe528cc9)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/4dc1f98c-a6d2-49da-9cc0-a678e893df7f)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/91935ca3-6f73-4256-b2a9-5135f5438132)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/be5aad89-47c0-4bec-9ead-2d433664b829)

Build the backend by using new pull request if there are any merge conflicts resolve them. After merge request is confirmed a `codepipeline`
will be triggered. Make sure that the codepipeline is ran successfully.
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/fc37fdda-f563-4942-8f5a-0e85135c1f2f)

Compile the frontend app by using the script `./bin/frontend/static-build`. you will encounter compilation errors resolve them.
Once compilation is done. run the script `./bin/frontend/sync` to sync the new changes into the s3 bucket and into the cloudfront.
when I did a sync for the frontend.
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/1b3b0bf8-4287-4414-ab2a-faee848cfdd3)
Make sure that these `gem install dotenv and gem install aws_s3_website_sync` are installed before you run the script file sync `./bin/frontend/sync`
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/6de7a0e9-48f2-4b5e-adab-600ad05c403e)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/980bec7e-495a-4047-ab43-d328354f7217)

![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/8dda215d-8df9-4b24-86a6-d8c9123bb699)

Invalidations
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/a062ab2f-aa41-4af1-9210-dac5c5562a1a)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/90fcbc41-f145-453c-abdd-75e83565814f)

open the browser and enter your domain name like madhavi27.xyz.
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/c20800a3-b2b3-40df-8f72-c04a00b97269)

![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/b69a931c-4c88-49d5-bec9-eaeb7bdd1f42)
Make the change to the Dynamodb table name in the cfn service.
- aws/cfn/service/template.yaml
- aws/cfn/service/config.toml
- backend-flask/lib/ddb.py
- erb/backend-flask.env.erb
**Provision the `./bin/cfn/service`**
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/30a00ae6-449f-4fc3-a62a-1bddf1f240f4)

![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/b8f48600-5b80-4e69-9b0d-5d2122635ea3)
**Backend service is up and running**
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/bedabc03-6b95-4190-9f4c-da328bf24d54)
**Task-definition with latest changes for DynamoDB table**
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/208f8f33-3e41-4609-9e1e-7e264f5ebe69)

**write a cloudformation template to create a user with permissionn to write and read to dynamodb**
Create a new cfn template to create a new user 
 - aws/cfn/machine-user/config.toml
 - aws/cfn/machine-user/template.yaml
 - bin/cfn/machineuser
Run the script to create a new IAM machine user.`./bin/cfn/machineuser`
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/d3f2fe23-e0e0-44ec-9b53-17551d32fbe1)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/afe79154-ec26-4f2a-9de0-594819df373c)

Generate the secret credentials for machine user and update them in the `ssm Parameter store` in 
`/cruddur/backend-flask/AWS_ACCESS_KEY_ID` and `/cruddur/backend-flask/AWS_SECRET_ACCESS_KEY`
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/f4131d8a-fe9d-405b-8f2d-f4e7bd7f0027)

**Create a new pull request from the main to prod.**
create a new pull request from prod to week-x-again and the pipeline should work successfully.
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/4cb3cf39-78db-4eb3-a6ad-98131931fe4e)

Open a new browser and enter the domain [madhavi27.xyz](https://madhavi27.xyz/)
Login into alternate user and make a new message
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/6d8980ae-8913-4427-9e83-b9c1d550536b)
The messages are stored in the dynamoDB(CrdDdb-DynamoDBTable-6P6A39BV4R9E)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/bbfcf198-8e59-4094-8c65-8a1406a76abc)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/f9a89dc0-be58-4d50-9404-f4437ea79cf9)

### Implement the Rollbar for the production
Modify the code in `backend-flask/lib/rollbar.py' and un comment the code in `backend-flask/routes/general.py` and add environment variable in
`erb/backend-flask.env.erb'
```py
## XXX hack to make request data work with pyrollbar <= 0.16.3
def _get_flask_request():
    print("Getting flask request")
    from flask import request
    print("request:", request)
    return request
rollbar._get_flask_request = _get_flask_request

def _build_request_data(request):
    return rollbar._build_werkzeug_request_data(request)
rollbar._build_request_data = _build_request_data
## XXX end hack
def init_rollbar(app):
  rollbar_access_token = os.getenv('ROLLBAR_ACCESS_TOKEN')
  flask_env = os.getenv('FLASK_ENV')
  rollbar.init(
      # access token
      rollbar_access_token,
      # environment name
      'production',
      flask_env,
      # server root directory, makes tracebacks prettier
      root=os.path.dirname(os.path.realpath(__file__)),
      # flask already sets up logging
      allow_logging_basic_config=False)
  # send exceptions from `app` to rollbar, using flask's signal system.
  got_request_exception.connect(rollbar.contrib.flask.report_exception, app)
  return rollbar
```
- After the code changes are done run the backend build script using `./bin/backend/build`
- Add the `EnvFlaskEnv` environment variable in the cfn service `aws/cfn/service`
- Provision the cfn bash script `./bin/cfn/service` to pick the environment variable in the backend service. review the changes and execute changesets. once the backend service is up and running.
- Goto `Task Definition' of backend-flask and verify the environment variable is picked up or not.
  ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/8b18ca7f-c73e-43ca-b26c-aae31a0653b4)

## Profile picture update was not working[PUT 405 error].
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/058b528c-6f82-40b1-9041-8b13d55ebaac)
Changes need to be done for the production.
- change the `"Access-Control-Allow-Origin": ` in `Lambda(cruddurAvatarUpload)` to production url like `"https://madhavi27.xyz"' there shouldn't be any trailing backslash(/) at the end of the url.
 ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/5def7a5d-28a5-4895-b48a-1242177086ba) 
- change `bucket(madhavi27-uploaded-avatars)` cors permission
  ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/7776fe83-e874-4231-ab91-4265bbe29cf1)
  ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/107d6d8e-1e95-4d73-a508-c6f4762927be)
- Pass the `gateway_url environment variable(REACT_APP_API_GATEWAY_ENDPOINT_URL)' into the static-build file where we passed all other env vars 
  to the frontend app.
  ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/9dd97ba1-fd02-410e-b641-eb38703aa08b)
- Change the code in the `backend-flask/routes/users.py` from the method from Post to put
  ```py
  @app.route("/api/profile/update", methods=['PUT','OPTIONS'])
  @cross_origin()
  @jwt_required()
  def data_update_profile():
    bio          = request.json.get('bio',None)
    display_name = request.json.get('display_name',None)
    model = UpdateProfile.run(
      cognito_user_id=g.cognito_user_id,
      bio=bio,
      display_name=display_name
    )
    return model_json(model)
  ```
- push the backend changes by using the script `./bin/backend/build and ./bin/backend/push'
- Goto aws console to ECS and stop the running backend service and while unstill a new service is provisioned and running
  ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/780675ca-ce72-4347-9a58-51f5e5737be9)
- Push the frontend changes by running the script './bin/frontend/static-build and ./bin/frontend/sync`
- go to aws console cloudfront and check a new invalidation has been provisioned.
  ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/9f862805-162d-48a4-8bd7-0084a7ce9942)
- Now Go into your browser and launch the app(https://madhavi27.xyz) goto profile and update the avatar. It should work without any issues.
 ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/47d503dd-e789-4536-9dcc-810b9f443006)

## I had a issue with the Bio field which is not updating in the Rds.
With the fix of the profile picture update my bio is also working.
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/a5ed74f4-07f7-4980-9175-5b9153b01b25)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/8ba39cbc-4cbd-44c7-ac9a-1036a04ddd0e)

Login into your prod DB by using the script file `./bin/db/connect prod` check wheather the bio field is updated or not
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/8d100156-7ea7-440c-8485-ec14cec5113e)

## update the profile avatar of other user.(alternate user or second user)
- Remove the Hardcoded user handler in the `frontend-react-js/src/components/DesktopNavigation.js`
- Push the frontend changes by running the script './bin/frontend/static-build and ./bin/frontend/sync`
- Go to aws console cloudfront and check a new invalidation has been provisioned.
- Now Go into your browser and launch the app(https://madhavi27.xyz) goto profile and update the avatar. It should work without any issues.
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/c3a13d84-6a3d-4eba-a0e5-7737604a7819)
