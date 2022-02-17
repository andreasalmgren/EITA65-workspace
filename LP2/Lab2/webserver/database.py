from flask import Flask, request
from flask_cors import CORS
import redis

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

# change this to connect to your redis server
# ===============================================
redis_server = redis.Redis(host='localhost', port=5002, charset='utf-8', decode_responses=True)
# ===============================================

redis_server.set('longitude', 13.21008)
redis_server.set('latitude', 55.71106)

#write your own movedrone fuction here, this function shoud
# 1. get the lastest longitude and latitude data
# 2. update longitude and latitude values with input movement data
# 3. write the updated data to the database
# ===============================================
def moveDrone(d_long, d_la):
    longitude = redis_server.get("longitude")
    latitude = redis_server.get("latitude")
    
    redis_server.set("longitude", float(longitude) + d_long)
    redis_server.set("latitude", float(latitude) + d_la)
    
# ===============================================

@app.route('/drone', methods=['POST'])
def drone():
    movement = request.get_json()
    d_long = movement['longitude']/10000
    d_la = movement['latitude']/10000
    moveDrone(d_long, d_la)
    return 'Get data'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5002')
