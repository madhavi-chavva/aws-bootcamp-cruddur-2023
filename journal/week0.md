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

**Using Budget**.
Using Cloudwatch Alarm. In this case, you need to create an alarm on us-east-1 region (since it is the only region you can create an alarm). You can create up to 10 free cloudwatch alarm
Those 2 alarms will be helpful to identify if you are underspending/overspending.

**Free Tier**
This section will show all the usage of your free tier. It will show all the services free for the 12 months (starting with the registration) and its usage and forcast. After the 12 months, they are still some services are always free. And also there are some service are "Trial" which means that is available for a short period such as 30 days.

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
![architectial diagram](https://user-images.githubusercontent.com/125069098/218807933-4e7e27c5-96e8-4a19-b3d3-2f73ffd36379.png)

or

https://lucid.app/lucidchart/502abf0f-1ba8-421b-aa25-14f8ed82e082/edit?viewport_loc=-655%2C199%2C2368%2C1172%2C0_0&invitationId=inv_c1f3c813-094d-4dc1-b1f5-959b3ceb7b6c

**Napkin design**
![IMG_2926](https://user-images.githubusercontent.com/125069098/218804640-721831a0-bb3a-4a8d-a3c9-db57ff805c6c.JPG)



**Architecture Diagram for CI/CD pipeline**
https://lucid.app/lucidchart/cc550498-caaa-476a-911d-603834a56530/edit?beaconFlowId=09150CAE4C35EED1&invitationId=inv_28046c1a-0399-4971-9bd8-67839edf8516&page=0_0#![image](https://user-images.githubusercontent.com/125069098/218788849-405ea333-2840-4f65-839d-ece44b9b32e8.png)
![test image 2](https://user-images.githubusercontent.com/125069098/218806448-15c099ae-f35c-4331-9364-5fb6bd47e478.png)

**Learned Basic pricing in free tier**
'''
   Gained knowledge on how to grant permissions to the admin user to perfrom billing activies from the root account.
   Steps to perform:
   - Login to the root account -> click on the right corner where your name is shown and select **account** 
   - Scroll where you see IAM User and Role Access to Billing Information, click on edit and enable the **Activate IAM Access**
   - Click on the update button to active this role access.
   - Now go to IAM -> policies -> search for billing and enable the billing permission and click on the **attach policy** and select the user to whom you want to grant the permission.
   - Now Login as IAM user and check the billing service. Now the IAM user has the permission to perform actions related to billing like creating budgets, redeem credits, cost allowcation tags, check the free tier service limits
 '''
