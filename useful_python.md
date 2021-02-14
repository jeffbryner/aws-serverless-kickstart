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

### Serverless
In the serverless framework we can set the value for an environment variable by specifying it in the serverless.yml config file

```yaml
provider:
  name: aws
  runtime: python3.7
  stage: ${opt:stage,'dev'}
  region: us-west-2
  environment:
    VARIABLE_NAME: 'value'
```


