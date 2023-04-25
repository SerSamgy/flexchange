# flexchange

This project was generated using [fastapi_template](https://github.com/s3rius/FastAPI-template).

## Poetry

This project uses poetry. It's a modern dependency management tool.

To run the project use this set of commands:

```bash
poetry install
poetry run python -m flexchange
```

This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.

You can read more about poetry [here](https://python-poetry.org/)

## Docker

You can start the project with docker using this command:

```bash
docker-compose -f docker-compose.yml . up --build
```

If you want to develop in docker with autoreload add `-f docker-compose.dev.yml` to your docker command.
Like this:

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml . up
```

This command exposes the web application on port 8000, mounts current directory and enables autoreload.

But you have to rebuild image every time you modify `poetry.lock` or `pyproject.toml` with this command:

```bash
docker-compose -f docker-compose.yml . build
```

## Project structure

```bash
$ tree "flexchange"
flexchange
├── conftest.py  # Fixtures for all tests.
├── db  # module contains db configurations
│   ├── dao  # Data Access Objects. Contains different classes to interact with database.
│   └── models  # Package contains different models for ORMs.
├── __main__.py  # Startup script. Starts uvicorn.
├── services  # Package for different external services such as rabbit or redis etc.
├── security.py  # Authorization related functions.
├── settings.py  # Main configuration settings for project.
├── static  # Static content.
├── templates  # HTML templates.
└── web  # Package contains web server. Handlers, startup config.
    ├── api  # Package with all handlers.
    │   ├── dependencies.py  # Dependencies for endpoints.
    │   └── router.py  # Main router.
    ├── application.py  # FastAPI application configuration.
    └── lifetime.py  # Contains actions to perform on startup and shutdown.
    └── templates.py  # Templates loader.
```

## Configuration

This application can be configured with environment variables.

Create `.env` file from `.env.default` in the root directory
and place all environment variables here.

All environment variables should start with "FLEXCHANGE_" prefix.

For example if you see in your "flexchange/settings.py" a variable named like
`random_parameter`, you should provide the "FLEXCHANGE_RANDOM_PARAMETER"
variable to configure the value. This behaviour can be changed by overriding `env_prefix` property
in `flexchange.settings.Settings.Config`.

An example of .env file:
```bash
FLEXCHANGE_RELOAD="True"
FLEXCHANGE_PORT="8000"
FLEXCHANGE_ENVIRONMENT="dev"
```

You can read more about BaseSettings class here: https://pydantic-docs.helpmanual.io/usage/settings/

## Authorization
To access `/reports` (as trader) and `/trades` (as superuser) endpoints a user must exist and
be authorized. For simplicity there is a SQL script `initial_data.sql` in root of project folder
that inserts a default data to DB. It creates 3 users: one superuser `gendo.ikari@nerv.jp` and
2 traders `shinji.ikari@nerv.jp` and `asuka.langley.soryu@nerv.de`. They all have the same
password: `gendowned`.

To load data from the script the `flexchange` web server must be running and a `sqlite3`
package must be installed. Locally with an appropriate package manager or in container with:

```bash
apt-get update
apt-get install sqlite3
```

To run script:

```bash
sqlite3 $FLEXCHANGE_DB_FILE -init initial_data.sql
```

## Pre-commit

To install pre-commit simply run inside the shell:
```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default it runs:
* black (formats your code);
* ruff (fixes some bugs, sorts imports in all files);


You can read more about pre-commit here: https://pre-commit.com/


## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose -f docker-compose.yml . run --rm api pytest -vv .
docker-compose -f docker-compose.yml . down
```

For running tests on your local machine.

```bash
pytest -vv .
```
