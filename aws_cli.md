# AWS CLI installation

## Prerequisites
This guide assumes you are on a mac/OSX system.

You’ll need a terminal. I recommend [iterm2](https://iterm2.com/) but terminal.app or any command line shell will do.

You will also need an AWS Access key. You can obtain one for your IAM user account by following [this guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey) or [this video](https://youtu.be/JvtmmS9_tfU)

If this is your first time getting a key, please note you only get one chance to download or record the access key/secret pair. Please store these in your password manager!

## Brew
First step is to install HomeBrew, the missing package manager for OSX. It is widely used to install various software dependencies and will make your life easier! To install it open a terminal shell and execute the following command:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```


## Pipenv
There are many ways to install python virtual environments.
The best way to do python serverless development is to install some isolation tools to separate development python from your OS python environment and avoid dependencies that may interfere with your native version of python, etc.

For this guide we will use the pipenv utility. You can install it using brew via:

```bash
brew install pipenv
```

## AWS CLI
Lets install the aws cli and configure it:

```bash
brew install awscli
aws configure
[You will be prompted for your default region, access key ID and secret access key]
```

If aws is working correctly you should be able to issue a command and receive a response from aws:

```bash
aws sts get-caller-identity
{
    "UserId": "AIDA...5H",
    "Account": "873...20",
    "Arn": "arn:aws:iam::873...20:user/you@youremail.com"
}
```