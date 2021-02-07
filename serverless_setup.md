# Tools Installation
## Visual Studio Code
For this project we are going to use Visual Studio Code to do the development work. You can download a copy at: https://code.visualstudio.com/Download

On mac it will download as a zipped file. Double click the zip file in finder and move the resulting .app file into your "Applications" folder.

## Serverless
You can find platform specific installation instructions for serverless in their guide posted at: https://www.serverless.com/framework/docs/getting-started/

Since we are using brew, you can get it with one shot:

```bash
brew install serverless
```

You can test your install by running

```bash
sls --help
```

You should receive the help text listing all the potential serverless commands.

## Development environment
Lets setup a development home for our project. First we create a directory, switch to it and create a virtual python environment.

```bash
mkdir -p development/serverless-kickstart
cd development/serverless-kickstart
pipenv --python 3.8
pipenv shell
```

Your command prompt should change to show you are in the virtual python environment:

```bash
(serverless-kickstart)
```
Now open Visual Studio, choose open folder and navigate to the 'serverless-kickstart' directory and choose open. You should be greated by a welcome screen showing the Pipfile that pipenv created for our project.

### VS python support
If this is a new VSCode install, in the welcome screen choose 'python' from the "Install support for" section to gear up your VSCode for some python work. This will install the default python extension with support for the language, virtual environments, etc.

### Python formatting tools
To make sure our code is of good quality, lets install a couple tools.

Back in your terminal, in your pip environment install pylint and black:

```bash
pipenv install pylint --dev
pipenv install black --dev --pre
```
(Note installing black this way is due to [this issue open at the time of writing](https://github.com/psf/black/issues/822))

Now back in VSCode, click the settings/gear icon at the bottom left, choose settings, type in python.formatting.provider in the search and choose black in the pull down.

Now type in formatOnSave and ensure the option is checked true.

## Serverless plugins
Last step in our setup lets ensure we have the serverless plugins we will need to develop a python lambda function.

The serverless framework supports plugins and there are many, many choices to help you in your development tasks. You can get a list of all supported plugins with

```bash
sls plugin list
```

Before adding plugins we must initialize our project:

```bash
sls
```

will prompt us through creating a new project. Choose AWS python and name your project serverless-kickstart.  You do not need to signup for a serverless account.

For this project we will use the python requirements plugin which will help us package up our lambda function and include whatever libraries we import.

```bash
cd serverless-kickstart
sls plugin install --name serverless-python-requirements
```

Now if you list your files you should see the basic scaffolding that the serverless framework has installed.

```bash
ls -la
handler.py
node_modules
package-lock.json
package.json
serverless.yml
```

The handler.py file is where we will put our python code. The node_modules directory is used by the serverless framework. The package*.json files are where serverless keeps track of what version of it's supporting libraries are in use. Lastly the serverless.yml file is the configuration for our lambda function.

