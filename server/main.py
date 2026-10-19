# Small Example Server. Not fully featured
from flask import Flask, jsonify, request, make_response, abort, send_file
from flask import Response, Request
from datetime import datetime as dt
import sqlite3
import os, uuid, pathlib
import regex as re

app = Flask(__name__)

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
        CX = sqlite3.connect("data.db")
        cu = CX.cursor()
        submission_id = uuid.uuid4()
        cu.execute(f"INSERT INTO log (uuid, lux, temperature, humidity, battery, emergency) VALUES ('{str(submission_id)}', {request.form.get('lux', 0)}, {request.form.get('temperature', 0)}, {request.form.get('humidity', 0)}, {1 if request.form.get('battery', 'STANDARD') == 'STANDARD' else 0}, {1 if request.form.get('trigger', 'ALARM') == 'ALARM' else 0})")
        if "video" in request.files.keys():
            request.files["video"].save(f"video/{submission_id}.mp4")
        cu.close()
        CX.commit()
        CX.close()
    else:
        abort(400, msg="wrong method; please use POST")

    return jsonify({
        "msg": "Saved!",
        "code": 200
    }), 200

@app.route("/video/<file>")
def video(file):
    path = pathlib.Path("video/" + file)
    if not path.exists():
        abort(404)
    return send_file(path.open("rb"), download_name="clip.mp4")

app.run("0.0.0.0", 5000)
