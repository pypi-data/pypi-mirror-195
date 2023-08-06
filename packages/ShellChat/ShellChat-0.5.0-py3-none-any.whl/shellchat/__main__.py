
import click

from .server.server import ShellServer
from .client.client import ShellClient


@click.group()
def main():
    pass


@main.command()
@click.option('--host', default='localhost', help='Host to bind to')
@click.option('--port', default=8000, help='Port to bind to')
def create(host, port):
    print(f"Starting server on {host}:{port}")
    ShellServer(host, port).run()


@main.command()
@click.option('--host', default='localhost', help='Host to bind to')
@click.option('--port', default=8000, help='Port to bind to')
@click.option('--username', default='anonymous', help='Username to use')
def connect(host, port, username):
    print(f"Connecting to {host}:{port}")
    ShellClient(username, host, port).run()


if __name__ == '__main__':
    main()
