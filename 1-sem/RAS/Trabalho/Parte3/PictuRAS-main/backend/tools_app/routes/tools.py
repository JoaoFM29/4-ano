from flask import Blueprint, request, jsonify # type: ignore
from controllers.tool import *
import traceback

tools_blueprint = Blueprint('tool', __name__)


@tools_blueprint.route('/', methods=['GET'])
def route_get_tools():
    tools = list_tools()
    return jsonify([tool.to_json() for tool in tools]), 200


@tools_blueprint.route('/<string:tool_id>', methods=['GET'])
def route_get_tool(tool_id: str):
    try:
        tool = find_by_id(tool_id)
        return jsonify(tool.to_json()), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 404


@tools_blueprint.route('/', methods=['POST'])
def route_insert_tool():
    try:
        tool = insert_tool(Tool(**request.json))
        return jsonify(tool.to_json()), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 500


@tools_blueprint.route('/<string:tool_id>', methods=['PUT'])
def route_update_tool(tool_id: str):
    try:
        tool = update_tool(tool_id, request.json)
        return jsonify(tool.to_json()), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 500


@tools_blueprint.route('/<string:tool_id>', methods=['DELETE'])
def route_delete_tool(tool_id: str):
    try:
        tool = delete_tool(tool_id)
        return jsonify(tool.to_json()), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 500
