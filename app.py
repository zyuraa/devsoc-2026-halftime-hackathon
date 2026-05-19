from flask import Flask, request, jsonify
from bakcend.models import User, Gym, Group
from bakcend.services import generate_secure_userid, delete_group_after
from bakcend.search import search_gyms

app = Flask(__name__)
users = [] #temp
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
        gender=data.get("gender"),
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
@app.route("/<id>", methods=["DELETE"])
# user deletes their account
def delete_user(id):
    data = request.get_json()
    confirm = 0
    for u in users:
        if u.id == id:
            users.remove(u)
            confirm = 1
            break
    for g in gyms:
        for gr in g.groups:
            if id in gr.members:
                gr.members.remove(id)
                confirm += 1
    if confirm == 2:
        return jsonify({"message": "success"})
    
    return jsonify({"message": "User not found!"}), 404

@app.route("/<id>", methods=["GET"])
def get_user(id):
    for u in users:
        if u.id == id:
            return jsonify({
                "email": u.email,
                "name": u.name,
                "age": u.age,
                "gender": u.gender,
                "message": "success"
            })
    return jsonify({"message": "User not found!"}), 404

# @app.route("/<id>/search", methods=["GET"])
# # user searches for gyms
# def search(id):
#     data = request.get_json()
#     found_gyms = search_gyms(
#         longitude=data.get("longitude"),
#         latitude=data.get("latitude"),
#         limit=data.get("limit"),
#         radius_km=data.get("radius_km")
#     )

#     return jsonify({"gyms": [gym.name for gym in found_gyms]})


@app.route("/<id>/search", methods=["GET"])
def search(id):
    longitude = request.args.get("longitude", type=float)
    latitude = request.args.get("latitude", type=float)
    limit = request.args.get("limit", default=10, type=int)
    radius_km = request.args.get("radius_km", default=5, type=float)

    print("longitude:", longitude)
    print("latitude:", latitude)
    print("limit:", limit)
    print("radius_km:", radius_km)
    found_gyms = []
    found_gyms = search_gyms(
        longitude,
        latitude,
        limit,
        radius_km
    )

    print("found_gyms:", found_gyms)

    return jsonify({"gyms": [gym.name for gym in found_gyms]})
@app.route("/<id>/groups", methods=["GET"])
# user searches for groups

@app.route("/<id>/groups", methods=["POST"])
def create_group():
    data = request.get_json()
    # Add group creation logic here
    group = Group(
        id=generate_secure_userid(),
        gym=data.get("gym"),
        time_start=data.get("time_start"),
        time_end=data.get("time_end"),
        members=data.get("members")
    )
    for g in gyms:
        if g.name == group.gym:
            g.groups.append(group)
            delete_group_after(group.id, group.time_end - group.time_start) # schedule group deletion after the end time
            return jsonify({"id": group.id, "message": "success"})
            
        
    return jsonify({"message": "Gym not found!"}), 404
# user creates a group

@app.route("/<id>/groups/<group_id>", methods=["PUT"])
# user joins a group
def join_group(id, group_id):
    for g in gyms:
        for gr in g.groups:
            if gr.id == group_id:
                gr.members.append(id)
                return jsonify({"message": "success"})
    return jsonify({"message": "Group not found!"}), 404

@app.route("/<id>/groups/<group_id>/leave", methods=["PUT"])
# user leaves a group
def leave_group(id, group_id):
    for g in gyms:
        for gr in g.groups:
            if gr.id == group_id:
                gr.members.remove(id)
                return jsonify({"message": "success"})
    return jsonify({"message": "Group not found!"}), 404

@app.route("/<id>/groups/<group_id>", methods=["DELETE"])
# user deletes a group
def delete_group(id, group_id):
    for g in gyms:
        for gr in g.groups:
            if gr.id == group_id:
                gyms.remove(gr) # or g.groups.remove(gr) depending on how you store groups in gyms
                return jsonify({"message": "success"})
    return jsonify({"message": "Group not found!"}), 404

@app.route("/")
def home():
    return "Ashesh Mahidadia approves!"

if __name__ == "__main__":
    app.run(debug=True)