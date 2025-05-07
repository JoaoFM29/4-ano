import os
from dotenv import load_dotenv # type: ignore
from flask import Flask # type: ignore
from mongoengine import connect # type: ignore
from flask_cors import CORS # type: ignore
from routes.plans import plans_blueprint

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
    db=os.getenv('PLANS_DB','picturas-plans'),
    host=os.getenv('MONGO_HOST','localhost'),
    port=int(os.getenv('MONGO_PORT', 27004)))

app.register_blueprint(plans_blueprint, url_prefix='/plans')

if __name__ == '__main__':
    app.run(
        host=os.getenv('PLANS_HOST', '0.0.0.0'),
        port=int(os.getenv('PLANS_PORT', 3004)),
        debug=True
    )