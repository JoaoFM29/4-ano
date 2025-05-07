import os
import asyncio
from dotenv import load_dotenv # type: ignore
from flask import Flask # type: ignore
from mongoengine import connect # type: ignore
from flask_cors import CORS # type: ignore
from threading import Thread
from serversocket.serversocket import ServerSocket
from routes.projects import projects_blueprint

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
    db=os.getenv('PROJECTS_DB','picturas-projects'),
    host=os.getenv('MONGO_HOST','localhost'),
    port=int(os.getenv('MONGO_PORT', 27003)))


app.register_blueprint(projects_blueprint, url_prefix='/projects')


if __name__ == '__main__':

    app.run(
        host=os.getenv('PROJECTS_HOST', '0.0.0.0'),
        port=int(os.getenv('PROJECTS_PORT', 3003)),
        debug=True)