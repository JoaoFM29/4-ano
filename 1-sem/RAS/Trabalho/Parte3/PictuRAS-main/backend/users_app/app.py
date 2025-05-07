import os
from dotenv import load_dotenv # type: ignore
from flask import Flask # type: ignore
from mongoengine import connect # type: ignore
from flask_cors import CORS # type: ignore
from routes.users import users_blueprint

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
    db=os.getenv('USERS_DB','picturas-users'),
    host=os.getenv('MONGO_HOST','localhost'),
    port=int(os.getenv('MONGO_PORT', 27005)))

app.register_blueprint(users_blueprint, url_prefix="/users")

if __name__ == '__main__':
    app.run(
        host=os.getenv('USERS_HOST', '0.0.0.0'),
        port=int(os.getenv('USERS_PORT', 3005)),
        debug=True
    )