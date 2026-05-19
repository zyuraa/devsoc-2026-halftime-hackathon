from fastapi import FastAPI
app = FastAPI()

class User:
    def __init__(self, id: int, name: str, password: str, age: int, gender: str):
        self.id = id
        self.name = name
        self.password = password
        self.age = age
        self.gender = gender
class Gym:
    def __init__(self, id: int, name: str, location: tuple):
        self.id = id
        self.name = name
        self.location = location

gym_list = [
    Gym(id=1, name="Gym A", location="City Center"),
    Gym(id=2, name="Gym B", location="Suburb"),
    Gym(id=3, name="Gym C", location="Downtown")
]

@app.post("/login")
def createUser(name: str, password: str, age: int, gender: str):
    user = User(id=1, name=name, password=password)
    return {"message": f"User {user.name} created successfully!"}
    

@app.get("/{id}/search")
def searchGyms(id: int):