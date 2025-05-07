import os
import json
import asyncio
import traceback
from dotenv import load_dotenv # type: ignore
from websockets.asyncio.server import serve # type: ignore
from processor.processor import Processor
from processor.tracer import Tracer

tracer = Tracer()


class ServerSocket:

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port


    async def start(self) -> None:
        async with serve(ServerSocket.on_request, self.host, self.port) as server:
            print(f'WebSocket server started at ws://{self.host}:{self.port}')
            await server.serve_forever()


    async def on_request(websocket) -> None:

        try:
            async for message in websocket:
                try:
                    request = json.loads(message)
                    print(json.dumps(request, indent=4))
                    processor = Processor(tracer,websocket,request)
                    await asyncio.create_task(processor.start())

                except json.JSONDecodeError:
                    traceback.print_exc()
                    print('Received invalid JSON')
                    await websocket.send(json.dumps({
                        'type': 'error',
                        'error': 'Invalid JSON'
                    }))

                except Exception as e:
                    traceback.print_exc()
                    await websocket.send(json.dumps({
                        'type': 'error',
                        'error': f'{e}'
                    }))

        finally:
            await websocket.close() 


if __name__ == '__main__':

    load_dotenv()

    server = ServerSocket(
        host=os.getenv('SERVER_SOCKET_HOST', 'localhost'),
        port=int(os.getenv('SERVER_SOCKET_PORT', 8765)))

    asyncio.run(server.start())