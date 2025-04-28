import asyncio, secrets, os
from websockets import serve
from rich.console import Console

console = Console()
CLIENTS = {}  # code → websocket

async def handler(ws):
    # Register client
    code = secrets.randbelow(10**6)
    CLIENTS[code] = ws
    console.print(f"[bold green]Your connection code:[/] {code}")
    try:
        async for message in ws:
            cmd, *args = message.split()
            # File list
            if cmd == "LS":
                files = os.listdir(".")
                await ws.send("\n".join(files))
            # Upload
            elif cmd == "UPLOAD":
                fname, data = args[0], ws.binary_data
                with open(fname, "wb") as f: f.write(data)
                await ws.send(f"Uploaded {fname}")
            # Download
            elif cmd == "DOWNLOAD":
                fname = args[0]
                with open(fname, "rb") as f: await ws.send(f.read())
            # Remove
            elif cmd == "REMOVE":
                os.remove(args[0]); await ws.send("Removed")
            # Poll messages (example: files in inbox/)
            elif cmd == "POLL":
                msgs = os.listdir("inbox")
                await ws.send("\n".join(msgs))
    finally:
        del CLIENTS[code]

async def start_server():
    async with serve(handler, "0.0.0.0", 8765):
        console.print("[bold blue]Server running on port 8765[/]")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(start_server())
