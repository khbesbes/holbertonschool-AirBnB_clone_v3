#!/usr/bin/python3
"""City objects that handles all default API"""
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def retrieve_cities_stateid(state_id=None):
    """retrieve cities obj"""

    obj_state = storage.get(State, state_id)

    if obj_state:
        cities = []
        for city in obj_state.cities:
            cities.append(city.to_dict())
        return jsonify(cities)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET'])
def retrieve_cities(city_id):
    """retreve city given an ID"""

    obj = storage.get(City, city_id)

    if obj:
        obj_todic = obj.to_dict()
        return jsonify(obj_todic), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    """Delete a city"""

    obj = storage.get(City, city_id)

    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def add_city(state_id=None):
    """Add a city"""

    obj_state = storage.get(State, state_id)
    if obj_state is None:
        abort(404)

    try:
        data = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')
    if not data.get('name'):
        abort(400, 'Missing Name')

    new_city = City(state_id=state_id, **data)
    storage.new(new_city)
    storage.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['PUT'])
def update_city(city_id=None):
    """Update info of city"""
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')

    obj = storage.get(City, city_id)

    if obj:
        for key, value in data.items():
            if key not in ("id", "created_at", "updated_at"):
                setattr(obj, key, value)
        storage.save()
    else:
        abort(404)

    return jsonify(obj.to_dict()), 200

