import asyncio, sys
from websockets import connect
from rich.console import Console

console = Console()

async def client(code):
    uri = f"ws://<office_ip>:8765"
    async with connect(uri) as ws:
        await ws.send(f"CONNECT {code}")
        console.print("[green]Connected![/]")
        while True:
            cmd = console.input("bsb> ")
            if cmd in ("stop","exit"):
                await ws.close(); break
            await ws.send(cmd.upper())
            resp = await ws.recv()
            console.print(resp)

if __name__ == "__main__":
    code = sys.argv[1]
    asyncio.run(client(code))
