import redis

# create the redis connection(s)
# You can set the number of databases in the redis.config file to the number you want and then select the dbid between 0 and 'databases'-1

r_conn0 = redis.Redis(host='localhost', port=6379, db = 0)

r_conn1 = redis.Redis(host='localhost', port=6379, db = 1)

# create a key-value pair with key as name and value as "amalgjose"
r_conn0.set('name', 'amalgjose')
r_conn0.set('2', 'amalgjosediff')

r_conn1.set('1', 'test')


# retrieve the value(s) by using the key(s)
value0 = r_conn0.get('name').decode() # decode() method: convert byte object into string object
print("Value from Redis -->", value0)

value0 = r_conn0.get('2').decode() # decode() method: convert byte object into string object
print("Value from Redis -->", value0)

value1 = r_conn1.get('1').decode() 
print("Value from Redis -->", value1)



