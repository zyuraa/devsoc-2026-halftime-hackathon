from flask import Flask, request, jsonify
from search import search_gyms
from models import Gym


def search():

    print("longitude:", longitude)
    print("latitude:", latitude)
    print("limit:", limit)
    print("radius_km:", radius_km)
    found_gyms = search_gyms(
        longitude,
        latitude,
        limit,
        radius_km
    )
    print("found_gyms:", found_gyms)

    return jsonify({"gyms": [gym.name for gym in found_gyms]})


longitude=151
latitude=-34
limit=10
radius_km=15

search()