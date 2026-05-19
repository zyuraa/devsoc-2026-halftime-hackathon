from flask import Flask, request, jsonify
from models.py import User, Gym
from services.py import generate_secure_userid

app = Flask(__name__)
db = [] #temp
gyms = [] #temp
ids = [] #temp

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    user = User(
        email=data.get("email"),
        name=data.get("name"),
        password=data.get("password"),
        age=data.get("age"),
        id = generate_secure_userid()
    )
    db.append(user)
    return jsonify({"id": user.id, "message": "success"})
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    # Add login logic here
    for u in db:
        if u.email == data.get("email") and u.password == data.get("password"):
            return jsonify({"id": u.id, "message": "success"})
    return jsonify({"message": "Invalid credentials!"}), 401

@app.route("/<id>/search", methods=["GET"])
# user searches for gyms
@app.route("/<id>/groups", methods=["GET"])
# user searches for groups

@app.route("/<id>/groups", methods=["POST"])
# user creates a group

@app.route("/<id>/groups/<group_id>", methods=["PUT"])
# user joins a group

@app.route("/<id>/groups/<group_id>", methods=["PUT"])
# user leaves a group

@app.route("/<id>/groups/<group_id>", methods=["DELETE"])
# user deletes a group

@app.route()
@app.route("/")
def home():
    return "Ashesh Mahidadia approves!"

if __name__ == "__main__":
    app.run(debug=True)