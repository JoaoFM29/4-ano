import requests


def fetch_project(host, port, project):
    response = requests.get(f'http://{host}:{port}/projects/{project}')
    response.raise_for_status()
    return response.json()


def fetch_user(host, port, username):
    response = requests.get(f'http://{host}:{port}/users/{username}')
    response.raise_for_status()
    return response.json()


def fetch_plan(host, port, plan_id):
    response = requests.get(f'http://{host}:{port}/plans/{plan_id}')
    response.raise_for_status()
    return response.json()


def fetch_tool(host, port, tool_id):
    response = requests.get(f'http://{host}:{port}/tools/{tool_id}')
    response.raise_for_status()
    return response.json()


def fetch_project_images(host, port, project):
    response = requests.get(f'http://{host}:{port}/images/project/{project}')
    response.raise_for_status()
    return response.json()


def fetch_image_data(host, port, image_id):
    response = requests.get(f'http://{host}:{port}/images/data/{image_id}')
    response.raise_for_status()
    return response.content