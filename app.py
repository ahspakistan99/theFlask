from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from pymongo import MongoClient  # type: ignore[reportMissingImports]


load_dotenv()

app = Flask(__name__)

# MongoDB connection
client = MongoClient(os.getenv("MONGODB_URI"))

db = client[os.getenv("MONGODB_DB", "my_db")]
users_collection = db["users"]


# Home endpoint
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Flask MongoDB API is running",
        "endpoints": [
            "GET /users",
            "POST /users"
        ]
    })


# GET users
@app.route("/users", methods=["GET"])
def get_users():
    users = list(users_collection.find({}, {"_id": 0}))
    return jsonify(users)


# POST user
@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON data is required"}), 400

    required_fields = ["name", "email", "age"]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"Missing field: {field}"
            }), 400

    result = users_collection.insert_one(data)

    return jsonify({
        "message": "User added successfully",
        "id": str(result.inserted_id)
    }), 201


if __name__ == "__main__":
    app.run(debug=True)