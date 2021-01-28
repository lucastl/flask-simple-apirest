from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost:27017/pythonapirest'

mongo = PyMongo(app)

@app.route('/users', methods=["POST"])
def create_user():
    email = request.json['email']
    password = request.json['password']

    if password and email:
        hashed_password = generate_password_hash(password)
        id = mongo.db.users.insert(
            {'email': email, 'password': hashed_password}
        )
        response = {
            'id': str(id),
            'email': email,
            'password': hashed_password
        }
        return response
    else:
        return not_found()

@app.route('/users', methods=["GET"])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application-json')

@app.route('/users/<id>', methods=["GET"])
def get_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype='application-json')

@app.route('/users/<id>', methods=["DELETE"])
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({
        'message': 'User has been deleted',
        'status': 200
    })
    return response

@app.route('/users/<id>', methods=["PUT"])
def update_user(id):
    email = request.json['email']
    password = request.json['password']
    
    if email and password:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': {
            'email': email,
            'password': hashed_password
        }})
    
    response = jsonify({
        'message': 'User updated succesfully',
        'status': 200
    })
    
    return response

@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resource not found ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True)