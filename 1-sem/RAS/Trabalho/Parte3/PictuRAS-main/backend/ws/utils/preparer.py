import os
import json
from dotenv import load_dotenv # type: ignore

load_dotenv()

EXCHANGE = os.getenv('EXCHANGE', 'TOOLS_EXCHANGE')

REQUEST_QUEUES = {
    'Binarization': os.getenv('BINARIZATION_QUEUE', 'BINARIZATION_QUEUE'),
    'Border': os.getenv('BORDER_QUEUE', 'BORDER_QUEUE'),
    'Brightness': os.getenv('BRIGHTNESS_QUEUE', 'BRIGHTNESS_QUEUE'),
    'Contrast': os.getenv('CONTRAST_QUEUE', 'CONTRAST_QUEUE'),
    'Crop': os.getenv('CROP_QUEUE', 'CROP_QUEUE'),
    'Object Counter': os.getenv('OBJECT_COUNTER_QUEUE', 'OBJECT_COUNTER_QUEUE'),
    'OCR': os.getenv('OCR_QUEUE', 'OCR_QUEUE'),
    'People Counter': os.getenv('PEOPLE_COUNTER_QUEUE', 'PEOPLE_COUNTER_QUEUE'),
    'Remove Background': os.getenv('AUTOCROP_QUEUE', 'AUTOCROP_QUEUE'),
    'Rotate': os.getenv('ROTATE_QUEUE', 'ROTATE_QUEUE'),
    'Scale': os.getenv('SCALE_QUEUE', 'SCALE_QUEUE'),
    'Watermark': os.getenv('WATERMARK_QUEUE', 'WATERMARK_QUEUE'),
}

handlers = {
    'Binarization': lambda tool : {},
    'Border': lambda tool : handle_border(tool),
    'Brightness': lambda tool : handle_brightness(tool),
    'Contrast': lambda tool : handle_contrast(tool),
    'Crop': lambda tool : handle_crop(tool),
    'Object Counter': lambda tool : {},
    'OCR': lambda tool : {},
    'People Counter': lambda tool : {},
    'Remove Background': lambda tool : {},
    'Rotate': lambda tool : handle_rotate(tool),
    'Scale': lambda tool : handle_scale(tool),
    'Watermark': lambda tool : {},
}


def get_parameter(name: str, parameters: list) -> dict:
    for parameter in parameters:
        if parameter['name'] == name:
            return parameter
    return None


def handle_border(tool: dict) -> dict:
    return {
        'border_height': get_parameter('border_height', tool['parameters'])['value'],
        'border_width': get_parameter('border_width', tool['parameters'])['value'],
        'border_color': get_parameter('border_color', tool['parameters'])['value'],
    }


def handle_brightness(tool: dict) -> dict:
    return {
        'brightness': get_parameter('brightness', tool['parameters'])['value'],
    }


def handle_contrast(tool: dict) -> dict:
    return {
        'contrast': get_parameter('contrast', tool['parameters'])['value'],
    }


def handle_crop(tool: dict) -> dict:
    return {
        'width': get_parameter('width', tool['parameters'])['value'],
        'height': get_parameter('height', tool['parameters'])['value'],
        'x_top_left': get_parameter('x_top_left', tool['parameters'])['value'],
        'y_top_left': get_parameter('y_top_left', tool['parameters'])['value'],
    }


def handle_rotate(tool: dict) -> dict:
    return {
        'angle': get_parameter('angle', tool['parameters'])['value'],
    }


def handle_scale(tool: dict) -> dict:
    return {
        'width': get_parameter('width', tool['parameters'])['value'],
        'height': get_parameter('height', tool['parameters'])['value'],
    }


def get_prepared_requets(tools: list) -> list:
    requests = []
    for tool in tools:
        requests.append({
            'exchange': EXCHANGE,
            'request_queue': REQUEST_QUEUES[tool['name']],
            'request': handlers[tool['name']](tool),
        })
    return requests