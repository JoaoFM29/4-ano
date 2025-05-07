from io import BytesIO
from flask import Blueprint, request, jsonify, send_file # type: ignore
from models.image import Image
from controllers.image import *
import traceback

images_blueprint = Blueprint('image', __name__)


@images_blueprint.route('/', methods=['GET'])
def route_get_images():
    images = list_images()
    return jsonify([image.to_json() for image in images]), 200


@images_blueprint.route('/<string:image_id>', methods=['GET'])
def route_get_image(image_id: str):
    try:
        image = find_by_id(image_id)
        return jsonify(image.to_json()), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 404


@images_blueprint.route('/info/<string:image_id>', methods=['GET'])
def route_get_image_info(image_id: str):
    try:
        image_info = find_info_by_id(image_id)
        return jsonify(image_info.to_json()), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 404


@images_blueprint.route('/project/<string:project_id>', methods=['GET'])
def route_get_project_images(project_id: str):
    images = list_project_images(project_id)
    return jsonify([image.to_json() for image in images]), 200


@images_blueprint.route('/data/<string:image_id>', methods=['GET'])
def route_get_image_data(image_id: str):
    try:
        chunks = find_chunks_by_id(image_id)
        image_info = find_info_by_id(image_id)
        data = b''.join(chunk.data for chunk in chunks)
        return send_file(BytesIO(data), mimetype=f'image/{image_info.format.lower()}'), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 404


@images_blueprint.route('/<string:image_id>', methods=['DELETE'])
def route_delete_image(image_id: str):
    try:
        image = delete_image(image_id)
        return jsonify({'id': str(image.id)}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 500


@images_blueprint.route('/', methods=['POST'])
def route_insert_image():
    try:
        image = Image(
            project=request.form.get('project'),
            image=BytesIO(request.files['image'].read()))
        image = insert_image(image)
        return jsonify(image.to_json()), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 500


@images_blueprint.route('/<string:image_id>', methods=['PUT'])
def route_update_image(image_id: str):
    try:
        image = Image(
            project=request.form.get('project'),
            image=BytesIO(request.files['image'].read()))
        image = update_image(image_id,image)
        return jsonify(image.to_json()), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 500
