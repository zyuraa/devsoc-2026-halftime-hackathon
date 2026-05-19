from enum import Enum

from flask import Flask, request, jsonify

class User:
  def __init__(self, email, name, password, age, gender, id):
    self.email = email
    self.name = name
    self.password = password
    self.age = age
    self.gender = gender
    self.id = id


class Gym:
    def __init__(self, id, name, latitude, longitude, groups):
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.groups = groups

class Group:
    def __init__(self, id, gym, time_start, time_end, members):
        self.id = id
        self.gym = gym
        self.time_start = time_start
        self.time_end = time_end
        self.members = members
