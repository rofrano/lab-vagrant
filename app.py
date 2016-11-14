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

import os
from redis import Redis
from flask import Flask, jsonify, request

# Create Flask application
app = Flask(__name__)

# Get bindings from the environment
debug = (os.getenv('DEBUG', 'False') == 'True')
port = os.getenv('PORT', '5000')
hostname = os.getenv('HOSTNAME', '127.0.0.1')
redis_port = os.getenv('REDIS_PORT', '6379')

# Application Routes

######################################################################
# GET /
######################################################################
@app.route('/')
def index():
    hits_url = request.base_url + 'hits'
    return jsonify(name='Hit Me Service', version='1.0', url=hits_url), 200

######################################################################
# GET /hits
######################################################################
@app.route('/hits')
def hits():
    redis.incr('hit_counter')
    count = redis.get('hit_counter')
    return jsonify(hits=count), 200


######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    redis = Redis(host=hostname, port=int(redis_port))
    app.run(host='0.0.0.0', port=int(port), debug=debug)
