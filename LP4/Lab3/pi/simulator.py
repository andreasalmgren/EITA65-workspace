import math
import requests
import argparse
from sense_hat import SenseHat
from time import sleep
import pygame


sense = SenseHat() 
pygame.mixer.init()


g = (0, 255, 0)
r = (255, 0, 0)
b = (255, 255, 204)
       
greenAlien = [
g,g,g,g,g,g,g,g,
g,g,g,g,g,g,g,g,
g,g,g,g,g,g,g,g,
g,g,g,g,g,g,g,g,
g,g,g,g,g,g,g,g,
g,g,g,g,g,g,g,g,
g,g,g,g,g,g,g,g,
g,g,g,g,g,g,g,g]

redCreeper = [
r,r,r,r,r,r,r,r,
r,r,r,r,r,r,r,r,
r,r,r,r,r,r,r,r,
r,r,r,r,r,r,r,r,
r,r,r,r,r,r,r,r,
r,r,r,r,r,r,r,r,
r,r,r,r,r,r,r,r,
r,r,r,r,r,r,r,r]

steve = [
b,b,b,b,b,b,b,b,
b,b,b,b,b,b,b,b,
b,b,b,b,b,b,b,b,
b,b,b,b,b,b,b,b,
b,b,b,b,b,b,b,b,
b,b,b,b,b,b,b,b,
b,b,b,b,b,b,b,b,
b,b,b,b,b,b,b,b]

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

    ##Tar drönare från nuvarande plats till pick up uppdaterar current_coords
    draw(redCreeper)
    play("coin.wav")
    sleep(3)
    play("space-odyssey.mp3")
    partOfRun(id, current_coords, from_coords)
    
    play("doorbell.mp3")
    waiting(id)
    
    ##Tar drönare från pickup plats till drop off
    draw(redCreeper)-    play("space-odyssey.mp3")
    partOfRun(id, from_coords, to_coords)
    
    play("doorbell.mp3")
    waiting(id)

    ##Denna del sättesense.set_pixels(image)r sedan status till idle
    updateStatus(id, 'idle', current_coords)
    draw(greenAlien)

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
        print(drone_info)
        resp = session.post(SERVER_URL, json=drone_info)
        
def draw(image):
    sense.set_pixels(image)
    
def play(tune):
    pygame.mixer.music.load(tune)
    pygame.mixer.music.play()

def waiting(id):
    updateStatus(id, 'waiting', current_coords)
    sense.clear()
    draw(steve)
    joystick = " "
    while joystick is not "up":
      for event in sense.stick.get_events():
        # Check if the joystick was pressed
        if event.action == "pressed":
          # Check which direction
          if event.direction == "up":
              joystick = "up"
          # Wait a while and then clear the screen
          sleep(0.5)


if __name__ == "__main__":
    # Fill in the IP address of server, in order to location of the drone to the SERVER
    #===================================================================
    SERVER_URL = "http://192.168.0.3:5001/drone"
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
