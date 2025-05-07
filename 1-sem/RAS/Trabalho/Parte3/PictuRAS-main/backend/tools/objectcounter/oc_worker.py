import os
import functools
import pika # type: ignore
import cv2 # type: ignore
from pika.exchange_type import ExchangeType # type: ignore
from detectron2.config import get_cfg # type: ignore
from detectron2.model_zoo import get_config_file, get_checkpoint_url # type: ignore
from multiprocessing.pool import ThreadPool
from oc_tool import ObjectCountingTool
from oc_message_request import ObjectCountingMessageRequest

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', '5672')

EXCHANGE=os.getenv('EXCHANGE', 'tools-exchange')
REQUEST_QUEUE = os.getenv('REQUEST_QUEUE', 'object-count-queue')
POOL_SIZE = int(os.getenv('POOL_SIZE', 5))

cfg = get_cfg()
cfg.merge_from_file(get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.WEIGHTS = get_checkpoint_url("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml")
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg.MODEL.DEVICE = "cuda" if cv2.cuda.getCudaEnabledDeviceCount() > 0 else "cpu"


class ObjectCountingWorker:

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
        self.pool.apply_async(ObjectCountingWorker.worker_handle_request, (ch, method, properties, body))


    def worker_handle_request(ch, method, properties, body):

        print(f'ObjectCountingWorker received image: {properties.correlation_id}')
        request = ObjectCountingMessageRequest.from_json(body.decode())
        tool = ObjectCountingTool(request,cfg)
        response = tool.apply().to_json()

        ch.connection.add_callback_threadsafe(
            functools.partial(ObjectCountingWorker.publish_response, ch, properties, response))

        ch.connection.add_callback_threadsafe(
            functools.partial(ObjectCountingWorker.ack_message, ch, method.delivery_tag))


    def publish_response(ch, properties, response):
        ch.basic_publish(
            exchange=EXCHANGE,
            routing_key=properties.reply_to,
            body=response.encode(),
            properties=pika.BasicProperties(
                correlation_id=properties.correlation_id))
        print(f'ObjectCountingWorker sent image: {properties.correlation_id}')


    def ack_message(ch, delivery_tag):
        ch.basic_ack(delivery_tag=delivery_tag)


    def start(self):
        self.setup()
        self.channel.start_consuming()


if __name__ == '__main__':
    server = ObjectCountingWorker()
    print('ObjectCountingWorker start consuming...')
    server.start()