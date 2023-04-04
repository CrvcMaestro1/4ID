import os
import subprocess
from typing import Union

import click
from dotenv import load_dotenv


def check_uri() -> bool:
    db_uri_check = os.getenv("DATABASE_APPLICATION")
    return db_uri_check is not None


def check_mandatory_env_variables():
    mandatory_env_variables = ["DATABASE_APPLICATION", "DATABASES_REPLICA_POOL"]
    for env in mandatory_env_variables:
        if os.getenv(env) is None:
            raise Exception(f'`{env}` environment variable is not set')


def load_env(env: str) -> None:
    dotenv_file = '.env'
    if env != 'local':
        dotenv_file = f'.env.{env}'
    load_dotenv(dotenv_file)
    check_mandatory_env_variables()


def validate_env(_context: click.Context, _parameter: Union[click.Option, click.Parameter],
                 env: str) -> str:
    values = ('local', 'test', 'dev', 'stg', 'prod')
    if env not in values:
        raise click.BadParameter(f'`env` must be one of: {values}')
    if not check_uri():
        load_env(env)
    return env


@click.group('App server CLI')
def cli() -> None:
    pass


@cli.command(help='Run the web server')
@click.argument('env', envvar='ENV', default='local', callback=validate_env)
@click.option('--host', '-h', default='0.0.0.0')
@click.option('--port', '-p', default='8080')
def server(env: str, host: str, port: str) -> int:
    try:
        load_env(env)
        subprocess.check_call(['python', 'manage.py', 'check', 'style'])
        subprocess.check_call(['python', 'manage.py', 'check', 'types'])
        subprocess.check_call(['python', 'manage.py', 'check', 'tests'])
        return subprocess.call(['uvicorn', 'src.application:app', '--host', host, '--port', port, '--reload'])
    except subprocess.CalledProcessError as cpe:
        raise Exception(str(cpe))


@cli.command(help='Run the production web server')
@click.argument('env', envvar='ENV', default='local', callback=validate_env)
@click.option('--host', '-h', default='0.0.0.0')
@click.option('--port', '-p', default='8080')
def prod(env: str, host: str, port: str) -> int:
    try:
        load_env(env)
        return subprocess.call(['uvicorn', 'src.application:app', '--host', host, '--port', port])
    except subprocess.CalledProcessError as cpe:
        raise Exception(str(cpe))


@cli.group(help="Manage the database")
def db() -> None:
    pass


@db.command(help="Make the database migrations")
@click.argument('env', envvar='ENV', default='local', callback=validate_env)
@click.option('--message', '-m')
def makemigrations(env: str, message: str) -> int:
    try:
        click.echo(f'Making migrations with message `{message}`...')
        load_env(env)
        return subprocess.call(['alembic', 'revision', '--autogenerate', '-m', message])
    except subprocess.CalledProcessError as cpe:
        raise Exception(str(cpe))


@db.command(help="Run the database migrations")
@click.argument('env', envvar='ENV', default='local', callback=validate_env)
def migrate(env: str) -> int:
    try:
        click.echo(f'Running migrations for database...')
        load_env(env)
        return subprocess.call(['alembic', 'upgrade', 'head'])
    except subprocess.CalledProcessError as cpe:
        raise Exception(str(cpe))


@cli.group(help='Run the code quality tools')
def check() -> None:
    pass


@check.command(help='Run the linter')
def style() -> int:
    try:
        click.echo('Running `flake8`...')
        return subprocess.check_call(['flake8', '--count'])
    except subprocess.CalledProcessError as cpe:
        raise Exception(str(cpe))


@check.command(help='Run the test suite, add --watch to keep running')
@click.argument('env', envvar='ENV', default='local', callback=validate_env)
@click.option('--watch', '-w', is_flag=True, help='to keep running')
def tests(watch: bool, env: str) -> int:
    try:
        load_env(env)
        click.echo('Running `pytest`...')
        if watch:
            return subprocess.check_call('ptw')
        return subprocess.check_call('pytest')
    except subprocess.CalledProcessError as cpe:
        raise Exception(str(cpe))


@check.command(help='Run the static analyzer')
def types() -> int:
    try:
        click.echo('Running `mypy`...')
        return subprocess.check_call(['mypy', '--show-error-code'])
    except subprocess.CalledProcessError as cpe:
        raise Exception(str(cpe))


if __name__ == "__main__":
    cli()
