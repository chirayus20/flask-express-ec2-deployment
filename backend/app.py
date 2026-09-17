from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash
import logging
import re

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# get db details from .env
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_cluster = os.getenv("DB_CLUSTER")
db_name = os.getenv("DB_NAME")

mongo_uri = f"mongodb+srv://{db_user}:{db_password}@{db_cluster}/?retryWrites=true&w=majority"

client = MongoClient(mongo_uri)
db = client[db_name]
collection = db["data"]

@app.route("/")
def home():
    return "Backend Running Successfully"

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/process", methods=["POST"])
def process():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "message": "No data received"}), 400

        name = data.get("name")
        password = data.get("password")

        name = name.strip() if name else ""
        password = password.strip() if password else ""

        # check if name and password is given
        if not name or not password:
            return jsonify({"success": False, "message": "Name and password required"}), 400

        if len(name) < 2:
            return jsonify({"success": False, "message": "Name too short"}), 400

        if len(password) < 4:
            return jsonify({"success": False, "message": "Password too short"}), 400
        
        if re.search(r'\s', name):
            return jsonify({"success": False, "message": "Name cannot contain spaces"}), 400

        if re.search(r'\s', password):
            return jsonify({"success": False, "message": "Password cannot contain spaces"}), 400

        # hash the password
        hashed = generate_password_hash(password)

        collection.insert_one({
            "name": name,
            "password": hashed
        })

        logger.info("Data saved for: %s", name)

        return jsonify({"success": True})

    except Exception as e:
        logger.error("Error: %s", str(e))
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
    