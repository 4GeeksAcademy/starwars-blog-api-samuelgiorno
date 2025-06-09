"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, FavouritePlanet, FavouritePeople
from sqlalchemy import select
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def handle_users():

    all_users = db.session.execute(select(User)).scalars().all()
    all_users = list(map(lambda user: user.serialize(), all_users))

    response_body = {
        "Users": all_users
    }

    return jsonify(response_body), 200


@app.route('/peoples', methods=['GET'])
def handle_people():

    all_people = db.session.execute(select(People)).scalars().all()
    all_people = list(map(lambda people: people.serialize(), all_people))

    response_body = {
        "People": all_people
    }
    return jsonify(response_body), 200


@app.route('/peoples/<int:people_id>', methods=['GET'])
def handle_people_for_id(people_id):
    people = db.session.get(People, people_id)
    if people is None:
        return jsonify({"error": "Person not found"}), 404
    response_body = {
        "People": people.serialize()
    }
    return jsonify(response_body), 200


@app.route('/peoples', methods=['POST'])
def handle_create_people():
    body = request.get_json()
    if not body:
        return jsonify({"error": "Request body must be JSON"}), 400

    required_fields = ['name', 'age', 'gender',
                       'height', 'weight', 'image', 'planet_of_birth']
    missing_fields = [field for field in required_fields if field not in body]

    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400
    people = People()
    people.name = body['name']
    people.age = body['age']
    people.gender = body['gender']
    people.height = body['height']
    people.weight = body['weight']
    people.image = body['image']
    people.planet_of_birth = body['planet_of_birth']

    db.session.add(people)
    db.session.commit()
    return jsonify({"ok": "Person add to list of people"}), 201


@app.route('/peoples/<int:people_id>', methods=['PUT'])
def handle_edit_people(people_id):

    body = request.get_json()

    if not body:
        return jsonify({"error": "Request body must be JSON"}), 400
    people_exist = select(People).where(People.id == people_id)
    person = db.session.execute(people_exist).scalar_one_or_none()

    if person is None:
        return jsonify({"error": "Person not found"}), 404
    if 'name' in body:
        person.name = body['name']
    if 'age' in body:
        person.age = body['age']
    if 'gender' in body:
        person.gender = body['gender']
    if 'height' in body:
        person.height = body['height']
    if 'weight' in body:
        person.weight = body['weight']
    if 'image' in body:
        person.image = body['image']
    if 'planet_of_birth' in body:
        person.planet_of_birth = body['planet_of_birth']

    db.session.commit()

    return jsonify({"message": "Person updated successfully"}), 200


@app.route('/peoples/<int:people_id>', methods=['DELETE'])
def handle_delete_people(people_id):
    people = db.session.get(People, people_id)

    if people is None:
        return jsonify({"error": "Favorite planpeoplet not found"}), 404

    db.session.delete(people)
    db.session.commit()

    return jsonify({"message": "People deleted"}), 200


