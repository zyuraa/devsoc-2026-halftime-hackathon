from flask import Flask, request, jsonify
from models.py import User, Gym

app = Flask(__name__)
db = [] #temp

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    user = User(
        id=data.get("id"),
        name=data.get("name"),
        password=data.get("password"),
        age=data.get("age"),
    )
    db.append(user)
    return jsonify({"message": "User registered successfully!"})
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User(
        id=data.get("id"),
        name=data.get("name"),
        password=data.get("password"),
        age=data.get("age"),
        gender=data.get("gender")
    )
    # Add login logic here
    for u in db:
        if u.name == user.name and u.password == user.password:
            return user.id
            return redirect(url_for("home"))
    return jsonify({"message": "Invalid credentials!"}), 401



@app.route("/")
def home():
    return "Ashesh Mahidadia approves!"

if __name__ == "__main__":
    app.run(debug=True)