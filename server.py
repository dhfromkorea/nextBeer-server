#!flask/bin/python
import os
from flask import Flask, jsonify, request, make_response
import string
import random

import database


try:
    from flask.ext.cors import cross_origin
except ImportError:
    from flask_cors import cross_origin

app = Flask(__name__)
# configure a default header
# we handle each route individually using @cross_origin()

# app.config['CORS_HEADERS'] = ['Content-Type']
# app.config['CORS_ORIGINS'] = ['*']


# flask url decorators
seed_list = list(string.digits + string.uppercase)
@app.route('/api/v2/user', methods=['GET'])
@cross_origin()
# @cross_origin(origin='*',headers=['Content-Type','Authorization'])
def create_new_user():
    unique_string = "".join([random.choice(seed_list) for _ in range(10)])
    database.save_new_user(unique_string)
    return jsonify({"unique_string": unique_string})

@app.route('/api/v2/<beer_id>/<rating>/<user_string>', methods = ['GET'])
@cross_origin()
def get_next_recommendation(beer_id, rating, user_string):
    user_id = database.get_userid_from_string(user_string)
    database.save_to_profile(user_id, beer_id, rating)

    recommended_beer_id = database.get_next_recommendation(user_id)

    return jsonify(database.get_metadata(recommended_beer_id))


@app.route('/api/v1/<beer_id>', methods = ['GET'])
@cross_origin()
def get_similar_beer(beer_id):
    try:
        top_beer = database.get_nearest_beers(beer_id, 1)[0]
        print top_beer
        recommended_beer_id = top_beer[1]
        return jsonify(database.get_metadata(recommended_beer_id))
    except IndexError:
        return jsonify({})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug = True)
