import os
from dotenv import load_dotenv # type: ignore
from flask import Flask # type: ignore
from mongoengine import connect # type: ignore
from flask_cors import CORS # type: ignore
from routes.images import images_blueprint

load_dotenv()

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": [
            os.getenv('API_GATEWAY','http://localhost:*')
        ]
    }
})

connect(
    db=os.getenv('IMAGES_DB','picturas-images'),
    host=os.getenv('MONGO_HOST','localhost'),
    port=int(os.getenv('MONGO_PORT', 27002)))

app.register_blueprint(images_blueprint, url_prefix='/images')

if __name__ == '__main__':
    app.run(
        host=os.getenv('IMAGES_HOST', '0.0.0.0'),
        port=int(os.getenv('IMAGES_PORT', 3002)),
        debug=True
    )