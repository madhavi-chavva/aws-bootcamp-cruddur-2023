**Pre-requisites for the Free AWS Bootcamp Project**

You will need to register to the following services:

- Create a Github Account. You will copy Andrew's repository with the right formatting of the repo and must be public.
- Create a Gitpod account and install the extention for your browser.
- Create Github CodeSpace.
- Create the AWS account (This is the important one as you will spin all the service here). Make sure you have a credit/debit card ready.
- Create Lucidchart. This app allows you to create chart/diagram. Having a visual structure are really useful to see the overview of what are you creating.
- Create Honeycomb.io account.
- Create Rollbar account.


# Week 0 — Billing and Architecture
In this section, we will be discussing the billing dashboard and all its component such as Cost Explorer, Billing Alerts, Tags, AWS calculator etc.

**Billing Alerts**
There are 2 ways to set the billing alerts.

![image](https://user-images.githubusercontent.com/125069098/218822748-70c7bde9-e036-42e9-9e9d-e8e5c3fcf566.png)


**Using Budget**.
Using Cloudwatch Alarm. In this case, you need to create an alarm on us-east-1 region (since it is the only region you can create an alarm). You can create up to 10 free cloudwatch alarm
Those 2 alarms will be helpful to identify if you are underspending/overspending.

![image](https://user-images.githubusercontent.com/125069098/218820054-7a9d85d8-1424-4032-a62f-29a60d86c5cb.png)

![image](https://user-images.githubusercontent.com/125069098/218833465-a5b249bc-ee6c-4724-95f2-8e3110296a3d.png)

**Free Tier**
This section will show all the usage of your free tier. It will show all the services free for the 12 months (starting with the registration) and its usage and forcast. After the 12 months, they are still some services are always free. And also there are some service are "Trial" which means that is available for a short period such as 30 days.

 **Billing preferences**
 ![billing preferences](https://user-images.githubusercontent.com/125069098/218819172-20b0e28a-7595-404b-a436-b189a59a7290.png)
 
 **Redeem Credits**
![image](https://user-images.githubusercontent.com/125069098/218821254-f318e889-9669-48a4-94ee-114faa157059.png)


**Tags**
Tags (are Key/Value pair) are useful when you want to know how your cost is allocated. For example if your want to identify all the services you used under the tag enviromenrt: dev (for example)

Cost Explorer
Cost explorer is a service which visualise, understand and manage your AWS costs usage over time.

Report
The section report allows to generate reports. there are some reports already created by AWS that you can use

Credit
This is the section when you submit your credit that you have obtain during an event (for example after submitting a feedback questionnaires). And also it shows when the expiration date.

AWS Calculator
This is a tool where you want to estimate the cost of one or more services. Useful when someone asks you to give an estimate cost of the service you are going to use. I used this tool in several learning plan during the Skillbuilder. https://calculator.aws/#/

**Architecture Diagram**
Requirements
Application using micro services
The frontend is in JS and the backend is in Python
Using api to communicate
Authetnication using Cognito
Use as much as possible the aws free tier
Momento as a third party caching system

**Cruddur logical diagram**
![architectial diagram](https://user-images.githubusercontent.com/125069098/219069732-712f0c43-269a-44a3-952a-6a7ba6117fef.png)

or

https://lucid.app/lucidchart/502abf0f-1ba8-421b-aa25-14f8ed82e082/edit?viewport_loc=-655%2C199%2C2368%2C1172%2C0_0&invitationId=inv_c1f3c813-094d-4dc1-b1f5-959b3ceb7b6c

**Napkin design**
![IMG_2926](https://user-images.githubusercontent.com/125069098/218804640-721831a0-bb3a-4a8d-a3c9-db57ff805c6c.JPG)



**Architecture Diagram for CI/CD pipeline**
https://lucid.app/lucidchart/cc550498-caaa-476a-911d-603834a56530/edit?beaconFlowId=09150CAE4C35EED1&invitationId=inv_28046c1a-0399-4971-9bd8-67839edf8516&page=0_0#![image](https://user-images.githubusercontent.com/125069098/218788849-405ea333-2840-4f65-839d-ece44b9b32e8.png)
![test image 2](https://user-images.githubusercontent.com/125069098/218806448-15c099ae-f35c-4331-9364-5fb6bd47e478.png)

**IAM User and Role Access to Billing Information**
'''
   Gained knowledge on how to grant permissions to the admin user to perfrom billing activies from the root account.
   Steps to perform:
   - Login to the root account -> click on the right corner where your name is shown and select **account** 
   - Scroll where you see IAM User and Role Access to Billing Information, click on edit and enable the **Activate IAM Access**
   - Click on the update button to active this role access.
   - Now go to IAM -> policies -> search for billing and enable the billing permission and click on the **attach policy** and select the user to whom you want to grant the permission.
   - Now Login as IAM user and check the billing service. Now the IAM user has the permission to perform actions related to billing like creating budgets, redeem credits, cost allowcation tags, check the free tier service limits

**MFA for the IAM user**
![mfa iam user](https://user-images.githubusercontent.com/125069098/218841164-414559e2-71a8-482f-b4d3-07718e2fff89.png)

**AWS CLI install in gitpod**
![aws cli](https://user-images.githubusercontent.com/125069098/218868841-d55d12ef-af87-4752-81b5-3baea711c602.png)

**AWS CLI with --cli-auto-prompt**
![gitpod aws cli](https://user-images.githubusercontent.com/125069098/218918357-1968dac6-7d5b-4450-9115-d3b9a2af43ed.png)

**To obtain Account-ID using gitpod aws cli**
![image](https://user-images.githubusercontent.com/125069098/219112362-0d9a3677-dfdd-4a71-96ec-f6dc71e4b4e3.png)

**Screenshot for the budget creation using aws-cli github**
![budget aws cli](https://user-images.githubusercontent.com/125069098/219121308-5203209c-e779-40c8-ad39-13aa882b267b.png)
 
 **create SNS Topic and Subscription using aws-cli**
 ![sns](https://user-images.githubusercontent.com/125069098/219130065-66bf8f89-d07d-473a-be23-5a9f4ecf3484.png)
 
 **screenshot from AWS
 ![image](https://user-images.githubusercontent.com/125069098/219130439-af0a373e-78ed-4d1a-b78b-de71f3eed01b.png)
 
 **subscription**
 ![image](https://user-images.githubusercontent.com/125069098/219130846-2be61615-9235-402a-af93-224e8a3241a8.png)
 
 **screenshot for alarm**
 ![image](https://user-images.githubusercontent.com/125069098/219135374-5976d1c0-aaeb-4643-83a6-be9ce80adc22.png)
 
 #### SECURITY
 The important thing when it comes to security. Always inform the business of the technical risk that can exist of open vulnerabilities that have not been resolved and can potentially affect the business and how will be solved.

#### Definition of the cloud security
Cybersecurity protects data, applications and services associated with cloud environments from both external and internal security threats.

### Why care about cloud security
- Reducing the impact of the breach
- Protecting all the system (application, network etc) against malicious data theft
- Reducing the human error responsible for data leaks
#### Cloud Security requires practice
- Understand the complexity of the system
- Always keep updated with the new services announced
- Bad hackers are improving as well.

#### MFA for root account
-Root user is the most powerful user in aws environment. I consider it the key to your kingdom. Once it is compromised, hackers can spin any services on your AWS account (for example creating a bitcoin mining) Enable the MFA for the root account gives you an extra layer of security. Could be virtual or physical.

#### AWS Organization
Create an organization unit (AWS Organization) AWS Organization allows you to create and manage multiple account. Also it allows to apply governance policies to accounts or group. There are 2 approce to create the organization:

- Creating business unit (HR Ou, Finance Ou, Engineering Ou)
- Creating a Standby and Active Pool.

SCP (Service Control Policy) are a type of organisational policy that you can use to manage permission in your organisation.

#### AWS Cloud Trail
Auditing Service in AWS. Most all the api will be recorded in this service. Cloudtrail will record only the activity in the region you will operate. This service is not free

#### IAM
Ability to access using user and password 3 kinds of users:

- IAM user with user and password (make sure MFA is active as well as you activated on root account)
- Federated user are users federated from an on-premise environment without a password
- Web Token User

Always Give the least privilege to the users. Don't give more than what it is necessary.

When you are working on AWS, it is a best practice to use the IAM user instead of the Root account. If for some reason the IAM user is compromised, it is simple to solve the problem by removing the policy attached to it/deleting the user himself.

Policies are assigned to either an IAM user or IAM role or IAM group and consist of what the entity can/can not do. For example, a policy could be the possibility to read the content of the s3 bucket.

Access Key and Secret Access key are similar to the user and password (keep it always secret). One reason you need to use it is for example you need to do some calls using CLI. Never hardcode this information on services that it is public expose (for example code on github with access key and secret access key) as bad actors could reuse those access to do bad actions (exploit your application and get sensible information or spin services)In some cases you need to use an IAM Role and attach it to a service or even a user. the difference between Iam user and Iam role is once the entity assumes the IAM role, it is valid for a short time and temporarily loses the previous privilege.

Make sure to create the IAM role as simply as possible.

#### Share Responsibility
This diagram shows what is the responsibility of the customer and what is the responsibility of AWS. For example, AWS is responsible for the global infrastructure. they care about everything work accordingly and are secure. Meanwhile, the customer is responsible for the application, eventually configuration (NACL/SG), and encryption at rest and in transit.
![shared responsibility](https://user-images.githubusercontent.com/125069098/219216125-e1ccce0e-63cc-4647-a0f8-43da3c5c398a.png)
 
### AWS CLI

There are 2 types to access aws via CLI.
One is installing the aws CLi from you terminal and after providing the secret key and secret access key and the region where you will call the api.

Another way is to use cloudshell from your the aws console.
Note that not all the region are available for this functionality. Please check the icon close to the name of you IAM User.
 
A  trick that I learnt from Bootcamp is to activate the auto prompt. This helped me a lot to complete the command that i wanted to launch and give you an overview of the command all on the terminal.

aws --cli-auto-prompt
if you want to put the pipe sign just type the following command "alt+124"


