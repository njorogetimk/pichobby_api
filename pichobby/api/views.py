from flask import jsonify
from pichobby.api import picapi


@picapi.route('/')
def home():
    return jsonify({"Pichobby Api": "My first API"})
