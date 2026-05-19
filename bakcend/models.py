from enum import Enum

from flask import Flask, request, jsonify

class User:
  def __init__(self, id, name, password, age, gender):
    self.id = id
    self.name = name
    self.password = password
    self.age = age
    self.gender = gender


class Franchise(str, Enum):
    ANYTIME_FITNESS = "Anytime Fitness"
    FITNESS_FIRST = "Fitness First"
    SNAP_FITNESS = "Snap Fitness"
    PLUS_FITNESS = "Plus Fitness"
    CLUB_LIME = "Club Lime"


class Gym:
    def __init__(self, name, latitude, longitude, franchise):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.franchise = franchise