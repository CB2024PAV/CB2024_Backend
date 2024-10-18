from flask import Flask,request
from API.login_page import login_api
from API.qdrant import qdrant_api
from API.gemini import gemini_api
from API.twelve_labs import twelvelabs_api
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

# @app.route("/")
# def helloworld():
#     return "Hello World!"

app.register_blueprint(login_api)
app.register_blueprint(qdrant_api)
app.register_blueprint(gemini_api)
app.register_blueprint(twelvelabs_api)

if __name__ == "__main__":
    # app.run()
    app.run(host="0.0.0.0", port=5000, debug=True)
