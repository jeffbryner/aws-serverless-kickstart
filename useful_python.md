# Useful python
Now that we have a framework to create a serverless function that runs whenever we want, lets add some common elements that make this pattern useful.

Most functions end up being a combination of:

- retrieving a configuration (environment variables)
- retrieving a secret (usually an api key or username/password)
- using the secret to call a web api
- doing something with the data

The following sections will walk through some sample code to use this pattern to:
- get a configuration for an apikey name
- retrieve the apikey from aws secret manager
- use the secret to call a web api
- log the result

## Configuration
Good code avoids hardcoding things like URLs, filenames, etc. Usually this is done through a configuration file or command line options. In a serverless environment we want to avoid physical things like files or user input as much as possible, so we will use environment variables to set and get our configuration.

### Python
The python code to get a value from an environment variable is simple:

```python
import os

config_value = os.environ.get('variable_name','default_value')
```

For our python code we'll get the name of the api key we are going to use. Ensure your handler.py looks like this:

```python
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

API_KEY_NAME = os.environ.get("API_KEY_NAME", "api_key")

def cron(event, context):
    logger.debug("Event is: {}".format(event))
    logger.debug("Context is: {}".format(context))
    logger.debug("API Key name is: {}".format(API_KEY_NAME))

```

This will prompt the function to retrieve the api key name on startup and log it to debug output when we run.


### Serverless
In the serverless framework we can set the value for an environment variable by specifying it in the serverless.yml config file

```yaml
environment:
  VARIABLE_NAME: 'value'
```

For our project ensure the 'provider' section of your serverless.yml file looks like this:

```yaml
provider:
  name: aws
  runtime: python3.7
  stage: ${opt:stage,'dev'}
  region: us-west-2
  environment:
    ENVIRONMENT: ${self:provider.stage}
    REGION: ${opt:region, self:provider.region}
    API_KEY_NAME: 'kickstart_api_key'
```

If you like you can deploy this version and test the output using the same pattern as earlier to deploy and print the logs. If it is working correctly you should see 'kickstart_api_key' logged as the value of the api key name:


```
2021-02-14 11:49:26.318 (-08:00)	3be5e694-97c6-43cd-ae8d-1bc8fa1c956c	[DEBUG]	API Key name is: kickstart_api_key
```


## Secrets
Good code doesn't store secrets insecurely. AWS has a service just for this called secrets manager! Here's how we use it in our serverless function.

### AWS
To store a secret in [AWS secrets manager](https://docs.aws.amazon.com/cli/latest/reference/secretsmanager/create-secret.html#examples):

```bash
aws secretsmanager create-secret --name kickstart_api_key --description "kickstart tutorial api key" --secret-string "apikeygoeshere"
```

You should receive output like this:
```bash
{
    "ARN": "arn:aws:secretsmanager:us-west-2:0123456789012:secret:kickstart_api_key-3aiKqB",
    "Name": "kickstart_api_key",
    "VersionId": "e0dab410-fe1c-4124-b58c-dbbf49c8eb90"
}
```
You can see that AWS has generated an [Amazon Resource Name (ARN)](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html) for our secret, along with the friendly name we gave for it and a version.

To retrieve your secret from the command line:

```bash
aws secretsmanager get-secret-value  --secret-id  kickstart_api_key
```

You should receive output like this:

```bash
{
    "ARN": "arn:aws:secretsmanager:us-west-2:0123456789012:secret:kickstart_api_key-3aiKqB",
    "Name": "kickstart_api_key",
    "VersionId": "e0dab410-fe1c-4124-b58c-dbbf49c8eb90",
    "SecretString": "apikeygoeshere",
    "VersionStages": [
        "AWSCURRENT"
    ],
    "CreatedDate": "2021-02-14T12:28:22.422000-08:00"
}
```

To update/change an existing secret:
```bash
aws secretsmanager update-secret --secret-id kickstart_api_key --secret-string "newapikeygoeshere"
```

### Python
Now that we have a sample secret stored, lets hook it up to our python function.

First we will need to add the [boto](https://pypi.org/project/boto3/) library so we can hook into AWS services.

```bash
pipenv install boto3
```

Now alter your handler.py function to include the following statements:

```python
import boto3  # put this in your include section at the top


# put these just after your API_KEY_NAME config retrieval
boto_session = boto3.session.Session()
secrets_manager = boto_session.client("secretsmanager")
API_KEY = secrets_manager.get_secret_value(SecretId=API_KEY_NAME)["SecretString"]


#lastly, add this to your debug statements (properly indented)
logger.debug("API Key is: {}".format(API_KEY))

```

Lastly we will need to update our serverless deployment to let AWS know the function will need access to the secret we have created.

In your serverless.yml file add the following to the provider stanza:


```yaml

  iamRoleStatements:
    - Effect: Allow
      Action:
        - secretsmanager:GetSecretValue
      Resource:
        - "arn:aws:secretsmanager:${opt:region, self:provider.region}:*:secret:${self:provider.environment.API_KEY_NAME}*"

```
This allows our function to get the secret value for the ARN associated with our secret. You'll notice we are pulling portions of the ARN from variables within the serverless.yml file, and ending with they API_KEY_NAME* to allow for the unique random bit aws appends to the end ( kickstart_api_key-3aiKqB in this case ).

