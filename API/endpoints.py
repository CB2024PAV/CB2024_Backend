from flask import Flask,request
from login_page import login_api
from qdrant import qdrant_api
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
app.register_blueprint(login_api)
app.register_blueprint(qdrant_api)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
