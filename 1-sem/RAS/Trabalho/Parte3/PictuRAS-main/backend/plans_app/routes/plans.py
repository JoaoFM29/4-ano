from flask import Blueprint, request, jsonify # type: ignore
from models.plan import Plan
from controllers.plan import *
import traceback

plans_blueprint = Blueprint('plan', __name__)


@plans_blueprint.route('/', methods=['GET'])
def route_get_plans():
    plans = list_plans()
    return jsonify([plan.to_json() for plan in plans]), 200


@plans_blueprint.route('/<string:plan_id>', methods=['GET'])
def route_get_plan(plan_id: str):
    try:
        plan = find_by_id(plan_id)
        return jsonify(plan.to_json()), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 404


@plans_blueprint.route('/', methods=['POST'])
def route_insert_plan():
    try:
        plan = insert_plan(Plan(**request.json))
        return jsonify(plan.to_json()), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 500


@plans_blueprint.route('/<string:plan_id>', methods=['PUT'])
def route_update_plan(plan_id: str):
    try:
        plan = update_plan(plan_id,request.json)
        return jsonify(plan.to_json()), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 500


@plans_blueprint.route('/<string:plan_id>', methods=['DELETE'])
def route_delete_plan(plan_id: str):
    try:
        plan = delete_plan(plan_id)
        return jsonify(plan.to_json()), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{e}'}), 500