@app.route('/planets', methods=['GET'])
def handle_planet():

    all_planets = db.session.execute(select(Planets)).scalars().all()
    all_planets = list(map(lambda planets: planets.serialize(), all_planets))

    response_body = {
        "Planets": all_planets
    }
    return jsonify(response_body), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_planet_for_id(planet_id):
    planet = db.session.get(Planets, planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    response_body = {
        "Planet": planet.serialize()
    }
    return jsonify(response_body), 200


@app.route('/planets', methods=['POST'])
def handle_create_planet():
    body = request.get_json()
    if not body:
        return jsonify({"error": "Request body must be JSON"}), 400

    required_fields = ['name', 'description',
                       'galaxy', 'population', 'gravity', 'image']
    missing_fields = [field for field in required_fields if field not in body]

    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    planet = Planets()
    planet.name = body['name']
    planet.description = body['description']
    planet.galaxy = body['galaxy']
    planet.population = body['population']
    planet.gravity = body['gravity']
    planet.image = body['image']

    db.session.add(planet)
    db.session.commit()

    return jsonify({"ok": "Planet add to Planets"}), 201


@app.route('/planets/<int:planet_id>', methods=['PUT'])
def handle_edit_planet(planet_id):
    body = request.get_json()
    if not body:
        return jsonify({"error": "Request body must be JSON"}), 400

    planet_exist = select(Planets).where(Planets.id == planet_id)
    planet = db.session.execute(planet_exist).scalar_one_or_none()

    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    if 'name' in body:
        planet.name = body['name']
    if 'description' in body:
        planet.description = body['description']
    if 'galaxy' in body:
        planet.galaxy = body['galaxy']
    if 'population' in body:
        planet.population = body['population']
    if 'image' in body:
        planet.image = body['image']

    db.session.commit()

    return jsonify({"message": "Planet updated successfully"}), 200


@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def handle_delete_planet(planet_id):
    planet = db.session.get(Planets, planet_id)
    if planet is None:
        return jsonify({"error": "Planet ID not found"}), 404

    fav_exists = db.session.execute(
        select(FavouritePlanet).where(FavouritePlanet.planet_id == planet_id)
    ).first()

    people_exist = db.session.execute(
        select(People).where(People.planet_of_birth == planet_id)
    ).first()

    if fav_exists or people_exist:
        return jsonify({"error": "Cannot delete planet with relationships"}), 400

    db.session.delete(planet)
    db.session.commit()

    return jsonify({"message": "Planet deleted successfully"}), 200


@app.route('/favoritePlanet/<int:user_id>', methods=['GET'])
def handle_favorite_by_user(user_id):
    all_favorite_planets = db.session.execute(
        select(FavouritePlanet).where(FavouritePlanet.user_id == user_id)
    ).scalars().all()
    all_favorite_planets = list(
        map(lambda favorite: favorite.serialize(), all_favorite_planets))

    response_body = {
        "FavoritePlanets": all_favorite_planets
    }
    print(all_favorite_planets)
    return jsonify(response_body), 200


@app.route('/favoritePlanet/<int:user_id>', methods=['POST'])
def handle_add_favorite_planet(user_id):
    body = request.get_json()

    if not body:
        return jsonify({"error": "Request body must be JSON"}), 400

    required_fields = ['planet_id', 'user_id']
    missing_fields = [field for field in required_fields if field not in body]

    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    if user_id != body['user_id']:
        return jsonify({"error": "User ID in URL and body do not match"}), 400

    existing_favorite = db.session.execute(
        select(FavouritePlanet).where(
            (FavouritePlanet.user_id == body['user_id']) &
            (FavouritePlanet.planet_id == body['planet_id'])
        )
    ).scalar_one_or_none()

    if existing_favorite:
        return jsonify({"message": "Planet already marked as favorite"}), 200

    favoritePlanet = FavouritePlanet()
    favoritePlanet.planet_id = body['planet_id']
    favoritePlanet.user_id = body['user_id']
    db.session.add(favoritePlanet)

    db.session.commit()
    return jsonify({"message": "Favorite planet added successfully"}), 201


@app.route('/favoritePlanet/<int:planet_id>/<int:user_id>', methods=['DELETE'])
def handle_delete_by_user(user_id, planet_id):

    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"error": " The id of user not exist"}), 404

    search_fav = select(FavouritePlanet).where(
        FavouritePlanet.user_id == user_id,
        FavouritePlanet.planet_id == planet_id
    )
    fav_result = db.session.execute(search_fav).scalar_one_or_none()
    if fav_result is None:
        return jsonify({"error": "Favorite planet not found"}), 404

    db.session.delete(fav_result)
    db.session.commit()

    return jsonify({"message": "Favorite planet deleted"}), 200


@app.route('/favoritePeople/<int:user_id>', methods=['GET'])
def handle_favorite_people_by_user(user_id):
    favorite_people = db.session.execute(
        select(FavouritePeople).where(FavouritePeople.user_id == user_id)
    ).scalars().all()
    favorite_people = list(
        map(lambda favorite: favorite.serialize(), favorite_people))

    response_body = {
        "Favorite_people": favorite_people
    }
    print(favorite_people)
    return jsonify(response_body), 200


@app.route('/favoritePeople/<int:user_id>', methods=['POST'])
def handle_add_favorite_people(user_id):
    body = request.get_json()

    if not body:
        return jsonify({"error": "Request body must be JSON"}), 400

    required_fields = ['people_id', 'user_id']
    missing_fields = [field for field in required_fields if field not in body]

    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400
    if user_id != body['user_id']:
        return jsonify({"error": "User ID in URL and body do not match"}), 400

    existing_favorite = db.session.execute(
        select(FavouritePeople).where(
            (FavouritePeople.user_id == body['user_id']) &
            (FavouritePeople.people_id == body['people_id'])
        )
    ).scalar_one_or_none()

    if existing_favorite:
        return jsonify({"message": "People already marked as favorite"}), 200

    favoritePeople = FavouritePeople()
    favoritePeople.people_id = body['people_id']
    favoritePeople.user_id = body['user_id']

    db.session.add(favoritePeople)
    db.session.commit()
    return jsonify({"message": "Favorite people added successfully"}), 201


@app.route('/favoritePeople/<int:user_id>/<int:people_id>', methods=['DELETE'])
def handle_delete_fav_by_user(user_id, people_id):

    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"error": " The id of user not exist"}), 404
    people = db.session.get(People, people_id)
    if people is None:
        return jsonify({"error": "The id of people not exist"}), 404

    search_fav = select(FavouritePeople).where(
        FavouritePeople.user_id == user_id,
        FavouritePeople.people_id == people_id
    )
    fav_result = db.session.execute(search_fav).scalar_one_or_none()
    if fav_result is None:
        return jsonify({"error": "Favorite planet not found"}), 404

    db.session.delete(fav_result)
    db.session.commit()

    return jsonify({"message": "Favorite people deleted"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
