from enum import Enum

from flask import Flask, request, jsonify

class User:
  def __init__(self, id, name, password, age, gender):
    self.id = id
    self.name = name
    self.password = password
    self.age = age
    self.gender = gender


class Gym:
    def __init__(self, id, name, latitude, longitude):
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
      