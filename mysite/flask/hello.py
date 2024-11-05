import flask
from flask import Flask
from flask_cors import CORS
from markupsafe import escape
import psycopg2
from .config import load_config
from recipes.models import Ingredient

app = Flask(__name__)
cors = CORS(app)
config = load_config()

number_list = [1,2,3,4,5,6]

@app.route("/")
def hello_world():
    response = flask.jsonify({'data': "I'm from the Bronx, err!"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/<name>")
def hello(name):
    response = flask.jsonify({'data': f"Hello, {escape(name)}!"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/numbers")
def numbers():
    return ", ".join([str(i) for i in number_list])

@app.route("/users")
def display_users():
    conn = psycopg2.connect(**config)
    cur = conn.cursor()
    users = []
    with psycopg2.connect(**config) as conn:
        command = "SELECT * FROM users"
        with conn.cursor() as cur:
            cur.execute(command)
            users = cur.fetchall()
    if users:
        users = [{'id': user[0], 'name': user[1]} for user in users]
    response = flask.jsonify({'data': users})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
