import io
import requests


def update_project_image(host, port, project_id, image_id, image_data):

    response = requests.put(
        f'http://{host}:{port}/images/{image_id}',
        files={'image': io.BytesIO(image_data)},
        data={'project': project_id})

    response.raise_for_status()
    return response.json()