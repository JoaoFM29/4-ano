import os
import asyncio
from dotenv import load_dotenv # type: ignore
import websockets  # type: ignore


class WebSocketGateway:

    def __init__(self, host: str, port: int, forward_host: str, forward_port: int) -> None:
        self.host = host
        self.port = port
        self.forward_url = f"ws://{forward_host}:{forward_port}"


    async def start(self):
        async with websockets.serve(self.handle_connection, self.host, self.port) as server:
            print(f"WebSocket Gateway started at ws://{self.host}:{self.port}")
            await server.serve_forever()


    async def handle_connection(self, client_websocket):

        try:
            async with websockets.connect(self.forward_url) as server_websocket:    
                client_to_server = self.forward_messages(client_websocket, server_websocket, "Client -> Server")
                server_to_client = self.forward_messages(server_websocket, client_websocket, "Server -> Client")
                await asyncio.gather(client_to_server, server_to_client)

        except Exception as e:
            print(f"Error handling connection: {e}")
            await client_websocket.close()


    async def forward_messages(self, source, destination, direction):

        try:
            async for message in source:
                print(f"Forwarding message ({direction}): {message}")
                await destination.send(message)

        except websockets.ConnectionClosed as e:
            print(f"Connection closed ({direction}): {e}")

        finally:
            await source.close()
            await destination.close() 
            print(f"Connection closed ({direction})")


if __name__ == "__main__":

    load_dotenv()

    WS_GATEWAY_WS_HOST = os.getenv('WS_GATEWAY_WS_HOST', '0.0.0.0')
    WS_GATEWAY_WS_PORT = int(os.getenv('WS_GATEWAY_WS_PORT', 8764))

    PROJECTS_WS_HOST = os.getenv('PROJECTS_WS_HOST', 'localhost')
    PROJECTS_WS_PORT = int(os.getenv('PROJECTS_WS_PORT', 8765))

    gateway = WebSocketGateway(WS_GATEWAY_WS_HOST, WS_GATEWAY_WS_PORT, PROJECTS_WS_HOST, PROJECTS_WS_PORT)
    asyncio.run(gateway.start())