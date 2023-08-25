#!/usr/bin/python3
"""view for Amenity objects"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/amenities', strict_slashes=False,
                 methods=['GET'])
@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def retrieve_amenity(amenity_id=None):
    """retrieve amenities objs"""
    dict_obj = storage.all(Amenity)

    if amenity_id is None:
        all_obj = [obj.to_dict() for obj in dict_obj.values()]
        return jsonify(all_obj)

    obj = storage.get(Amenity, amenity_id)

    if obj:
        obj_todict = obj.to_dict()
        return jsonify(obj_todict)
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id=None):
    """Delete an amenity """

    obj = storage.get(Amenity, amenity_id)

    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', strict_slashes=False,
                 methods=['POST'])
def add_amenity():
    """Add a new amenity"""
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')
    if not data.get('name'):
        abort(400, 'Missing Name')

    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id=None):
    """Update info about an amenity"""
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')

    obj = storage.get(Amenity, amenity_id)

    if obj:
        for key, value in data.items():
            if key not in ("id", "created_at", "updated_at"):
                setattr(obj, key, value)
        storage.save()
    else:
        abort(404)

    return jsonify(obj.to_dict()), 200