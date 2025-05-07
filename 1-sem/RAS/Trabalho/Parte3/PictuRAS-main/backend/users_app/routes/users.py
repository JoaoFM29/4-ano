from flask import Blueprint, request, jsonify # type: ignore
from models.user import User
from controllers.user import *
import traceback

users_blueprint = Blueprint('user', __name__)


@users_blueprint.route('/', methods=['GET'])
def route_get_users():
    users = list_users()
    return jsonify([user.to_json() for user in users]), 200


@users_blueprint.route('/<string:username>', methods=['GET'])
def route_get_user(username: str):
    try:
        user = find_by_username(username)
        return jsonify(user.to_json()), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 404


@users_blueprint.route('/', methods=['POST'])
def route_insert_user():
    try:
        user = insert_user(User(**request.json))
        return jsonify(user.to_json()), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 500


@users_blueprint.route('/<string:username>', methods=['PUT'])
def route_update_user(username: str):
    try:
        user = update_user(username,request.json)
        return jsonify(user.to_json()), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 500


@users_blueprint.route('/<string:username>', methods=['DELETE'])
def route_delete_user(username: str):
    try:
        user = delete_user(username)
        return jsonify(user.to_json()), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 500