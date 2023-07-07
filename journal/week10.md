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

- Edit the config.toml with the `GithubRepo = 'madhavi-chavva/aws-bootcamp-cruddur-2023'` 
then click on the `release changes` then it has to pick the source changes.
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/ce69d427-867b-47ae-876b-4aeeca228156)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/5b628928-cf06-440e-a06a-c386ea6c4b70)
- codepipeline has failed because of the build name is not correct. correct the build name and reprovision the cfn-stack by 
 running the script file `./bin/cfn/cicd`
 ![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/e56c2c72-ea2c-45fb-9828-80e8f049022d)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/acd541b1-f5bf-432d-9c1f-db2f12548d4e)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/97bc67bd-2e1c-4ba3-95d5-634bc158b84f)
Click on `execute changeset` to pick the new changes into the stack
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/d3a969b4-fa08-4c20-8faf-a25d8f7d632d)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/fecbed0e-c1ad-4626-858f-820f3b01c34f)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/77f3af13-97b0-4c6f-897b-438ce1266ea0)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/563e3e32-93ec-40ea-8a4e-464fdafae88e)
Even after we fix the codebuild name you get with different error 
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/a721a1d9-6790-49bc-bbd5-6bacbb404bbe)
`arn:aws:sts::480134889878:assumed-role/CrdCicd-CodePipelineRole-1EUN4ZKAS1LOP/1684950776474 is not authorized to perform: codebuild:BatchGetBuilds on resource:`
Add the permission `codebuild:BatchGetBuilds` in the cfn cicd change set template.yml and reprovision and see it works this time.
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/d1a70868-8d2c-4f68-a988-315dcd572b02)
click on `release change` to pick the changes to the pipeline
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/f9b48b2c-d4f4-4dd4-ba4c-09a9ec7f4886)
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/291a191b-8075-4f0b-acad-0423aa1af521)
This time it failed with different errors `AccessDenied: Access Denied
 status code: 403, request id: E5SYNTVCV38YJAG5, host id: 9GdB9hXs/yDZU0dZR+L9S8hkfGbcidN5tvT6J80HVXdzeLsAa/1obJpi5SONB/Qzul/fIqJsAS4= for primary source and source version arn:aws:s3:::codepipeline-cruddur-artifacts-m/CrdCicd-Pipeline-QJ7/Source/PyABmmZ`
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/be865c34-025c-41fa-bf84-5bdb702b87b0)
Modify the template.yml of cfn stack and the nested codebuild.yml accordingly to access the artifact bucket and policies to access the bucket 
and reprovision the cfn-stack again by running the script file. Also specify the path of the buildspec.yml file in the backend-flask in the config.toml and  codebuild.yml, template.yml accordingly
Once the changeset is provisioned goto your codepipeline and release the changes and the pipeline will release the changes.
This time it ran successfully.
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/8302393e-a7f6-4cf8-9841-484bf41da24b)

## CFN Diagramming CICD

![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/68f6f1f7-1e1e-4d03-ad3b-b2777344df93)

![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/fa7257b1-d718-4775-8cdf-5b78b4c93c76)

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
![image](https://github.com/madhavi-chavva/aws-bootcamp-cruddur-2023/assets/125069098/aaef0960-dd7b-4f2c-b9d1-92d2b8a32bbb)




  
















































   





 

 

 






       
 
 








`







      




    
