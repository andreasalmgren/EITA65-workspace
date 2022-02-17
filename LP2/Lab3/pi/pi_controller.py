import math
import requests
import argparse

#from webserver.database import drone


#Write you own function that moves the dr1 from one place to another 
#the function returns the drone's current location while moving
#====================================================================================================
def your_function(current_coords, destination_coords):
    v = math.atan2((destination_coords[1] - current_coords[1]), (destination_coords[0] - current_coords[0]))
    print((destination_coords[0] - current_coords[0]), (destination_coords[1] - current_coords[1]))
    print("steps left: " + str(int(math.sqrt((current_coords[0] - destination_coords[0])**2 + (current_coords[1] - destination_coords[1])**2) * 10000) + 1))
    print(current_coords)
    print(destination_coords)
    if math.sqrt((current_coords[0] - destination_coords[0])**2 + (current_coords[1] - destination_coords[1])**2) < 0.0001:
        longitude = destination_coords[0]
        latitude = destination_coords[1]
    else:
        longitude = current_coords[0] + 0.0001 * math.cos(v) #13.21008
        latitude = current_coords[1] + 0.0001 * math.sin(v) #55.71106
    return longitude, latitude
#====================================================================================================


def run(current_coords, from_coords, to_coords, SERVER_URL):
    drone_coords = current_coords
    # Complete the while loop:
    # 1. Change the loop condition so that it stops sending location to the database 
    #    when the drone arrives the to_address
    # 2. Plan a path with your own function, so that the drone moves from [current_address] to 
    #    [from_address], and the from [from_address] to [to_address]. 
    # 3. While moving, the drone keeps sending it's location to the database. Consider the moveDrone() 
    #    function we used in the previous instruction parts.
    #====================================================================================================
    while drone_coords != from_coords:
        print("we movin' bois")
        drone_coords = your_function(drone_coords, from_coords)
        with requests.Session() as session:
            drone_location = {'longitude': drone_coords[0],
                              'latitude': drone_coords[1]
                        }
            resp = session.post(SERVER_URL, json=drone_location)
    #Drone is at from
    while drone_coords != to_coords:
        print("we movin' bois")
        drone_coords = your_function(drone_coords, to_coords)
        with requests.Session() as session:
            drone_location = {'longitude': drone_coords[0],
                              'latitude': drone_coords[1]
                        }
            resp = session.post(SERVER_URL, json=drone_location)
  #====================================================================================================

   
if __name__ == "__main__":
    SERVER_URL = "http://127.0.0.1:5001/drone"

    parser = argparse.ArgumentParser()
    parser.add_argument("--clong", help='current longitude of drone location' ,type=float)
    parser.add_argument("--clat", help='current latitude of drone location',type=float)
    parser.add_argument("--flong", help='longitude of input [from address]',type=float)
    parser.add_argument("--flat", help='latitude of input [from address]' ,type=float)
    parser.add_argument("--tlong", help ='longitude of input [to address]' ,type=float)
    parser.add_argument("--tlat", help ='latitude of input [to address]' ,type=float)
    args = parser.parse_args()

    current_coords = (args.clong, args.clat)
    from_coords = (args.flong, args.flat)
    to_coords = (args.tlong, args.tlat)

    print(current_coords)
    print(from_coords)
    print(to_coords)

    run(current_coords, from_coords, to_coords, SERVER_URL)
