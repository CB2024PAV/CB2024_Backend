from flask import Blueprint,request
import jsonify

login_api = Blueprint('login_api', __name__)

@login_api.route("/login", methods=['POST'])
def login():
    data = request.form
    username = data.get('usr')
    password = data.get('pass')
    if username == "Bob" and password == "password":
        return {
            "success": True,
            "message":"Login Successful",
            "data":{}
        }
    else:
        return {
            "success": False,
            "message":"Login Successful",
            "data":{}
        }


@login_api.route("/hello", methods=['GET'])
def asds():
    return "Hey"