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

CFN_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/cluster/template.yaml"
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









 
 





      




    
