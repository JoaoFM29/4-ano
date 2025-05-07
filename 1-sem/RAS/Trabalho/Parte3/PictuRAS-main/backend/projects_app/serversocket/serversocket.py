import json
from websockets.asyncio.server import serve # type: ignore

class ServerSocket:

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port


    async def start(self):
        async with serve(ServerSocket.on_request, self.host, self.port) as server:
            print(f"WebSocket server started at ws://{self.host}:{self.port}")
            await server.serve_forever()


    async def on_request(websocket):
        async for message in websocket:
            try:
                print(f"Received message from: {message}")
                data = json.loads(message)
                response = {"status": "success", "received": data}
                await websocket.send(json.dumps(response))

            except json.JSONDecodeError:
                print("Received invalid JSON")
                await websocket.send(json.dumps({"error": "Invalid JSON"}))