import os
import json
import base64
import uuid
import asyncio
import aio_pika # type: ignore
from pika.exchange_type import ExchangeType # type: ignore
from dotenv import load_dotenv # type: ignore
from utils.publisher import update_project_image

load_dotenv()

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 3003))

IMAGES_HOST = os.getenv('IMAGES_HOST', 'localhost')
IMAGES_PORT = int(os.getenv('IMAGES_PORT', 3002))


class ProcessorWorker:

    def __init__(self, tracer, websocket, project, requests, images, save):
        self.tracer = tracer
        self.websocket = websocket
        self.project = project
        self.requests = requests
        self.images = images
        self.save = save
        self.ids = dict()
        self.channel = None
        self.connection = None
        self.consumer_tag = None
        self.exclusive_queue = str(uuid.uuid4())


    async def setup(self):

        await self.tracer.register(self.project)

        self.connection = await aio_pika.connect_robust(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT)

        self.channel = await self.connection.channel()

        for request in self.requests:

            request_queue = await self.channel.declare_queue(request['request_queue'], durable=True)
            results_queue = await self.channel.declare_queue(self.exclusive_queue, durable=True)

            await self.channel.declare_exchange(
                request['exchange'],
                aio_pika.ExchangeType.DIRECT,
                durable=True)

            await request_queue.bind(
                exchange=request['exchange'],
                routing_key=request['request_queue'])

            await results_queue.bind(
                exchange=request['exchange'],
                routing_key=self.exclusive_queue)

        results_queue = await self.channel.get_queue(self.exclusive_queue)
        self.consumer_tag = await results_queue.consume(self.on_response)


    async def on_response(self, message: aio_pika.IncomingMessage):

        async with message.process():

            properties = message.properties

            if properties.correlation_id in self.ids:

                response = json.loads(message.body.decode())
                correlation_id = properties.correlation_id
                image_id = self.ids[correlation_id]

                self.images[image_id]['iterations'] += 1
                self.images[image_id]['data'] = response['data']
                self.images[image_id]['mimetype'] = response['mimetype']
                self.images[image_id]['active'] = await self.tracer.getState(self.project)

                if await self.tracer.getState(self.project):
                    await self.update_progress()

                current_iteration = self.images[image_id]['iterations']
                print(f'Iteration {current_iteration}/{len(self.requests)}: {image_id}')

                if current_iteration < len(self.requests) and self.images[image_id]['active']:

                    current_request = self.requests[current_iteration]
                    current_request['request']['image'] = self.images[image_id]['data']

                    await self.channel.default_exchange.publish(
                        aio_pika.Message(
                            body=json.dumps(current_request['request']).encode(),
                            reply_to=self.exclusive_queue,
                            correlation_id=correlation_id),
                        routing_key=current_request['request_queue'])

                all_done = all(image['iterations'] == len(self.requests) for image in self.images.values())
                all_canceled = all(not image['active'] for image in self.images.values())

                if all_done or all_canceled:

                    print(f'All project images processed: {self.project} -> {json.dumps(self.ids, indent=0)}')

                    results_queue = await self.channel.get_queue(self.exclusive_queue)
                    await results_queue.cancel(self.consumer_tag)
                    await results_queue.delete(if_unused=False, if_empty=False)

                    if self.save and await self.tracer.getState(self.project):
                        await self.save_results()

                    await self.tracer.deregister(self.project)


    async def update_progress(self):

        images = list()
        tasks_completed = 0
        tasks_total = len(self.requests) * len(self.images)

        for image_id in self.images:
            tasks_completed += self.images[image_id]['iterations']
            if self.images[image_id]['iterations'] == len(self.requests) and not self.images[image_id]['sent']:
                self.images[image_id]['sent'] = True
                images.append({
                    "mimetype": self.images[image_id]['mimetype'],
                    "data": self.images[image_id]['data'],
                })

        await self.websocket.send(json.dumps({
            "type": "progress",
            "progress": tasks_completed/tasks_total,
            "project": self.project,
            "images": images,
        }))


    async def save_results(self):
        for image_id in self.images:
            if 'image' in self.images[image_id]['mimetype']: 
                image_bytes = base64.b64decode(self.images[image_id]['data'])
                update_project_image(IMAGES_HOST, IMAGES_PORT, self.project, image_id, image_bytes)
        await asyncio.sleep(0.001)


    async def start(self):

        if len(self.requests) > 0 and len(self.images) > 0:

            await self.setup()

            for image_id in self.images:

                correlation_id = str(uuid.uuid4())
                self.ids[correlation_id] = image_id
                self.images[image_id]['iterations'] = 0
                self.images[image_id]['mimetype'] = None
                self.images[image_id]['sent'] = False
                self.images[image_id]['active'] = True
                self.images[image_id]['data'] = base64.b64encode(self.images[image_id]['data']).decode('utf-8')

                current_request = self.requests[0]
                current_request['request']['image'] = self.images[image_id]['data']

                await self.channel.default_exchange.publish(
                    aio_pika.Message(
                        body=json.dumps(current_request['request']).encode(),
                        reply_to=self.exclusive_queue,
                        correlation_id=correlation_id),
                    routing_key=current_request['request_queue'])

            print(f'Start processing project images: {self.project} -> {json.dumps(self.ids, indent=0)}')