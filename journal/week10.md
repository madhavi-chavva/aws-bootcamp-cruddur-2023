# Week 10 — CloudFormation Part 1

## Create a ECS Cluster using Cloudformation template.

Create a Folder under AWS with `cfn/template.yaml`
```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: |
  Setup ECS Cluster
Resources:
  ECSCluster: #LogicalName
    Type: 'AWS::ECS::Cluster'
```

Create a bash script to deploy the aws cli command to deploy the cloudformation template.

```sh
#! /usr/bin/env bash
set -e # stop the execution of the script if it fails

CFN_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/template.yaml"
echo $CFN_PATH

aws cloudformation deploy \
 --stack-name "my-cluster" \
 --template-file "$CFN_PATH" \
  --no-execute-changeset \
  --capabilities CAPABILITY_NAMED_IAM
```
Run the script file to deploy the cloudformation template `./bin/cfn/deploy`

![image](https://user-images.githubusercontent.com/125069098/236894205-fb5d4c5b-b621-4c32-ba2e-3d80a33e9359.png)

copy and paste the command which is generated in the above statement. It give you the details of the changeset what it is going to deploy in aws.
eg: aws cloudformation describe-change-set --change-set-name arn:aws:cloudformation:us-east-1:480134889878:changeSet/awscli-cloudformation-package-deploy-1683567791/f666848f-f80a-4b46-bd1f-e5c4ab1aff90
![image](https://user-images.githubusercontent.com/125069098/236893833-18bc2af0-9f01-4d20-8b3e-6579ceea6f5c.png)
![image](https://user-images.githubusercontent.com/125069098/235775363-9f5b7307-2e50-4c8e-ae2c-d70de01908b0.png)

Also output in `table format`
![image](https://user-images.githubusercontent.com/125069098/236894820-3277734f-af63-44f6-96e9-3b251230e79b.png)

In AWS console `Cloudformation` you will see the changeset which you need to review the changes made to the resources you add or update to changeset before you `execute changeset`.
![image](https://user-images.githubusercontent.com/125069098/235777467-0d6f49e5-e369-41ec-89ca-d79ca76470e6.png)
![image](https://user-images.githubusercontent.com/125069098/235778407-ea4036a4-dddd-47f4-8b63-10533f0a187e.png)
**It has two options**
- Roll back all stack resources: Roll back the stack to the last known stable state.
- Preserve successfully provisioned resources: Preserves the state of successfully provisioned resources, while rolling back failed resources to the last known stable state.
Click on the `execute changeset`
![image](https://user-images.githubusercontent.com/125069098/235779386-7f1b8ecc-bd2f-4eb8-b850-a607f5c749d1.png)
![image](https://user-images.githubusercontent.com/125069098/235779456-72ee016c-9aa1-4ad4-89d7-8086517e1f11.png)
![image](https://user-images.githubusercontent.com/125069098/235779576-a6f10524-cee8-4d7f-9fd6-6d1643e72d60.png)

Modify the template.yaml file
```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: |
  Setup ECS Cluster
Resources:
  ECSCluster: #LogicalName
    Type: 'AWS::ECS::Cluster'
    Properties:
      ClusterName: MyCluster1
 ```
 Run the script `./bin/cfn/deploy`
 
 ![image](https://user-images.githubusercontent.com/125069098/235780463-1b70c62f-8b82-4afc-a72c-7dffc4a38747.png)

Goto Aws cloudformation changeset you will see modify this time with `Replacement = True`

![image](https://user-images.githubusercontent.com/125069098/235780824-b7c4616f-f44d-4dc8-80a4-34239e608bc8.png)


If you have errors in the cloudformation then you can check it in the `cloudTrail Event Histroy`
![image](https://user-images.githubusercontent.com/125069098/235781964-d70268f9-410f-4f55-90fe-5d8e10244cc5.png)

![image](https://user-images.githubusercontent.com/125069098/235781772-66822b3d-c081-44e1-ab82-bd161405dd41.png)

Introduce some errors in the template.yaml
```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: |
  Setup ECS Cluster
Resources:
  ECSCluster: #LogicalName
    Type: 'AWS::ECS::Cluster'
    Properties:
      ClusterName: MyCluster1
      CapacityProviders: ["NEARGATE"]
 ```
 Run the script `./bin/cfn/deploy`
 
 ![image](https://user-images.githubusercontent.com/125069098/235783225-f812f940-6674-4b03-8ac3-eaaf83fadb19.png)
![image](https://user-images.githubusercontent.com/125069098/235783619-0299e3e9-0c5b-4995-934a-1bd98ba9e362.png)

view the logs in the `CloudTrail Event History`
![image](https://user-images.githubusercontent.com/125069098/235784144-c0ad7574-299f-4d67-b5fc-72dd2c18eceb.png)

![image](https://user-images.githubusercontent.com/125069098/235784059-d6582db5-c786-4c73-86da-86dc0f5f5d71.png)


For Cloudformation validation we can use `aws cloudformation validate-template`

After you run the command, AWS CloudFormation will check the syntax and validate the contents of the template. If there are any errors or warnings, it will display them in the output.
```aws
aws cloudformation validate-template --template-body <value> [--template-url <value>]
```
 - --template-body or -t: The CloudFormation template that you want to validate, passed as a string or a file path. You must specify either --template-body or --template-url.

 - --template-url: The URL of the CloudFormation template that you want to validate. You must specify either --template-body or --template-url.

```aws
aws cloudformation validate-template --template-body file:////workspace/awsbootcampcruddur-2023/aws/cfn/template.yaml
```
![image](https://user-images.githubusercontent.com/125069098/235786717-4df150aa-5cd1-49d3-b82e-4aff1baff7ca.png)

Introduce some error
![image](https://user-images.githubusercontent.com/125069098/235786975-ea9fbe82-dccb-4df4-aabb-912e654061bf.png)

Install the lint to validate the error
```sh
pip install cfn-lint
```
![image](https://user-images.githubusercontent.com/125069098/235787579-03b7c40d-1c16-4a68-9fa7-7dd5ccdd3143.png)
![image](https://user-images.githubusercontent.com/125069098/235787857-0f2c4782-4686-42de-8fea-3b3596776f62.png)

Test the cfn-lint 
![image](https://user-images.githubusercontent.com/125069098/235788410-5dd8fc72-158a-4302-91a6-b5020511874a.png)

Install the cargo 
```sh
cargo install cfn-guard
```
 Is a command that installs the cfn-guard tool using the Rust package manager called Cargo.
 
 cfn-guard is an open-source tool developed by AWS that allows you to create policy rules in order to validate AWS CloudFormation templates. 
 The tool uses a simple YAML syntax for defining policy rules and supports a wide range of CloudFormation resources and property types.
 When you run cargo install cfn-guard, Cargo will download and compile the cfn-guard source code from the internet, and install the compiled binary on your local machine. Once you have installed cfn-guard, you can use it to validate your CloudFormation templates against your policy rules.
 
 Run the command 
 ```sh
 cfn-guard rulegen --template /workspace/awsbootcampcruddur-2023/aws/cfn/template.yaml
 ```
 ![image](https://user-images.githubusercontent.com/125069098/235791887-4e9d6813-a74e-4539-93b1-f45943640aad.png)

Create a s3 name `cfn-artifacts-m` in the aws console
![image](https://user-images.githubusercontent.com/125069098/235795184-15e1360a-eade-490a-aa9e-efb6f20de52e.png)

Run the `./bin/cfn/deploy`
![image](https://user-images.githubusercontent.com/125069098/235796139-248af015-9bdc-43d3-b1cd-429c4fd29d86.png)

![image](https://user-images.githubusercontent.com/125069098/235796081-3e26233b-a249-454d-8c17-b851855efbd6.png)

## CFN For Networking Layer
Set the environment variable s3 bucket artifacts in the gitpod.
```sh
export CFN_BUCKET="cfn-artifacts-m"
gp env CFN_BUCKET="cfn-artifacts-m"
```
Modify the bash script file bin/cfn/networking-deploy to use CFN_BUCKET

- create a folder aws/cfn/networking
create a cloudformation YAML template to create VPC, IGW, AttachIGW, RouteTable, RouteToIGW, public and private Subnets, SubnetRTAssociation and outputs.

- Run `./bin/cfn/networking-deploy`
![image](https://user-images.githubusercontent.com/125069098/236048122-9d27f99c-544b-471a-ba12-0b4118f37a40.png)
- Review the resources it is going to create and click on `execute changeset`
![image](https://user-images.githubusercontent.com/125069098/236047305-50f18795-b5fc-4643-ae7d-9872b23a28eb.png)
![image](https://user-images.githubusercontent.com/125069098/236047397-beea5d9a-59a8-43a6-b00c-5ef93b83cb0d.png)
Outputs after the execution of the changeset.
![image](https://user-images.githubusercontent.com/125069098/236047646-8b2d7ca6-03a8-4cdd-9bc0-a4f79c8aa79a.png)
![image](https://user-images.githubusercontent.com/125069098/236047763-c261c178-d567-4a58-8155-5c54c29d9bf9.png)
![image](https://user-images.githubusercontent.com/125069098/236047823-7ef543ed-bbf5-4b85-8b46-eec1ed740911.png)
![image](https://user-images.githubusercontent.com/125069098/236047903-d1edeef2-a6cb-480c-99ca-96bfb0c02840.png)

## CFN Diagramming the Network Layer

![CFN Diagramming the Network Layer](https://user-images.githubusercontent.com/125069098/236074797-45d7a797-8f79-4283-b0b7-88654cc57810.png)

## CFN Cluster Layer
 Create a cloudformation for 
 -ECS Fargate Cluster
 -ALB(Application LoadBalancer)
   - ipv4 only
   - internet facing
   - certificate attached from ACM(Amazon certificate Manager)
   - ALB Security Group
 - HTTPS Listerner
    - send naked domain to frontend Target Group
    - send api. subdomain to backend Target Group
 - HTTP Listerner
    - redirects to HTTPS Listerner
  - Backend Target Group
  - Frontend Target Group

- Delete the cluster's services frontend-react-js and backend which we have already created in week 6
- Delete the ALB and target group which we created already.
![image](https://user-images.githubusercontent.com/125069098/236561649-a9396262-e5fb-4a3a-a98d-c4eb6c9ba5ac.png)
![image](https://user-images.githubusercontent.com/125069098/236561908-600744ee-22f0-4e1e-8091-54728eca9254.png)
![image](https://user-images.githubusercontent.com/125069098/236562157-ad5abbd4-2900-4ca8-bace-bef708164a47.png)

![image](https://user-images.githubusercontent.com/125069098/236562027-54b86547-314c-438d-83d1-4a3d7d97aff3.png)
![image](https://user-images.githubusercontent.com/125069098/236562100-fa3e03b8-60a5-4aab-bfcf-3f229d7ce5fd.png)

![image](https://user-images.githubusercontent.com/125069098/236559953-74f97e05-846d-495b-b1ad-655dc61e0730.png)
![image](https://user-images.githubusercontent.com/125069098/236562265-6f4d49de-6ee2-4a59-bd75-bdca2cbc0c10.png)
![image](https://user-images.githubusercontent.com/125069098/236562385-57fc31a3-8fa1-449b-a76e-7828843c67ff.png)
![image](https://user-images.githubusercontent.com/125069098/236562461-3302140f-2ab6-445b-ac2e-f10f01d8a544.png)
![image](https://user-images.githubusercontent.com/125069098/236562995-d5446f17-8a4c-42c2-a775-09ef715a1a47.png)
![image](https://user-images.githubusercontent.com/125069098/236563095-eb0b2036-1176-441b-bd51-5689b363d07b.png)
![image](https://user-images.githubusercontent.com/125069098/236563176-fbc05a8c-6809-4b60-ad31-09406b3e894e.png)

Delete the namespace.(so to delete the namespace we need to go to cloudmap)

![image](https://user-images.githubusercontent.com/125069098/236563615-03db5f19-7f17-457a-93f1-af9849e4fe2b.png)
![image](https://user-images.githubusercontent.com/125069098/236563706-8f0b16ec-94a8-46c8-b110-1c0e833ea93a.png)
![image](https://user-images.githubusercontent.com/125069098/236563775-e319ea72-2935-4d82-b8e7-c3127cf03ddf.png)
![image](https://user-images.githubusercontent.com/125069098/236563879-63302fc5-e5ec-4fb2-86d9-68393c4eab71.png)

Execute the bash script file `bin/cfn/cluster-deploy` 
It gives an error for CertificateArn is not defined.

## CFN Toml 
To populate the Parameter value for CertificateArn install the cfn-toml
`gem install cfn-toml`
![image](https://user-images.githubusercontent.com/125069098/236931336-10a5161c-8459-476d-8d8a-674742d06abd.png)

Create a new file `aws/cfn/cluster/config.toml`
```cfn
[deploy]
bucket = 'cfn-artifacts-m'
region = 'us-east-1'
stack_name = 'CrdCluster'

[parameters]
CertificateArn = 'arn:aws:acm:us-east-1:480134889878:certificate/8a62223d-469e-4094-8c9d-bbecb01bba5d'
NetworkingStack = 'CrdNet'
```
Pass the parameters in the `aws/cfn/cluster/config.toml` to bash script file `bin/cfn/cluster-deploy`

```sh
#! /usr/bin/env bash
set -e # stop the execution of the script if it fails

CFN_PATH="/workspace/awsbootcampcruddur-2023/aws/cfn/cluster/template.yaml"
CONFIG_PATH="/workspace/awsbootcampcruddur-2023/aws/cfn/cluster/config.toml"
echo $CFN_PATH

cfn-lint $CFN_PATH

BUCKET=$(cfn-toml key deploy.bucket -t $CONFIG_PATH)
REGION=$(cfn-toml key deploy.region -t $CONFIG_PATH)
STACK_NAME=$(cfn-toml key deploy.stack_name -t $CONFIG_PATH)
PARAMETERS=$(cfn-toml params v2 -t $CONFIG_PATH)


aws cloudformation deploy \
  --stack-name $STACK_NAME \
  --s3-bucket $BUCKET \
  --region $REGION \
  --template-file "$CFN_PATH" \
  --no-execute-changeset \
  --tags group=cruddur-cluster \
  --parameter-overrides $PARAMETERS \
  --capabilities CAPABILITY_NAMED_IAM
```
Run the bash script file `./bin/cfn/cluster-deploy` Now it should pick the parameter CertificateArn.

![image](https://user-images.githubusercontent.com/125069098/236932537-cec37fb9-abe6-40ec-99cc-b948c48462a5.png)
![image](https://user-images.githubusercontent.com/125069098/236932719-1b456c12-be4d-46a8-ae95-22c88ca93253.png)
![image](https://user-images.githubusercontent.com/125069098/236932767-a45bc89a-4624-414f-82fa-2fd6319d26a4.png)
![image](https://user-images.githubusercontent.com/125069098/236932977-fceab96d-0cbb-4b7d-8e92-bec1848ec199.png)
![image](https://user-images.githubusercontent.com/125069098/236933062-faf7ce22-42bd-4b81-a879-f43159133c30.png)

### Outputs generated by cfn-stack.
`Fargate ECS`
![image](https://user-images.githubusercontent.com/125069098/236933385-5af428f7-7863-4f9e-8304-0548b4411052.png)
![image](https://user-images.githubusercontent.com/125069098/236933458-1847a22e-a34a-4499-91a9-9e22dbac0444.png)
`Target Groups`
![image](https://user-images.githubusercontent.com/125069098/236933686-d3cf5bcd-23ed-4c8c-8c26-63198992c598.png)
![image](https://user-images.githubusercontent.com/125069098/236933774-81faff57-5614-40f8-b6f0-9403d99c8cf8.png)
![image](https://user-images.githubusercontent.com/125069098/236933845-29832eee-0e7d-4a87-87c3-07209d15c9f5.png)
`ALB`
![image](https://user-images.githubusercontent.com/125069098/236934047-96e0d1f4-3f40-4119-a1d9-42fa0ddb18c9.png)
![image](https://user-images.githubusercontent.com/125069098/236934155-2cb72128-8460-45c9-82fb-ed35ddfc3470.png)
`Security Group`
![image](https://user-images.githubusercontent.com/125069098/236934427-85cbe481-450d-467c-8979-38125333eaa1.png)


In the same way create new file for networking `aws/cfn/networking/config.toml`

```cfn-toml
[deploy]
bucket = 'cfn-artifacts-m'
region = 'us-east-1'
stack_name = 'CrdNet'
```
Pass the values of bucket, region and stack-name in the `aws/cfn/networking/config.toml` to bash script file `bin/cfn/networking-deploy`

```sh
#! /usr/bin/env bash
set -e # stop the execution of the script if it fails

CFN_PATH="/workspace/awsbootcampcruddur-2023/aws/cfn/networking/template.yaml"
CONFIG_PATH="/workspace/awsbootcampcruddur-2023/aws/cfn/networking/config.toml"
echo $CFN_PATH

cfn-lint $CFN_PATH

BUCKET=$(cfn-toml key deploy.bucket -t $CONFIG_PATH)
REGION=$(cfn-toml key deploy.region -t $CONFIG_PATH)
STACK_NAME=$(cfn-toml key deploy.stack_name -t $CONFIG_PATH)
# PARAMETERS=$(cfn-toml params v2 -t $CONFIG_PATH)

aws cloudformation deploy \
  --stack-name $STACK_NAME \
  --s3-bucket $BUCKET \
  --region $REGION \
  --template-file "$CFN_PATH" \
  --no-execute-changeset \
  --tags group=cruddur-networking \
```
Run the bash script file `./bin/cfn/networking-deploy`

![image](https://user-images.githubusercontent.com/125069098/236932157-996b77d1-2f7f-45a2-a818-d133900a648d.png)
![image](https://user-images.githubusercontent.com/125069098/236932212-c125055d-7f6d-4b50-8681-d4d5306f9424.png)
![image](https://user-images.githubusercontent.com/125069098/236932276-ad039544-5786-4657-9d79-47da451e05b5.png)

## CFN Diagram Cluster

![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/6315ce47-8293-4155-b873-a186c3d03f65)

![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/b8c0b824-6d8e-4118-a960-6fbe365e082a)



## CFN Service Layer
Create outputs for the cloudformation stack `CrdCluster`
 - ClusterName
 - ALBSecurityGroupId
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/a4a526cf-e9db-4fff-b141-5d47b764a327)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/7b8e136b-e624-45ed-8253-fb8557558b15)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/2f40f84f-6a0b-45ab-a9ef-5ebdc9df8661)

Create a cloudformation stack for 
  - Task Definition
  - Fargate Service
  - Execution Role
  - Task Role
and use the outputs for the cloudformation stack `CrdCluster` and outputs for the cloudformation stack `CrdNet`

![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/5c5c7eb6-f95e-4f13-a6ba-38b01165d412)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/330a1774-72ad-45f2-801c-38e8807010cb)
Stack created the following resources but failed to create `FargateService` because ALB is not attached to the service.
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/5a145135-5799-471b-8b96-cdba2763903b)

## CFN ECS Fargate Service Debugging
Create outputs for the cloudformation stack `CrdCluster` 
 - FrontendTGArn
 - BackendTGArn
modify the FrontendTG and BackendTG to add as  `TargetType: ip` and add the `Tags`
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/34f70306-f280-47b3-9c62-ba5dd1a70a4f)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/9b1ecbbc-2a73-47a3-95a7-27c7d38c8f5d)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/d3ea78dc-e48f-4252-92e9-442b5d9247b9)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/20a9f4a6-0fbb-4ed4-99f3-f81ce7ee049d)

Modify cloudformation stack for `CrdSrvBackendFlask`
Add properties `ServiceConnectConfiguration` and import `TargetGroupArn` BackendTGArn
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/6c031bcc-6279-4057-a529-2b6bd1bc9765)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/c372597f-d374-4336-9f49-f9f679612239)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/666d67a2-f27d-403c-8acb-5ea5fde6fe3a)
![securitygroupinbound ALB](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/97c05ed8-8ae2-46e1-8f6e-2a113b8d5dac)
![securitygroupoutbound ALB](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/1ba8f345-7ae1-46a7-81ae-5e6aac15f53e)
![backend-flask service](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/9677cc56-55f9-4b2f-a866-2eb958f58bb0)
![health check](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/ad113e1f-a825-46c7-afac-03b578fe2765)

Change the TargetgroupArn and subnets for the `aws/json/service-backend-flask.json`
Run the `./bin/backend/deploy`
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/f111f49d-c408-4887-b9f2-b493c760af24)

Export the outputs for the  cloudformation stack `CrdSrvBackendFlask`
- ServiceSecurityGroupId
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/a44a086a-f684-40db-b383-91886d55bda7)

`service fails to deploy with unhealthy because the rds we deployed is in default VPC but our service is setup is setup in different vpc`. 
So we have to do database before we do service.

## CFN RDS
Create a cloudformation stack to create RDS.
The primary Postgres RDS Database for the application
  - RDS Instance
  - Database Security Group
  - DBSubnetGroup
 
 create a `config.toml`
 ```cfn
 [deploy]
bucket = 'cfn-artifacts-m'
region = 'us-east-1'
stack_name = 'CrdDb'

[parameters]
NetworkingStack = 'CrdNet'
ClusterStack = 'CrdCluster'
MasterUsername = 'cruddurroot'
```
create bash script to deploy the cfn `bin/cfn/db-deploy`
```sh
#! /usr/bin/env bash
set -e # stop the execution of the script if it fails

CFN_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/db/template.yaml"
CONFIG_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/db/config.toml"
echo $CFN_PATH

cfn-lint $CFN_PATH

BUCKET=$(cfn-toml key deploy.bucket -t $CONFIG_PATH)
REGION=$(cfn-toml key deploy.region -t $CONFIG_PATH)
STACK_NAME=$(cfn-toml key deploy.stack_name -t $CONFIG_PATH)
PARAMETERS=$(cfn-toml params v2 -t $CONFIG_PATH)

aws cloudformation deploy \
  --stack-name $STACK_NAME \
  --s3-bucket $BUCKET \
  --region $REGION \
  --template-file "$CFN_PATH" \
  --no-execute-changeset \
  --tags group=cruddur-cluster \
  --parameter-overrides $PARAMETERS MasterUserPassword=$DB_PASSWORD \
  --capabilities CAPABILITY_NAMED_IAM
```  


set the env var for MasterUserPassword in gitpod

```sh
export DB_PASSWORD=<"">
gp env DB_PASSWORD=<"">
```
Redeploy the `bin/cfn/cluster-deploy` 
To add the resouce `ServiceSG`
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/143385a8-ac50-4044-91ec-6daf4dc522ac)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/1a3fb2f6-595e-44b1-b86e-d93018f13847)

Deploy the rds postgres `bin/cfn/db-deploy`

![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/f3bce8ac-ce40-4a94-9c86-3be3fca5e23c)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/e6c88501-8933-4076-96a9-b15687c13737)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/715a7ace-29f5-43a5-96ce-67e5eb6ddc8b)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/2f27ecdd-2c0a-41c0-8582-fb217e25e4f0)


**Change the Endpoint url of the postgres with newly created db in the `parameter store`**.
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/4d70b6a1-2c65-4ec6-8748-f10791489b44)

## CFN Service Fixed
Change the targetgroup `CrdClu-Backe-AQLES3UBDF7B` health-check port to 4567
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/17d89838-bfa5-47d1-887a-d5617fc6bf43)

Modify the cloudformation stack `aws/cfn/cluster/template.yaml` file to change security group `ServiceSG` of `SecurityGroupIngress` 
to 4567 for both `FromPort and ToPort`

- Deploy the `bin/cfn/cluster-deploy`  to pick the changes.

- Deploy the `bin/cfn/service-deploy`
Check the ECS `CrdClusterFargateCluster` and check the health-check
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/df01be06-f2f5-475b-a023-462a5b613c14)

![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/d559013f-779f-4030-8eac-dba797ccd5a0)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/0d39b84a-66bc-439b-8f2b-baa57da3d085)

- Change `Route53` to pick the newly created ALB(dualstack.CrdClusterALB-1312429613.u-east-1.elb.amazonaws.com) for the api.madhavi27.xyz record.
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/7fadbc85-b5c8-4eca-ac7e-679842a857ea)

- Do the same thing for the record main(madhavi27.xyz)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/19ecbd46-9dad-43bd-8c44-2451818af91f)
- Open the browser and open the api.madhavi27.xyz/api/health-check
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/4654852a-6fb3-4468-aff2-d286dbbe4b0e)

**Resolution** for 503 service Temporarily  unavailable.
I haven't  changed the domain name for the `host-header` in cluster `ApiALBListernerRule` `aws/cfn/cluster/template.yaml` 
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/3afa59a3-5f5c-4433-a2de-6be09f5badb1)
changed the domain name
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/dc21a8e7-1256-4207-98f7-02f0f0aad667)

![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/11f137af-63dd-4e80-9e81-b77b3c927310)


- Test it in gitpod by pinging
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/ab2b93e4-450b-43ab-9bd9-5b7f2c0c8e87)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/62cd6aaa-c445-4d52-b8f8-afa0f7ec3275)

- Shell into the `backend-flask` with `TaskID` using the bash script `./bin/backend/connect taskID` before that change the
name of the cluster to `CrdClusterFargateCluster`
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/77a1387f-68f8-423d-9192-1eeed40b32cd)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/e2b253f7-6d31-4398-8015-3b096bbc6ee3)



## CFN - Diagramming Service and RDS

![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/533f803b-ecaf-463e-8e9a-21bc1d743d71)

## SAM CFN for Dynamodb DynamoDB Streams Lambda
- Create a cloudformation stack to create dynamodb.
  - DynamoDB Table
  - DynamoDB Stream
  - LambdaLogGroup
  - ExecutionRole for lambda
 - Install sam in the gitpod and also in the gitpod.yml
 ```sh
 wget https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip
 unzip aws-sam-cli-linux-x86_64.zip -d sam-installation
 sudo ./sam-installation/install
 ```
 ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/2b27aed2-5328-496e-ac8b-55939523009f)
-SAM stands for "Serverless Application Model." It is an open-source framework that allows you to define and deploy serverless applications on AWS.   SAM simplifies the process of building serverless applications by providing a simplified syntax for defining serverless resources such as       functions, APIs, and event sources.
- SAM uses a CloudFormation template syntax extension, which provides a shorthand notation for defining serverless resources. It makes it easier to express serverless application architectures and reduces the amount of code you need to write.
- SAM enables you to test and debug your serverless applications locally before deploying them to AWS. It provides a local development environment that mimics the AWS Lambda execution environment, allowing you to iterate quickly and catch issues early in the development process.
-  SAM simplifies the deployment process by providing commands to package and deploy your serverless applications. It handles the creation of necessary AWS resources, such as Lambda functions, API Gateway APIs, and event sources, based on the definitions in your SAM template.
-  SAM integrates with various AWS services to provide a comprehensive serverless application development experience. It supports easy configuration and integration with services like AWS Lambda, Amazon API Gateway, Amazon DynamoDB, Amazon S3, and more.
 - create a bash script file to sam build, sam package and sam deploy .
 ```sh
 #! /usr/bin/env bash
set -e # stop the execution of the script if it fails

FUNC_DIR="/workspace/aws-bootcamp-cruddur-2023/aws/lambdas/cruddur-messaging-stream/"
TEMPLATE_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/ddb/template.yaml"
CONFIG_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/ddb/config.toml"
ARTIFACT_BUCKET="cfn-artifacts-m"

# https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-build.html
sam build \
--config-file $CONFIG_PATH \
--template-file  $TEMPLATE_PATH \
--base-dir $FUNC_DIR
#--parameter-overrides

TEMPLATE_PATH="/workspace/aws-bootcamp-cruddur-2023/.aws-sam/build/template.yaml"
OUTPUT_TEMPLATE_PATH="/workspace/aws-bootcamp-cruddur-2023/.aws-sam/build/packaged.yaml"

# https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-package.html
sam package \
  --s3-bucket $ARTIFACT_BUCKET \
  --config-file $CONFIG_PATH \
  --output-template-file $OUTPUT_TEMPLATE_PATH \
  --template-file $TEMPLATE_PATH \
  --s3-prefix "ddb"

PACKAGED_TEMPLATE_PATH="/workspace/aws-bootcamp-cruddur-2023/.aws-sam/build/packaged.yaml"

# https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-deploy.html
sam deploy \
  --template-file $PACKAGED_TEMPLATE_PATH  \
  --config-file $CONFIG_PATH \
  --stack-name "CrdDdb" \
  --tags group=cruddur-ddb \
  --capabilities "CAPABILITY_IAM"
```
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/ddca83c7-de60-488a-aa9e-57f35d8a40b2)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/9e360fb3-b649-4dfa-8fcc-13dfe44797f0)

To fix the above issue in the local gitpod we have python 3.11 and lambda function is using python3.9. so we need to use the `--use-container` for
sam build to pick the runtime of different version.
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/6c61872c-5753-4831-960c-e1b760a07205)

Now the sam build is hanging on mounting. To resolve the mounting issue remove the `Architectures: - arm64` from `aws/cfn/ddb/template.yaml`
```yaml
ProcessDynamoDBStream:
    # https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html
    Type: AWS::Serverless::Function
    Properties:
      Architectures: 
        - arm64
```
Run the bash script file `./bin/sam/ddb/deploy
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/558f7960-09b6-4038-b7b6-cbd09af4f140)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/2b166446-a780-400a-a781-fdff79715698)
It is saying that the s3 upload zip file is empty.
Restructure the ddb folder and run the following files
- `./ddb/build`
- `./ddb/package`
- `./ddb/deploy`
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/923b3832-4297-44bb-924e-7ee60462b696)
when you run sam bash script file `./ddb/build` it will generate a zip with ProcessDynamoDBStream as shown below.
 ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/6eac25ee-dbe8-4acf-a0dd-d7960892bc97)
 
-  Run the bash script file `./ddb/build`
 ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/a9c9f413-7cb2-4f9a-a8c4-f5fa668fcf8a)
-  Run the bash script file `./ddb/package`
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/c1921075-4cf9-44eb-b716-8dee8eadc458)
-  Run the bash script file `./ddb/deploy`
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/3b907518-be53-497d-a826-5c3945ed689f)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/bd2716b8-5ac6-49d9-b445-833436cd043e)

![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/6e47ee0c-0c22-4ff3-a6ac-2c5c9315084b)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/0add22bb-adbc-403e-bdcd-d9a78ecdbf78)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/5f6de707-36ae-4906-b626-750ef190eb3d)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/b4610664-4a3e-45a0-bb46-766ce29bcb1f)

## Diagramming DynamoDB

![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/331fe50a-f1d0-464f-b16b-34dc689bd97a)

## CFN CICD 
- Create a cloudformation stack to create CICD.
  - CodeStar Connection V2 Github
  - CodePipeline
  - Codebuild
- create a nested cloudformation stack to create Codebuild Project.
  - Codebuild used for baking container images
  - Codebuild Project
  - Codebuild Project Role
- Modify the cloudformation stack `service aws/cfn/service/template.yaml` to generate the outputs for the ServiceName 
```yaml
Outputs:
  ServiceName:
    Value: !GetAtt FargateService.Name
    Export:
      Name: !Sub "${AWS::StackName}ServiceName"
```
- Run the bash script file './bin/cfn/service-deploy`
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/e0e7a0cf-6f60-4cb2-b8b8-8b54064b306c)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/91c0334d-a1d9-49dd-a82c-5bb162f3424c)
- Run the bash script file ` ./bin/cfn/cicd-deploy`
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/a83b7f47-d240-483b-87c1-98498a3941e8)

To resolve the above errors create a artifacts s3 bucket and include Property ConnectionName in Resources/CodeStarConnection/Properties
- include Property ConnectionName in Resources/CodeStarConnection/Properties
```yaml
CodeStarConnection:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html
    Type: AWS::CodeStarConnections::Connection
    Properties:
      ConnectionName: !Sub ${AWS::StackName}-connection
      ProviderType: GitHub 
```      
- create a new bucket manually in aws console with 'codepipeline-cruddur-artifacts-m` to store the artifacts.
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/ef887b99-0021-43d7-b3a4-b9d0d3055a1b)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/e221b183-3974-48e3-9129-1ac773155c34)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/f1f2eff5-b689-4f15-a1ac-7025ab93937e)

- specify the bucket name in the `aws/cfn/cicd/template.yaml` under the `resource pipeline`
```yaml
parameters:
  ArtifactBucketName:
    Type: String   
Pipeline:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html
    Type: AWS::CodePipeline::Pipeline
    Properties:
      ArtifactStore:
        Location: !Ref ArtifactBucketName
          Type: S3
      RoleArn: !GetAtt CodePipelineRole.Arn
      Stages:
```
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/d9e94488-a428-46c0-8334-62af1195bea9)

- In the bash script file you need to do cloudformation package before you deploy the cloudformation template. and output it to a tmp folder
(create a new temp folder) and output the package to that folder.
```sh
#! /usr/bin/env bash
#set -e # stop the execution of the script if it fails

CFN_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/cicd/template.yaml"
CONFIG_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/cicd/config.toml"
PACKAGED_PATH="/workspace/aws-bootcamp-cruddur-2023/tmp/packaged-template.yaml"
PARAMETERS=$(cfn-toml params v2 -t $CONFIG_PATH)
echo $CFN_PATH

cfn-lint $CFN_PATH

BUCKET=$(cfn-toml key deploy.bucket -t $CONFIG_PATH)
REGION=$(cfn-toml key deploy.region -t $CONFIG_PATH)
STACK_NAME=$(cfn-toml key deploy.stack_name -t $CONFIG_PATH)

# package
# -----------------
echo "== packaging CFN to S3..."
aws cloudformation package \
  --template-file $CFN_PATH \
  --s3-bucket $BUCKET \
  --s3-prefix cicd-package \
  --region $REGION \
  --output-template-file "$PACKAGED_PATH"

aws cloudformation deploy \
  --stack-name $STACK_NAME \
  --s3-bucket $BUCKET \
  --s3-prefix cicd \
  --region $REGION \
  --template-file "$PACKAGED_PATH" \
  --no-execute-changeset \
  --tags group=cruddur-cicd \
  --parameter-overrides $PARAMETERS \
  --capabilities CAPABILITY_NAMED_IAM
```
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/2d374600-4191-4a78-af39-341e0800c4b3)
-  Review the change sets in the cloudformation stack in aws and click on `execute changeset`
 
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/120e4f96-aa73-45e2-8130-df1b6ab66ead)

- change the version 2 to version 1 in `resource pipeline` in `CodeStarSourceConnection` in `ActionTypeId`
```yaml
Pipeline:
    # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html
    Type: AWS::CodePipeline::Pipeline
    Properties:
      ArtifactStore:
        Location: !Ref ArtifactBucketName
        Type: S3
      RoleArn: !GetAtt CodePipelineRole.Arn
      Stages:
        - Name: Source
          Actions:
            - Name: ApplicationSource
              RunOrder: 1
              ActionTypeId:
                Category: Source
                Provider: CodeStarSourceConnection
                Owner: AWS
                Version: '1'
              OutputArtifacts:
                - Name: Source

  ```
  ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/2dc7ddb9-65e9-4ad0-830b-52bdf7860a4a)
Navigate to codepipeline and check
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/197f2eb2-dcc2-4b48-9016-2b98d2fd3ede)
It failed for the first time because codestar connection(`CrdCicd-connection`) is in pending status.
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/fa555942-2205-49ff-b51a-79e4a2193d5a)

- navigate to aws and click on pending connection status and click on `Update pending connections`
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/3c3d4326-b6c3-4cf5-a8eb-4d741174ad45)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/585c7592-08db-4029-a6f1-ef239407d4fe)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/1d6879c4-f834-476d-b36b-11e9765b1453)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/0c03e676-6752-47fc-9080-0aa97f4e78ae)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/45d3d3ee-ac71-44ca-86b8-bd7b09c3a4ab)

## CFN Diagramming CICD

![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/68f6f1f7-1e1e-4d03-ad3b-b2777344df93)


![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/fa7257b1-d718-4775-8cdf-5b78b4c93c76)


 
 








`







      




    
