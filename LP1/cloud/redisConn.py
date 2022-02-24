import redis

# create the redis connection(s)
# You can set the number of databases in the redis.config file to the number you want and then select the dbid between 0 and 'databases'-1

r_conn = redis.Redis(host='34.88.44.178', port=7777)

# create a key-value pair with key as name and value as "amalgjose"
r_conn.set('name', 'amalgjose')

# retrieve the value(s) by using the key(s)
value0 = r_conn.get('name').decode() # decode() method: convert byte object into string object
print("Value from Redis -->", value0)




