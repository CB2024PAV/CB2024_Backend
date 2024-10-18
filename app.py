import time
from flask import Flask,request
from API.login_page import login_api
from API.qdrant import qdrant_api
from API.gemini import gemini_api
from API.twelve_labs import twelvelabs_api
from flask_cors import CORS
import uuid
import os
from flask import g

qdrant_url = os.environ.get('QDRANT_URL')
qdrant_key = os.environ.get('QDRANT_KEY')



app = Flask(__name__)
CORS(app)

@app.before_request
def before_request_func():
    execution_id = uuid.uuid4()
    g.start_time = time.time()
    g.execution_id = execution_id

    print(g.execution_id, "ROUTE CALLED ", request.url)

@app.route("/")
def helloworld():
    return "Hello World!"

app.register_blueprint(login_api)
app.register_blueprint(qdrant_api)
app.register_blueprint(gemini_api)
app.register_blueprint(twelvelabs_api)

if __name__ == "__main__":
    # app.run()
    app.run(host="0.0.0.0", port=os.environ.get('PORT'))
