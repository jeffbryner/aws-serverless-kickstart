# Your into to serverless python
In this section we will use our aws python/serverless environment to setup a basic python program triggered by the passing of time.

This scheduled program will run in AWS on whatever frequency we determine and simply log it's output and operating environment.

At the end of this section you will have:

 - A functional serverless.yml config file
 - Environment variables used to send runtime options to the function
 - A simple python function
 - A working deployment pipeline to develop locally, execute in AWS, gather logs, etc.


## Serverless.yml init
This file is critical in describing to the serverless framework what you want it to do. It will detail the python program, the name of the service, the AWS services you want to hook into and the permissions of the function.

Serverless has done us a favor and created a sample serverless.yml file, but it is a bit distracting. For the purposes of this tutorial, let us start fresh.

In your serverless-kickstart directory that was created by the serverless framework run:

```bash
> serverless.yml
```

to get us a clean start.

### Serverless.yml configuration
Ultimately we will be making use of the [schedule event for serverless/aws](https://www.serverless.com/framework/docs/providers/aws/events/schedule/).

The docs for all of [serverless for aws can be found here](https://www.serverless.com/framework/docs/providers/aws/).

Under the hood, this scheduled event is provided by AWS cloudwatch and [uses the same syntax as cron on a linux system](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html). We will use this to trigger our python function on a regular basis.

To tell serverless this is what we want, we need to tell it the name of the function, the environment for the function and the AWS service we intend to use to trigger the function.

[The docs for all the serverless.yml options are here.](https://www.serverless.com/framework/docs/providers/aws/guide/serverless.yml/) For this tutorial we will get you off to a good start using some of the most common configuration options.

Edit your serverless.yml file so it looks like this:

```yaml

service: serverless-kickstart
custom:
  pythonRequirements:
    dockerizePip: false

provider:
  name: aws
  runtime: python3.7
  stage: ${opt:stage,'dev'}
  region: us-west-2
  environment:
    ENVIRONMENT: ${self:provider.stage}
    REGION: ${opt:region, self:provider.region}

functions:
  serverless-cron:
    handler: handler.cron
    timeout: 600
    reservedConcurrency: 1
    events:
      - schedule: rate(1 minute)

package:
  exclude:
    - node_modules/**
    - .pytest_cache/**

plugins:
  - serverless-python-requirements

```

The first ```service``` block is just the name of the service. The ```custom``` block is where we can setup variables for use later in the configuration. It is also where we put configuration options for whatever plugins we are using. In this case we are telling the python plugin not to use docker to generate the runtime function. Eventually you will need to use docker to properly deploy your function and this option will be handy, but for now you can leave it as false.

The ```provider``` is where we configure the AWS-specific parameters, like region, etc. The ```environment``` section of this is important since we can use it to pass variables to our serverless function. Here we are passing the region and the ```stage```. Stage is a serverless construct and can be used to separate out development from production so you can do development in the same AWS account as your production environment.

The ```functions``` stanza is where we will setup the lambda functions. There's only one here and includes just enough to link the handler.py file to the cloudwatch trigger to run every minute.

The ```package``` section is useful for limiting the size of your deployment. Under the hood, serverless will zip up your project, deploy it to an S3 bucket and use that deployment as the source for the lambda function. Lambda has size limits, so this stanza give you the opportunity to trim down your function. In this case we are ignoring the serverless runtime itself and any test functions we may create as they aren't used by the resulting python service.

Lastly the ```plugins``` stanza tells the serverless framework which plugins we will be using on deployment.


As a quick sanity check run the print option to see what serverless will use for the various variable settings in our config to make sure it can properly parse the yaml we have created:

```bash
sls print
```

You should see a fully resolved yaml configuraiton with varables like stage, region, etc resolved to their conclusion. If you receive an error from the command, double check your yaml as indentation matters!

# Python
OK, with serverless happy let us move on to setting up a simple python program.

In handler.py, remove any code setup by the serverless init/create and ensure the entire file consists only of:

```python

import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def cron(event, context):
    logger.debug('Event is: {}'.format(event))
    logger.debug('Context is: {}'.format(context))

```

## Testing
You should be able to run this program via

```bash
python handler.py
```
It should complete with no output since we aren't running in AWS, but more importantly it shouldn't produce any errors. If it does, please double check your python code (whitespace matters).

You can also test it within the serverless framework without deploying it to AWS:


```bash
sls invoke local --function serverless-cron
```
You should now see some output showing:


```bash
DEBUG:root:Event is: {}
DEBUG:root:Context is: <__main__.FakeLambdaContext object at 0x1100952e0>

null
```
As we aren't doing very much except echoing out the event and context and we don't have a real event or context, this isn't very exciting but at least shows that we are ready to deploy to AWS.

## Deploying to AWS
To deploy to AWS run:

```bash
sls deploy --stage dev --verbose
```

You should see output similar to the following:

```bash
sls deploy --stage dev --verbose
Serverless: Packaging service...
Serverless: Excluding development dependencies...
Serverless: Injecting required Python packages to package...
Serverless: Creating Stack...
Serverless: Checking Stack create progress...
CloudFormation - CREATE_IN_PROGRESS - AWS::CloudFormation::Stack - serverless-kickstart-dev
CloudFormation - CREATE_IN_PROGRESS - AWS::S3::Bucket - ServerlessDeploymentBucket
CloudFormation - CREATE_IN_PROGRESS - AWS::S3::Bucket - ServerlessDeploymentBucket
CloudFormation - CREATE_COMPLETE - AWS::S3::Bucket - ServerlessDeploymentBucket
CloudFormation - CREATE_COMPLETE - AWS::CloudFormation::Stack - serverless-kickstart-dev
Serverless: Stack create finished...
Serverless: Uploading CloudFormation file to S3...
Serverless: Uploading artifacts...
Serverless: Uploading service serverless-kickstart.zip file to S3 (7.35 KB)...
Serverless: Validating template...
Serverless: Updating Stack...
Serverless: Checking Stack update progress...
CloudFormation - UPDATE_IN_PROGRESS - AWS::CloudFormation::Stack - serverless-kickstart-dev
CloudFormation - CREATE_IN_PROGRESS - AWS::Logs::LogGroup - ServerlessUnderscorecronLogGroup
CloudFormation - CREATE_IN_PROGRESS - AWS::IAM::Role - IamRoleLambdaExecution
CloudFormation - CREATE_IN_PROGRESS - AWS::IAM::Role - IamRoleLambdaExecution
CloudFormation - CREATE_IN_PROGRESS - AWS::Logs::LogGroup - ServerlessUnderscorecronLogGroup
CloudFormation - CREATE_COMPLETE - AWS::Logs::LogGroup - ServerlessUnderscorecronLogGroup
CloudFormation - CREATE_COMPLETE - AWS::IAM::Role - IamRoleLambdaExecution
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Function - ServerlessUnderscorecronLambdaFunction
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Function - ServerlessUnderscorecronLambdaFunction
CloudFormation - CREATE_COMPLETE - AWS::Lambda::Function - ServerlessUnderscorecronLambdaFunction
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Version - ServerlessUnderscorecronLambdaVersion8AFeZWGvONMEIJbXCAvbWEI9IAPtDeJGIzMLIuq1wg
CloudFormation - CREATE_IN_PROGRESS - AWS::Events::Rule - ServerlessUnderscorecronEventsRuleSchedule1
CloudFormation - CREATE_IN_PROGRESS - AWS::Events::Rule - ServerlessUnderscorecronEventsRuleSchedule1
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Version - ServerlessUnderscorecronLambdaVersion8AFeZWGvONMEIJbXCAvbWEI9IAPtDeJGIzMLIuq1wg
CloudFormation - CREATE_COMPLETE - AWS::Lambda::Version - ServerlessUnderscorecronLambdaVersion8AFeZWGvONMEIJbXCAvbWEI9IAPtDeJGIzMLIuq1wg
CloudFormation - CREATE_COMPLETE - AWS::Events::Rule - ServerlessUnderscorecronEventsRuleSchedule1
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Permission - ServerlessUnderscorecronLambdaPermissionEventsRuleSchedule1
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Permission - ServerlessUnderscorecronLambdaPermissionEventsRuleSchedule1
CloudFormation - CREATE_COMPLETE - AWS::Lambda::Permission - ServerlessUnderscorecronLambdaPermissionEventsRuleSchedule1
CloudFormation - UPDATE_COMPLETE_CLEANUP_IN_PROGRESS - AWS::CloudFormation::Stack - serverless-kickstart-dev
CloudFormation - UPDATE_COMPLETE - AWS::CloudFormation::Stack - serverless-kickstart-dev
Serverless: Stack update finished...
Service Information
service: serverless-kickstart
stage: dev
region: us-west-2
stack: serverless-kickstart-dev
resources: 7
api keys:
  None
endpoints:
  None
functions:
  serverless-cron: serverless-kickstart-dev-serverless-cron
layers:
  None

Stack Outputs
ServerlessUnderscorecronLambdaFunctionQualifiedArn: arn:aws:lambda:us-west-2:711111111111:function:serverless-kickstart-dev-serverless-cron:1
ServerlessDeploymentBucketName: serverless-kickstart-dev-serverlessdeploymentbuck-o2x3uiym4i4c

```

This shows the steps serverless is taking to package up your python program, make a deployment s3 bucket, upload the code to s3, create a cloudformation template to deploy the lambda function and deploy the cloudformation template.

You can test invoke the function in AWS as follows:

```bash
sls invoke --function serverless-cron
```

The output may be underwhelming, but the logs should show more context from the last several times the function ran inside AWS:

```bash
sls logs --function serverless-cron
START RequestId: 63ae4069-5a27-4d1e-ac49-0278fef420e3 Version: $LATEST
2021-02-07 12:08:48.609 (-08:00)	63ae4069-5a27-4d1e-ac49-0278fef420e3	[DEBUG]	Event is: {'version': '0', 'id': 'a9a16452-e05e-18fa-d6ea-1bfd82b35339', 'detail-type': 'Scheduled Event', 'source': 'aws.events', 'account': '711111111111', 'time': '2021-02-07T20:08:31Z', 'region': 'us-west-2', 'resources': ['arn:aws:events:us-west-2:711111111111:rule/serverless-kickstart-dev-ServerlessUnderscorecronE-MN4RICOFJKS6'], 'detail': {}}
2021-02-07 12:08:48.610 (-08:00)	63ae4069-5a27-4d1e-ac49-0278fef420e3	[DEBUG]	Context is: <bootstrap.LambdaContext object at 0x7f5e901144d0>
END RequestId: 63ae4069-5a27-4d1e-ac49-0278fef420e3
REPORT RequestId: 63ae4069-5a27-4d1e-ac49-0278fef420e3	Duration: 1.50 ms	Billed Duration: 2 ms	Memory Size: 1024 MB	Max Memory Used: 51 MB
```

You can see our function is working as intended, passing along the event and context that it is receiving from AWS!

You can also visit your new function in the AWS console, by logging into your account and going to the lambda service in the us-west-2 region. It should be named "serverless-kickstart-dev-serverless-cron" which is the name of our project plus the stage plus the name of the function.

You should also now see a .serverless directory where the framework generated all the artifacts it deployed to AWS including the zip file of the function and the cloud formation template.

## Removing from AWS
The cloud is meant to be ephemeral, so it's always a good idea to know how to destroy anything you deploy when you no longer need it.

To destroy our function:

```bash
sls remove --stage dev --verbose
Serverless: Getting all objects in S3 bucket...
Serverless: Removing objects in S3 bucket...
Serverless: Removing Stack...
Serverless: Checking Stack removal progress...
CloudFormation - DELETE_IN_PROGRESS - AWS::CloudFormation::Stack - serverless-kickstart-dev
CloudFormation - DELETE_IN_PROGRESS - AWS::Lambda::Permission - ServerlessUnderscorecronLambdaPermissionEventsRuleSchedule1
CloudFormation - DELETE_SKIPPED - AWS::Lambda::Version - ServerlessUnderscorecronLambdaVersion8AFeZWGvONMEIJbXCAvbWEI9IAPtDeJGIzMLIuq1wg
CloudFormation - DELETE_COMPLETE - AWS::Lambda::Permission - ServerlessUnderscorecronLambdaPermissionEventsRuleSchedule1
CloudFormation - DELETE_IN_PROGRESS - AWS::Events::Rule - ServerlessUnderscorecronEventsRuleSchedule1
CloudFormation - DELETE_COMPLETE - AWS::Events::Rule - ServerlessUnderscorecronEventsRuleSchedule1
CloudFormation - DELETE_IN_PROGRESS - AWS::Lambda::Function - ServerlessUnderscorecronLambdaFunction
CloudFormation - DELETE_COMPLETE - AWS::Lambda::Function - ServerlessUnderscorecronLambdaFunction
CloudFormation - DELETE_IN_PROGRESS - AWS::Logs::LogGroup - ServerlessUnderscorecronLogGroup
CloudFormation - DELETE_IN_PROGRESS - AWS::S3::Bucket - ServerlessDeploymentBucket
CloudFormation - DELETE_IN_PROGRESS - AWS::IAM::Role - IamRoleLambdaExecution
CloudFormation - DELETE_COMPLETE - AWS::S3::Bucket - ServerlessDeploymentBucket
CloudFormation - DELETE_COMPLETE - AWS::Logs::LogGroup - ServerlessUnderscorecronLogGroup
Serverless: Stack removal finished...
```