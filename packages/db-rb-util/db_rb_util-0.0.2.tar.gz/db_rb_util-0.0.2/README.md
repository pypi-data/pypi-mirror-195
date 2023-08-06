# DB-RB-Util

DB-RB-Util provides common database utility functions for use in the receipt matching and dictionary generation systems.

This is a global package used to support database connection methods for different countries.</br>

## Table of Content
1. [Getting started](#getting-started)
2. [SonarQube](#sonar-qube)
3. [Precommit Hooks](#precommit-hooks)
4. [Contributing to the project](#contribution)

## Getting Started <a name="getting-started"></a>

Use the following steps to make sure your code follows the project's coding and formatting standards.
#### <u>**Preparation**</u>

Before running any of the commands in this section ensure you're in the new project directory where the Makefile is located.

```bash
> cd <path-to-your-workspace>/db-rb-util
```

and that all virtual environments are deactivated.

```bash
> deactivate
```


#### <u>**Set up project using the make commands**</u>
Open the Makefile, if you want to know what each make command is doing.

To get an overview of all available make commands run
```bash
> make help
```

1. **Creating your project development environment**

   To create a development environment for your project run the command below.

   ```bash
   > make environment-dev
   ```

   This will create a **virtual environment** for you called `.venv` in your project directory. It will 
 also install all the **requirements** from requirements-dev.txt and requirements.txt. And finally it will install the **pre-commit hook** settings.


2. **Activate the environment**

   ```bash
   > . .venv/bin/activate
   (.venv) >
   ```

   You should see the `(.venv)` text before your prompt to show you have activated the environment.

3. **Run tests**

   Now try to run the project unit tests which requires the environment to be activated:

   ```bash
   (.venv) > make test
   ```

   You should see a code coverage report in the terminal. Additionally, the report is saved to the `coverage-reports` folder where it will be picked up by the sonarqube runner.

## Pre-commit hooks <a name="precommit-hooks"></a>

This project uses pre-commit hooks. These are scripts that are run before you make a commit to run various tasks.
 * In the project the pre-commit hooks are installed using a python library called `pre-commit`.
 * The configuration of the pre-commit hooks is in the `.pre-commit-config.yaml` file.

Here's some guidance on getting started with these.

### Summary of Hooks from the Docs

> Git hook scripts are useful for identifying simple issues before submission to code review.
> We run our hooks on every commit to automatically point out issues in code such as missing semicolons,
> trailing whitespace, and debug statements. By pointing these issues out before code review,
> this allows a code reviewer to focus on the architecture of a change while not wasting
> time with trivial style nitpicks.

To summarise pre-commit hooks briefly, these run automated tasks which are helpful for improving your code quality. For example, `isort` will sort your imports so that you and your fellow developers specify these in exactly the same order.

We have implemented the pre-commit hooks in such a way that they are run consistently in your local repo and on the CI pipeline.

### Using Pre-commit in the Project
To adopt `pre-commit` into our project we simply perform the following actions:

- Make sure you have run the `make environment-dev` task which will install the `pre-commit` library and then install pre-commit hooks for you in your local repo (it runs the `pre-commit install` command for you)
- The `.pre-commit-config.yaml` for this project includes `isort`, `black`, `flake8` and `mypy`.

> If you amend the hooks you will need to rerun the `pre-commit install` command.

The project requires you to use pre-commit hooks in two ways:

1. Your commits will be checked by pre-commit hooks running *before each commit*. They might require you to make changes before you can commit.
2. Run the `make format` task to run apply `isort` and `black`
3. Run `check-format` to check if all pre-commit hooks will pass
4. run `ci-check` to run include tests. This will make sure that your CI pipeline will not fail.

By default `pre-commit` will only run on the *staged files* during git hooks. 
However, if you want to run pre-commit on all files then do
```bash
(.venv) > pre-commit run --all-files
```

You can see if you have pre-commit hooks installed in your local repo by checking to see if you have the `.git/hooks/pre-commit` script. This is what's installed by the python `pre-commit` library.

## Sonarqube <a name="sonar-qube"></a>

Sonarqube is a static analysis tool. In the template the `sonar-scanner` tool is run across your code and the results of the scan are sent to the GfK Sonarqube server. This means you can then login to the server and see lots of interesting metrics and information about your code including:
 * Coverage
 * Complexity
 * Issues
 * Maintainability

The template is configured to run analysis of your python code via Sonarqube. A `cobertura` style coverage report is generated when you run the `make test` command. This is analysed by the `sonar-scanner` which is how Sonarqube is able to tell you your test coverage if you have followed the steps below to set up your project with Sonarqube.

### Accessing Sonarqube

To access the Sonarqube UI:
* Link to this project on Sonarqube [https://sonarqube.gfk.com/dashboard?id=RMS-JSON-Interface](https://sonarqube.gfk.com/dashboard?id=DB-RB-Util) 
* Everyone should be able login with their AD credentials immediately, no ticket or request required

## Contributing to the project <a name="contribution"></a>
### Pushing your Changes
Create a merge request so you can merge your changes to the `develop` branch.
This will automatically publish a new package version to the [GitLab Package Registry](https://gitlab.td.gfk.com/consumer-voice/common_modules/DB-RB-Util/-/packages)

<mark>You cannot publish a package if a package of the same name and version already exists. You must delete the existing package first. If you attempt to publish the same package more than once, a 400 Bad Request error occurs.</mark>

### Import as package to other repositories
Create a personal access token in your gitlab account. The token only needs `read_api` rights.
</br> Set the environment variable <${GITLAB_PIP_TOKEN}> with personal token value.
```bash
(.venv) > export GITLAB_PIP_TOKEN=<your-personal-access-token>
```
   
In the requirements.txt we use `--extra-index-url` to download and install the package from the gitlab package registry.

   `--extra-index-url https://__token__:${GITLAB_PIP_TOKEN}@gitlab.td.gfk.com/api/v4/projects/2099/packages/pypi/simple`
   
   `db-rb-util==<required_version>`

   Now you can import the package in other repositories just like any other library
   ```json
   (.venv) > from db-rb-util import ...
   ```

   You should see a log report in the terminal. Additionally, in case of error you should see the log trace.
