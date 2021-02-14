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
