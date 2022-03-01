import math
import requests
import argparse

def getMovement(src, dst):
    speed = 0.00001
    dst_x, dst_y = dst
    x, y = src
    direction = math.sqrt((dst_x - x)**2 + (dst_y - y)**2)
    longitude_move = speed * ((dst_x - x) / direction )
    latitude_move = speed * ((dst_y - y) / direction )
    return longitude_move, latitude_move

def moveDrone(src, d_long, d_la):
    x, y = src
    x = x + d_long
    y = y + d_la        
    return (x, y)

    ##Denna funktion kallar på andra funktioner för att flytta drönarna och uppdatera status
def run(id, current_coords, from_coords, to_coords, SERVER_URL):

    ##Tar drönare från nuvarande plats till pick up uppdaterar current_coords (hoppas jag)
    partOfRun(id, current_coords, from_coords)

    ##Tar drönare från pickup plats till drop off
    partOfRun(id, current_coords, to_coords)

    ##Denna del sätter sedan status till idle
    updateStatus(id, 'idle', current_coords)

    return current_coords[0], current_coords[1]

    ##Denna flyttar drönare från a till b och kallar på updateStatus under tiden
def partOfRun(id, current, finnish):
    d_long, d_la = getMovement(current, finnish)
    while ((finnish[0] - current[0]) ** 2 + (finnish[1] - current[1]) ** 2) * 10 ** 6 > 0.0002:
        current = moveDrone(current, d_long, d_la)
        updateStatus(id, 'busy', current)


    ##Denna uppdaterar hemsidans koordinater och status på drönare
def updateStatus(id, status, current_coords):
    with requests.Session() as session:
        drone_info = {'id': id,
                      'longitude': current_coords[0],
                      'latitude': current_coords[1],
                      'status': status
                      }
        resp = session.post(SERVER_URL, json=drone_info)

if __name__ == "__main__":
    # Fill in the IP address of server, in order to location of the drone to the SERVER
    #===================================================================
    SERVER_URL = "http://192.168.0.3:6379/drone"
    #===================================================================

    parser = argparse.ArgumentParser()
    parser.add_argument("--clong", help='current longitude of drone location' ,type=float)
    parser.add_argument("--clat", help='current latitude of drone location',type=float)
    parser.add_argument("--flong", help='longitude of input [from address]',type=float)
    parser.add_argument("--flat", help='latitude of input [from address]' ,type=float)
    parser.add_argument("--tlong", help ='longitude of input [to address]' ,type=float)
    parser.add_argument("--tlat", help ='latitude of input [to address]' ,type=float)
    parser.add_argument("--id", help ='drones ID' ,type=str)
    args = parser.parse_args()

    current_coords = (args.clong, args.clat)
    from_coords = (args.flong, args.flat)
    to_coords = (args.tlong, args.tlat)

    print(current_coords, from_coords, to_coords)
    drone_long, drone_lat = run(args.id ,current_coords, from_coords, to_coords, SERVER_URL)
    # drone_long and drone_lat is the final location when drlivery is completed, find a way save the value, and use it for the initial coordinates of next delivery
    #=============================================================================