import os
import functools
import pika # type: ignore
from detectron2.config import get_cfg # type: ignore
from detectron2 import model_zoo # type: ignore
from pika.exchange_type import ExchangeType # type: ignore
from multiprocessing.pool import ThreadPool
from pc_tool import PeopleCountingTool
from pc_message_request import PeopleCountingMessageRequest

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', '5672')

EXCHANGE=os.getenv('EXCHANGE', 'tools-exchange')
REQUEST_QUEUE = os.getenv('REQUEST_QUEUE', 'people-count-queue')
POOL_SIZE = int(os.getenv('POOL_SIZE', 5))

cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 80


class PeopleCountingWorker:

    def __init__(self):
        self.parameters = pika.ConnectionParameters(host=RABBITMQ_HOST,port=RABBITMQ_PORT)
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        self.pool = ThreadPool(processes=POOL_SIZE)


    def setup(self):

        self.channel.queue_declare(queue=REQUEST_QUEUE, durable=True)

        self.channel.exchange_declare(
            exchange=EXCHANGE,
            exchange_type=ExchangeType.direct,
            durable=True)

        self.channel.queue_bind(
            queue=REQUEST_QUEUE,
            exchange=EXCHANGE,
            routing_key=REQUEST_QUEUE)

        self.channel.basic_consume(
            queue=REQUEST_QUEUE,
            on_message_callback=functools.partial(self.on_request))


    def on_request(self, ch, method, properties, body):
        self.pool.apply_async(PeopleCountingWorker.worker_handle_request, (ch, method, properties, body))


    def worker_handle_request(ch, method, properties, body):

        print(f'PeopleCountingWorker received image: {properties.correlation_id}')
        request = PeopleCountingMessageRequest.from_json(body.decode())
        tool = PeopleCountingTool(request,cfg)
        response = tool.apply().to_json()

        ch.connection.add_callback_threadsafe(
            functools.partial(PeopleCountingWorker.publish_response, ch, properties, response))

        ch.connection.add_callback_threadsafe(
            functools.partial(PeopleCountingWorker.ack_message, ch, method.delivery_tag))


    def publish_response(ch, properties, response):
        ch.basic_publish(
            exchange=EXCHANGE,
            routing_key=properties.reply_to,
            body=response.encode(),
            properties=pika.BasicProperties(
                correlation_id=properties.correlation_id))
        print(f'PeopleCountingWorker sent image: {properties.correlation_id}')


    def ack_message(ch, delivery_tag):
        ch.basic_ack(delivery_tag=delivery_tag)


    def start(self):
        self.setup()
        self.channel.start_consuming()


if __name__ == '__main__':
    server = PeopleCountingWorker()
    print('PeopleCountingWorker start consuming...')
    server.start()