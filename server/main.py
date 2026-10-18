# Small Example Server. Not fully featured
from flask import Flask, jsonify, request, make_response, abort
from flask import Response, Request
import sqlite3

app = Flask(__name__)
CX = sqlite3.connect("data.db")

@app.errorhandler(400)
def error400(msg: str = "Bad Request"):
    return jsonify({
        "msg": msg,
        "code": 400
    }), 400

@app.errorhandler(404)
def error404(msg: str = "not found"):
    return jsonify({
        "msg": msg,
        "code": 404
    }), 404

@app.route("/")
def index():
    return jsonify({
        "msg": "Hello World!",
        "code": 200
    }), 200

@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        cu = CX.cursor()
        cu.execute(f"")
    else:
        return abort(400, msg="wrong method; please use POST")

    return Response()
