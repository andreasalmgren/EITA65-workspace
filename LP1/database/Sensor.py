from sense_hat import SenseHat
from time import sleep
import redis

sense = SenseHat()

#set up two databases
#r_conn = redis.Redis(host='localhost', port=6379, db = 0)
#r_conn1 = redis.Redis(host='localhost', port=6379, db = 1)

#r_conn1 = redis.Redis(host='127.0.0.1', port=6379, charset='utf-8')

r_conn1 = redis.Redis(host='34.88.44.178', port=7777, charset='utf-8', decode_responses = True)
r_conn = redis.Redis(host='34.88.44.178', port=7777, charset='utf-8', decode_responses = True)

while True:
  for event in sense.stick.get_events():
    # Check if the joystick was pressed
    if event.action == "pressed":
 
      # Check which direction, store in database under key and print StdOut val
      if event.direction == "up":
        r_conn.set("dir", "North")
        value = r_conn.get('dir').decode() 
        print('\n', value)
      elif event.direction == "down":
        r_conn.set("dir", "South")
        value = r_conn.get('dir').decode() 
        print('\n', value)
      elif event.direction == "left": 
        r_conn.set("dir", "West")
        value = r_conn.get('dir').decode() 
        print('\n', value)  
      elif event.direction == "right":
        r_conn.set("dir", "East")
        value = r_conn.get('dir').decode() 
        print('\n', value)
      elif event.direction == "middle":
        r_conn.set("dir", "middle")
        value = r_conn.get('dir').decode() 
        print('\n', value)  
  
  temp = round(sense.get_temperature())
  r_conn1.set("temp", temp)
  print('\n', temp)
  sleep(0.4)
