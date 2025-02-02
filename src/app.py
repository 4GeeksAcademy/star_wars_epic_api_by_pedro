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
from models import db, User,Planet,Favourite_list,Species,Character,FavoriteTypeEnum
from random import randint
app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#############################USERS##############################
@app.route('/user', methods=['GET'])
def get_all_users():
    user_list=User.query.all()
    
    response_body = {"content":user_list
    }

    return jsonify(response_body), 200
@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user=User.query.get(id)
    response_body = {"content":user
    }

    if user:
        return jsonify(response_body),200
    else:
        return jsonify({"error": "User not found"}), 400
@app.route('/user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()

      
        required_fields = ['name', 'password', 'email']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Requiered fields missing"}), 400

   
        existing_user = db.session.query(User).filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({"error": "Email already registered"}), 400

     
        new_user = User(
            name=data['name'],
            password=data['password'],  
            email=data['email']
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "Usuario creado con éxito",
            "user": {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email
            }
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = db.session.get(User, id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": f"User {user.name} deleted succesfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
#############################CHARACTERS##############################
@app.route('/character', methods=['GET'])
def get_all_characters():
    character_list=Character.query.all()
    
    response_body = {"content":character_list
    }

    return jsonify(response_body), 200
@app.route('/character/<int:id>', methods=['GET'])
def get_character(id):
    character=Character.query.get(id)
    response_body = {"content":character
    }

    if character:
        return jsonify(response_body),200
    else:
        return jsonify({"error": "Character not found"}), 400
@app.route('/character', methods=['POST'])
def create_character():

   
    try:
        data = request.get_json()

        required_fields = ['name', 'firstname', 'home_world', 'species']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Requiered fields missing"}), 400

        new_character = Character(
            name=data['name'],
            firstname=data['firstname'],
            home_world=data['home_world'],
            species=data['species']
        )

        db.session.add(new_character)
        db.session.commit()

        return jsonify({"message": "character created succesfully", "character": {
            "id": new_character.id,
            "name": new_character.name,
            "firstname": new_character.firstname,
            "home_world": new_character.home_world,
            "species": new_character.species
        }}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500    
@app.route('/character/<int:id>', methods=['DELETE'])
def delete_character(id):
    try:
        character = db.session.get(Character, id)
        if not character:
            return jsonify({"error": "Character not found"}), 404
        
        db.session.delete(character)
        db.session.commit()

        return jsonify({"message": f"Character {character.name} deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
#############################PLANETS##############################
@app.route('/planet', methods=['GET'])
def get_all_planets():
    planet_list=Planet.query.all()
    
    response_body = {"content":planet_list
    }

    return jsonify(response_body), 200
@app.route('/planet/<int:id>', methods=['GET'])
def get_planet(id):
    planet=Planet.query.get(id)
    response_body = {"content":planet
    }

    if planet:
        return jsonify(response_body),200
    else:
        return jsonify({"error": "Planet not found"}), 400
@app.route('/planet', methods=['POST'])
def create_planet():
    try:
        data = request.get_json()

        required_fields = ['name', 'population']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Requiered fields missing"}), 400

     
        new_planet = Planet(
            name=data['name'],
            population=data['population']
        )

        db.session.add(new_planet)
        db.session.commit()

        return jsonify({
            "message": "Planet created succesfully",
            "planet": {
                "id": new_planet.id,
                "name": new_planet.name,
                "population": new_planet.population
            }
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500    
@app.route('/planet/<int:id>', methods=['DELETE'])
def delete_planet(id):
    try:
        planet = db.session.get(Planet, id)
        if not planet:
            return jsonify({"error": "Planet not found"}), 404
        
        db.session.delete(planet)
        db.session.commit()

        return jsonify({"message": f"Planet {planet.name} deleted succesfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
#############################SPECIES##############################
@app.route('/species', methods=['GET'])
def get_all_species():
    species_list=Species.query.all()
    
    response_body = {"content":species_list
    }

    return jsonify(response_body), 200
@app.route('/species/<int:id>', methods=['GET'])
def get_species(id):
    species=Species.query.get(id)
    response_body = {"content":species
    }

    if species:
        return jsonify(response_body),200
    else:
        return jsonify({"error": "Species not found"}), 400
@app.route('/species', methods=['POST'])
def create_species():
    try:
        data = request.get_json()

       
        required_fields = ['name', 'homeworld', 'language']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing requiered fields"}), 400

     
        homeworld = db.session.get(Planet, data['homeworld'])
        if not homeworld:
            return jsonify({"error": "planet does not exist"}), 400

      
        new_species = Species(
            name=data['name'],
            homeworld=data['homeworld'],
            language=data['language']
        )

        db.session.add(new_species)
        db.session.commit()

        return jsonify({
            "message": "Especie creada con éxito",
            "species": {
                "id": new_species.id,
                "name": new_species.name,
                "homeworld": new_species.homeworld,
                "language": new_species.language
            }
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/species/<int:id>', methods=['DELETE'])
def delete_species(id):
    try:
        species = db.session.get(Species, id)
        if not species:
            return jsonify({"error": "Species not found"}), 404
        
        db.session.delete(species)
        db.session.commit()

        return jsonify({"message": f"Species {species.name} deleted succesfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
############################FAVORITE LIST########################
@app.route('/favourite_lists', methods=['GET'])
def get_all_favourites():
    try:
        favourite_lists = Favourite_list.query.all()
        if not favourite_lists:
            return jsonify({"message": "Not lists available"}), 404
        
        result = [{
            "id": fav.id,
            "user_id": fav.user_id,
            "external_id": fav.external_id,
            "name": fav.name,
            "type": fav.type.value 
        } for fav in favourite_lists]
        
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/favourite_lists/<int:id>', methods=['GET'])
def get_favourite(id):
    try:
        favourite = Favourite_list.query.get(id)
        if not favourite:
            return jsonify({"error": "list not found"}), 404
        
        return jsonify({
            "id": favourite.id,
            "user_id": favourite.user_id,
            "external_id": favourite.external_id,
            "name": favourite.name,
            "type": favourite.type.value  
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/favourite_lists', methods=['POST'])
def add_favourite():
    try:
        data = request.get_json()

        required_fields = ['user_id', 'external_id', 'name', 'type']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

     
        if data['type'] not in [e.name for e in FavoriteTypeEnum]:
            return jsonify({"error": "invalid type"}), 400
        
  
        new_favourite = Favourite_list(
            user_id=data['user_id'],
            external_id=data['external_id'],
            name=data['name'],
            type=FavoriteTypeEnum[data['type']] 
        )

        db.session.add(new_favourite)
        db.session.commit()

        return jsonify({
            "message": "list created succesfully",
            "favourite": {
                "id": new_favourite.id,
                "user_id": new_favourite.user_id,
                "external_id": new_favourite.external_id,
                "name": new_favourite.name,
                "type": new_favourite.type.value
            }
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/favourite_lists/<int:id>', methods=['DELETE'])
def delete_favourite(id):
    try:
        favourite = Favourite_list.query.get(id)
        if not favourite:
            return jsonify({"error": "List not found"}), 404
        
        db.session.delete(favourite)
        db.session.commit()

        return jsonify({"message": f"List {favourite.name} deleted succesfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


