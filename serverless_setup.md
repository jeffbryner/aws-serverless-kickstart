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

