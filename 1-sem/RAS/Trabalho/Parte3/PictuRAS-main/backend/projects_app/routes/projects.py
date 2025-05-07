import os
from io import BytesIO
from dotenv import load_dotenv # type: ignore
from flask import Blueprint, request, jsonify, send_file # type: ignore
from models.project import Project
from controllers.project import *
import traceback
import requests

load_dotenv()

IMAGES_HOST = os.getenv('IMAGES_HOST','localhost')
IMAGES_PORT = os.getenv('IMAGES_PORT','3002')

projects_blueprint = Blueprint('project', __name__)


@projects_blueprint.route('/', methods=['GET'])
def route_get_projects():
    projects = list_projects()
    return jsonify([project.to_json() for project in projects]), 200


@projects_blueprint.route('/<string:project_id>', methods=['GET'])
def route_get_project(project_id: str):
    try:
        project = find_by_id(project_id)
        return jsonify(project.to_json()), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 404


@projects_blueprint.route('/owner/<string:user_id>', methods=['GET'])
def route_get_user_projects(user_id: str):
    try:
        projects = find_user_projects(user_id)
        return jsonify([project.to_json() for project in projects]), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 404


@projects_blueprint.route('/images/<string:project_id>', methods=['GET'])
def route_get_project_images(project_id: str):
    try:
        response = requests.get(f'http://{IMAGES_HOST}:{IMAGES_PORT}/images/project/{project_id}')
        return jsonify(response.json()), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 404


@projects_blueprint.route('/images/data/<string:image_id>', methods=['GET'])
def route_get_image_data(image_id: str):
    try:
        response = requests.get(f'http://{IMAGES_HOST}:{IMAGES_PORT}/images/data/{image_id}')
        return send_file(BytesIO(response.content), mimetype=response.headers.get('Content-Type')), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 404


@projects_blueprint.route('/', methods=['POST'])
def route_insert_project():
    try:
        project = Project(**request.json)
        project = insert_project(project)
        return jsonify(project.to_json()), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 500
    

@projects_blueprint.route('/images/<string:project_id>', methods=['POST'])
def route_insert_project_image(project_id: str):
    try:
        find_by_id(project_id)
        response = requests.post(
            f'http://{IMAGES_HOST}:{IMAGES_PORT}/images',
            files=request.files,
            data={**request.form, 'project': project_id})
        response.raise_for_status()
        return jsonify(response.json()), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 500


@projects_blueprint.route('/<string:project_id>', methods=['PUT'])
def route_update_project(project_id: str):
    try:
        project = update_project(project_id,request.json)
        return jsonify(project.to_json()), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 500


@projects_blueprint.route('/<string:project_id>', methods=['DELETE'])
def route_delete_project(project_id: str):
    try:
        response = requests.get(f'http://{IMAGES_HOST}:{IMAGES_PORT}/images')
        response.raise_for_status()

        for image in response.json():
            if image['project'] == project_id:
                requests.delete(f'http://{IMAGES_HOST}:{IMAGES_PORT}/images/{image['id']}')
                response.raise_for_status()

        project = delete_project(project_id)
        return jsonify(project.to_json()), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 500
    

@projects_blueprint.route('/images/<string:image_id>', methods=['DELETE'])
def route_delete_project_image(image_id: str):
    try:
        response = requests.delete(f'http://{IMAGES_HOST}:{IMAGES_PORT}/images/{image_id}')
        response.raise_for_status()
        return jsonify(response.json()), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 500