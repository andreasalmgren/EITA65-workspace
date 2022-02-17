from os import fdopen
from flask import Flask, render_template, request
from flask.json import jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import time
import redis
import pickle
import json

from database import drone

app = Flask(__name__)
CORS(app)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

# change this so that you can connect to your redis server
# ===============================================
redis_server = redis.Redis(host = 'localhost', port = 6379, decode_responses=True, charset="unicode_escape")
# ===============================================

drones = [['192.168.0.1', '1', 13.21002, 55.71106, 'busy'],
          ['192.168.0.2', '2', 13.21002, 55.71500, 'idle'],
          ['192.168.0.3', '3', 13.21002, 55.71190, 'busy'],
          ['192.168.0.4', '4', 13.21002, 55.71109, 'idle'],
          ['192.168.0.5', '5', 13.21002, 55.71110, 'busy']
          ]

for i in drones:
    redis_server.set('droneIP' + i[1], i[0])
    redis_server.set('longitude' + i[1], i[2])
    redis_server.set('latitude' + i[1], i[3])
    redis_server.set('status'+ i[1], i[4])

"""
redis_server.set('longitude4', 13.21002)
redis_server.set('latitude4', 55.71106)
redis_server.set('longitude2', 13.21005)
redis_server.set('latitude2', 55.71106)
redis_server.set('status2', 'idle')
redis_server.set('status4', 'idle')
redis_server.set('droneIP2', '192.168.0.2')
redis_server.set('droneIP4', '192.168.0.4')
"""



# Translate OSM coordinate (longitude, latitude) to SVG coordinates (x,y).
# Input coords_osm is a tuple (longitude, latitude).
def translate(coords_osm):
    x_osm_lim = (13.143390664, 13.257501336)
    y_osm_lim = (55.678138854000004, 55.734680845999996)

    x_svg_lim = (212.155699, 968.644301)
    y_svg_lim = (103.68, 768.96)

    x_osm = coords_osm[0]
    y_osm = coords_osm[1]

    x_ratio = (x_svg_lim[1] - x_svg_lim[0]) / (x_osm_lim[1] - x_osm_lim[0])
    y_ratio = (y_svg_lim[1] - y_svg_lim[0]) / (y_osm_lim[1] - y_osm_lim[0])
    x_svg = x_ratio * (x_osm - x_osm_lim[0]) + x_svg_lim[0]
    y_svg = y_ratio * (y_osm_lim[1] - y_osm) + y_svg_lim[0]

    return x_svg, y_svg

@app.route('/', methods=['GET'])
def map():
    return render_template('index.html')

@app.route('/get_drones', methods=['GET'])
def get_drones():
    #=============================================================================================================================================
    # Get the information of all the drones from redis server and update the dictionary `drone_dict' to create the response
    drone_dict = {}
    for i in drones:
        drones_longitude_osm = float(redis_server.get('longitude' + i[1]))
        drones_latitude_osm = float(redis_server.get('latitude' + i[1]))
        drones_status = redis_server.get('status' + i[1])
        drones_longitude_svg, drones_latitude_svg = translate([drones_longitude_osm, drones_latitude_osm])
        drone_dict[i[1]] = {'longitude': drones_longitude_svg, 'latitude': drones_latitude_svg, 'status': drones_status}
        
    #use function translate() to covert the coodirnates to svg coordinates
    #=============================================================================================================================================
    return jsonify(drone_dict)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000')
