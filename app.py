# Copyright 2016 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Hit Me Service

Example used to show how easy it is to create a simple microservice
using Python and Flask that leverages a Redis database
"""

import os
from redis import Redis
from flask import Flask, jsonify, request, url_for

# Create Flask application
app = Flask(__name__)

# Get bindings from the environment
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')
HOSTNAME = os.getenv('HOSTNAME', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')

# Application Routes

@app.route('/')
def index():
    """ Returns a message about the service """
    return jsonify(name='Hit Me Service',
                   version='1.0',
                   url=url_for('hits', _external=True)
                  ), 200

@app.route('/hits')
def hits():
    """ Increments the counter each time calls """
    redis.incr('hit_counter')
    count = redis.get('hit_counter')
    return jsonify(hits=count), 200


######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    print "============================================"
    print "   H I T   C O U N T E R   S E R V I C E "
    print "============================================"
    redis = Redis(host=HOSTNAME, port=int(REDIS_PORT))
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
