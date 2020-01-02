# Copyright 2016, 2020 John J. Rofrano. All Rights Reserved.
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
import logging
from redis import StrictRedis
from redis.exceptions import ConnectionError
from flask import Flask, jsonify, url_for

######################################################################
# Get bindings from the environment
######################################################################
DEBUG = os.getenv("DEBUG", "False") == "True"
PORT = os.getenv("PORT", "5000")
# Get Redis ports from environment
REDIS_SERVICE_HOST = os.getenv("REDIS_SERVICE_HOST", "127.0.0.1")
REDIS_SERVICE_PORT = os.getenv("REDIS_SERVICE_PORT", "6379")


######################################################################
# Create Flask application
######################################################################
app = Flask(__name__)
app.logger.setLevel(logging.INFO)

redis = StrictRedis(
    REDIS_SERVICE_HOST, int(REDIS_SERVICE_PORT), charset="utf-8", decode_responses=True,
)

######################################################################
# Application Routes
######################################################################
@app.route("/")
def index():
    """ Returns a message about the service """
    app.logger.info("Request for Index page")
    return (
        jsonify(
            name="Hit Me Service", version="1.0", url=url_for("hits", _external=True)
        ),
        200,
    )


@app.route("/hits")
def hits():
    """ Increments the counter each time it is called """
    app.logger.info("Request to increment the counter")
    try:
        redis.incr("hit_counter")
        count = redis.get("hit_counter")
    except ConnectionError as error:
        error_message = "Cannot contact Redis service: {}".format(error)
        app.logger.error(error_message)
        return jsonify(error=error_message), 500

    app.logger.info("Counter is now %s", count)
    return jsonify(hits=count), 200


######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    app.logger.info("*" * 70)
    app.logger.info("   H I T   C O U N T E R   S E R V I C E   ".center(70, "*"))
    app.logger.info("*" * 70)
    app.run(host="0.0.0.0", port=int(PORT), debug=DEBUG)
