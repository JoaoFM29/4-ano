# server.py
import asyncio
import json
import websockets

connected_clients = set()

async def handle_client(websocket):
    # Add the new client to the set of connected clients
    connected_clients.add(websocket)
    print("Client connected")
    images = []
    try:
        async for message in websocket:
            # Parse the incoming message as JSON
            data = json.loads(message)
            print(f"Received message: {data}")
            
            # Check the type of the message
            if data["type"] == "process_project":
                project_id = data["id_projeto"]
                print(f"Processing project with ID: {project_id}")

                # Simulate processing and send progress updates
                for progress in range(0, 101, 10):  # Progress in 10% increments
                    progress_message = {
                        "type": "progress",
                        "progress": f"{progress}%",
                        "images": images
                    }
                    await websocket.send(json.dumps(progress_message))
                    images.append("6787f967941418ba20905f0e")
                    await asyncio.sleep(1)  # Simulate processing time

                # Send the final result when processing is complete
                result_message = {
                    "type": "result",
                    "images": "congrats, its working!",
                }
                await websocket.send(json.dumps(result_message))
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        # Remove the client when it disconnects
        connected_clients.remove(websocket)

# Start the server
async def main():
    server = await websockets.serve(handle_client, "localhost", 8080)
    print("WebSocket server started on ws://localhost:8080")
    await server.wait_closed()

asyncio.run(main())
