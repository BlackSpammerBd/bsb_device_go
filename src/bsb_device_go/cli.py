import click
from rich import print
from . import server, client

@click.group()
def bsb(): pass

@bsb.command("start-bsb")
def start():
    """Start server and display code."""
    print("[bold cyan]Starting server...[/]")
    server.start_server()

@bsb.command("c")
@click.argument("code")
def connect(code):
    """Connect to office device with CODE."""
    print(f"[bold cyan]Connecting with code {code}...[/]")
    client.client(int(code))

@bsb.command("stop-it")
def stop():
    """Stop the current session."""
    print("[red]Stopping session...[/]")
    # on client side, closing handled automatically

if __name__ == "__main__":
    bsb()
