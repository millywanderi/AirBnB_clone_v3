#!/usr/bin/python3
"""Places Views"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.place import Place
from models.city import City
from models.user import User
from flask import abort
from flask import make_response
from flask import request


@app_views.route('cities/<city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retuens places according to id of city obj
    or 404 error
    """
    if city_id:
        dic_city = storage.get(City, city_id)
        if dic_city is None:
            abort(404)
        else:
            places = storage.all(Place).values()
            list_places = []
            for place in places:
                if place.city_id == city_id:
                    list_places.append(place.to_dict())
            return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Return place according class and id of the place
    otherwise 404 error
    """
    if place_id:
        dic_place = storage.get(Place, place_id)
        if dic_place is None:
            abort(404)
        else:
            return jsonify(dic_place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes an obj place if it exists
    otherwise return 404 error
    """
    if place_id:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        else:
            storage.delete(place)
            storage.save()
            return make_response(jsonify({}), 200)


@app_views.route('cities/<city_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Create a new place, otherwise raise 404 error if name exists"""
    if city_id:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    reque = request.get_json()

    if "user_id" not in reque:
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    user = storage.get(User, reque['user_id'])
    if user is None:
        abort(404)

    if "name" not in reque:
        return make_response(jsonify({"error": "Missing name"}), 400)
    reque['city_id'] = city_id
    places = Place(**reque)
    places.save()
    return make_response(jsonify(places.to_dict()), 201)


@app_views.route('places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates attributes from a place obj"""
    if place_id:
        places_obj = storage.get(Place, place_id)
        if places_obj is None:
            abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    reque = request.get_json()
    for key, value in reque.items():
        if key not in [
            'id',
            'user_id',
            'city_id',
            'created_at',
                'updated_at']:
            setattr(places_obj, key, value)
    places_obj.save()
    return make_response(jsonify(places_obj.to_dict()), 200)
