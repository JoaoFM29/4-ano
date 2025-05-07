import re
import os
import json
import asyncio
from dotenv import load_dotenv # type: ignore
from utils.fetch import *
from utils.preparer import get_prepared_requets
from processor.processor_worker import ProcessorWorker

load_dotenv()

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

IMAGES_HOST = os.getenv('IMAGES_HOST', 'localhost')
IMAGES_PORT = int(os.getenv('IMAGES_PORT', 3002))

PROJECTS_HOST = os.getenv('PROJECTS_HOST', 'localhost')
PROJECTS_PORT = int(os.getenv('PROJECTS_PORT', 3003))

USERS_HOST = os.getenv('USERS_HOST', 'localhost')
USERS_PORT = int(os.getenv('USERS_PORT', 3005))

PLANS_HOST = os.getenv('PLANS_HOST', 'localhost')
PLANS_PORT = int(os.getenv('PLANS_PORT', 3004))

TOOLS_HOST = os.getenv('TOOLS_HOST', 'localhost')
TOOLS_PORT = int(os.getenv('TOOLS_PORT', 3005))


class Processor:

    def __init__(self, tracer, websocket, request):
        self.tracer = tracer
        self.request = request
        self.websocket = websocket
        self.handlers = {
            'process': lambda tracer, websocket, request : Processor.process_project(tracer, websocket, request, True),
            'preview': lambda tracer, websocket, request : Processor.process_project(tracer, websocket, request, False),
            'cancel': lambda tracer, websocket, request : Processor.process_cancel(tracer, websocket, request),
            'error': lambda tracer, websocket, request : Processor.process_error(tracer, websocket, request),
        }


    async def process_project(tracer, websocket, request, save):

        images = {}
        premium_user = False

        project = fetch_project(PROJECTS_HOST, PROJECTS_PORT, request['project'])

        if save:
            images = fetch_project_images(IMAGES_HOST, IMAGES_PORT, request['project'])
            images = {image['id']: {'data': fetch_image_data(IMAGES_HOST, IMAGES_PORT, image['id'])} for image in images}

        else:
            images = {request['image']: {'data': fetch_image_data(IMAGES_HOST, IMAGES_PORT, request['image'])}}

        if EMAIL_REGEX.match(project['owner']):
            user = fetch_user(USERS_HOST, USERS_PORT, project['owner'])
            plan = fetch_plan(PLANS_HOST, PLANS_PORT, user['plan'])
            print(plan['name'])
            premium_user = (plan['name'] == 'premium' or plan['name'] == 'enterprise')

        print(premium_user)
        if not premium_user:
            for tool in project['tools']:
                if fetch_tool(TOOLS_HOST, TOOLS_PORT, tool['id'])['premium']:
                    raise Exception(f'User {project['owner']} can not use premium tools')

        bus_requests = get_prepared_requets(project['tools'])
        print(json.dumps(bus_requests, indent=4))

        processorWorker = ProcessorWorker(tracer, websocket, request['project'], bus_requests, images, save)
        await processorWorker.start()


    async def process_cancel(tracer, websocket, request):
        project = request['project']
        print(f'Canceling project: {project}')
        await tracer.cancel(project)


    async def process_error(tracer, websocket, request):
        error = request['error']
        print(f'Error: {error}')
        await asyncio.sleep(0.001)


    async def start(self):
        type = self.request['type']
        handler = self.handlers.get(type)
        await handler(self.tracer, self.websocket, self.request)