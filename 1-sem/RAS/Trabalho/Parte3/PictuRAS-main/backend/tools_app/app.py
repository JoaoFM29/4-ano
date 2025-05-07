import os
from dotenv import load_dotenv # type: ignore
from flask import Flask # type: ignore
from mongoengine import connect # type: ignore
from flask_cors import CORS # type: ignore
from routes.tools import tools_blueprint

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
    db=os.getenv('TOOLS_DB','picturas-tools'),
    host=os.getenv('MONGO_HOST','localhost'),
    port=int(os.getenv('MONGO_PORT', 27001)))

app.register_blueprint(tools_blueprint, url_prefix='/tools')

if __name__ == '__main__':
    app.run(
        host=os.getenv('TOOLS_HOST', '0.0.0.0'),
        port=int(os.getenv('TOOLS_PORT', 3001)),
        debug=True
    )