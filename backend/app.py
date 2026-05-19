from flask import Flask, request, jsonify
from models import User, Gym, Group
from services import generate_secure_userid, delete_group_after
from search import search_gyms
from datetime import datetime, timedelta


app = Flask(__name__)
users = [] #temp
gyms = [] #temp // gym class
ids = [] #temp

# Helpers
def find_user_by_id(user_id):
    for user in users:
        if str(user.id) == str(user_id):
            return user
    return None

# Routes

@app.route("/groups/<gym_id>", methods=["GET"])
# get groups from gym
def get_gym_groups(gym_id):

    for g in gyms:
        if g.id == gym_id:
            gym_groups = g.groups
            return jsonify({"groups": [
                {
                    "id": gr.id,
                    "gym": gr.gym,
                    "time_start": gr.time_start,
                    "time_end": gr.time_end,
                    "members": [
                        {
                            "name": m.name,
                            "age": m.age
                            }
                                for m in gr.members
                    ]
                    } for gr in gym_groups]})
    
    return jsonify({"groups": []}), 200

@app.route("/<id>/groups/current", methods=["GET"])
# get groups from user
def get_current_groups(id):
    current_groups = []
    for g in gyms:
        for gr in g.groups:
            if any(str(m.id) == str(id) for m in gr.members):
                current_groups.append(gr)
    return jsonify({"groups": [
                    {
                        "id": gr.id,
                        "gym": gr.gym,
                        "time_start": gr.time_start,
                        "time_end": gr.time_end,
                        "members": [
                            {
                                    "name": m.name,
                                    "age": m.age
                                    }
                                        for m in gr.members
                        ]
                        } for gr in current_groups]})

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Missing JSON body"}), 400

    required_fields = ["email", "name", "password", "age"]

    for field in required_fields:
        if field not in data or data.get(field) in [None, ""]:
            return jsonify({"error": f"Missing field: {field}"}), 400
        
    user = User(
        email=data.get("email"),
        name=data.get("name"),
        password=data.get("password"),
        age=data.get("age"),
        id = generate_secure_userid()
    )
    users.append(user)
    return jsonify({"id": user.id, "message": "success"})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    # Add login logic here
    for u in users:
        if u.email == data.get("email") and u.password == data.get("password"):
            return jsonify({"id": u.id, "message": "success"})
    return jsonify({"message": "Invalid credentials!"}), 401

@app.route("/<id>/search", methods=["GET"])
def search(id):
    longitude = request.args.get("longitude", type=float)
    latitude = request.args.get("latitude", type=float)
    limit = request.args.get("limit", default=10, type=int)
    radius_km = request.args.get("radius_km", default=5, type=float)

    if longitude is None:
        return jsonify({"error": "Missing longitude"}), 400

    if latitude is None:
        return jsonify({"error": "Missing latitude"}), 400

    if limit <= 0:
        return jsonify({"error": "Limit must be greater than 0"}), 400

    if radius_km <= 0:
        return jsonify({"error": "Radius must be greater than 0"}), 400

    found_gyms = search_gyms(
        longitude=longitude,
        latitude=latitude,
        limit=limit,
        radius_km=radius_km
    )

    for gym in found_gyms:
        if (gym not in gyms):
            gyms.append(gym)

    return jsonify({"gyms": [{
        "id": gym.id,
        "name": gym.name,
        "groups": gym.groups
    }                       
        for gym in found_gyms]})

@app.route("/<id>", methods=["GET"])
def getUserInfo(id):
    for u in users:
        if u.id == id:
            return jsonify({
                "name": u.name,
                "email": u.email
                })
    return jsonify({"message": "User not found!"}), 404

@app.route("/<id>/groups", methods=["GET"])
# user searches for groups
# input: gym name, time start, time end
# output: list of groups matching the criteria
def search_groups(id):
    gym_name = request.args.get("gym_name")
    time_start = request.args.get("time_start")
    time_end = request.args.get("time_end")

    if not gym_name:
        return jsonify({"error": "Missing gym_name"}), 400

    if not time_start:
        return jsonify({"error": "Missing time_start"}), 400

    if not time_end:
        return jsonify({"error": "Missing time_end"}), 400
    
    matching_groups = []
    for g in gyms:
        if g.name == gym_name:
            for gr in g.groups:
                if gr.time_start >= time_start and gr.time_end <= time_end:
                    matching_groups.append(gr)
    return jsonify({"groups": [
        {
            "id": gr.id,
            "gym": gr.gym,
            "time_start": gr.time_start,
            "time_end": gr.time_end,
            "members": [
                {
                    "name": m.name,
                    "age": m.age
                }
                for m in gr.members
            ]
        }
        for gr in matching_groups
    ]})

@app.route("/<id>/groups", methods=["POST"])
def create_group(id):
    # user creates a group
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Missing JSON body"}), 400

    if not data.get("gym"):
        return jsonify({"error": "Missing field: gym"}), 400

    if not data.get("time_start"):
        return jsonify({"error": "Missing field: time_start"}), 400

    if not data.get("time_end"):
        return jsonify({"error": "Missing field: time_end"}), 400
    
    member_ids = data.get("members", [])
    members = []
    for member_id in member_ids:
        user = find_user_by_id(member_id)
        if user is not None:
            members.append(user)

    group = Group(
        id=generate_secure_userid(),
        gym=data.get("gym"),
        time_start=data.get("time_start"),
        time_end=data.get("time_end"),
        members=members
    )
    for g in gyms:
        if g.name == group.gym:
            g.groups.append(group)

            time_end = datetime.fromisoformat(group.time_end)
            delay_seconds = (time_end - datetime.now()).total_seconds()

            delete_group_after(group.id, delay_seconds, gyms) # schedule group deletion after the end time
            return jsonify({"id": group.id, "message": "success"})
            
        
    return jsonify({"message": "Gym not found!"}), 404

@app.route("/<id>/groups/<group_id>", methods=["PUT"])
def join_group(id, group_id):
    user = find_user_by_id(id)

    if user is None:
        return jsonify({"message": "User not found!"}), 404

    for g in gyms:
        for gr in g.groups:
            if str(gr.id) == str(group_id):
                if not any(str(m.id) == str(id) for m in gr.members):
                    gr.members.append(user)

                return jsonify({"message": "success"})

    return jsonify({"message": "Group not found!"}), 404

@app.route("/<id>/groups/<group_id>/leave", methods=["PUT"])
def leave_group(id, group_id):
    for g in gyms:
        for gr in g.groups:
            if str(gr.id) == str(group_id):
                gr.members = [
                    m for m in gr.members
                    if str(m.id) != str(id)
                ]

                return jsonify({"message": "success"})

    return jsonify({"message": "Group not found!"}), 404

@app.route("/<id>/groups/<group_id>", methods=["DELETE"])
# user deletes a group
def delete_group(id, group_id):
    for g in gyms:
        for gr in g.groups:
            if gr.id == group_id:
                g.groups.remove(gr)
                return jsonify({"message": "success"})
    return jsonify({"message": "Group not found!"}), 404

@app.route("/")
def home():
    return "Ashesh Mahidadia approves!"

if __name__ == "__main__":
    app.run(debug=True)