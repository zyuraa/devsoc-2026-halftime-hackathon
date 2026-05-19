from flask import Flask, request, jsonify

class User:
  def __init__(self, id, name, password, age, gender):
    self.id = id
    self.name = name
    self.password = password
    self.age = age
    self.gender = gender
  
  def