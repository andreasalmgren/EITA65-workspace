import math, requests, argparse, pygame, rsa, cv2, re
import pyzbar.pyzbar as pyzbar
from picamera import PiCamera
from time import sleep
from datetime import datetime



with open('privateKey.txt', 'rb') as f:
    privateKey = rsa.PrivateKey.load_pkcs1(f.read(), format='PEM')
print(type(privateKey))

camera = PiCamera()
pygame.mixer.init()
customer = 'Person som har köpt saker'




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

    sleep(3)
    ##play("space-odyssey.mp3")
    partOfRun(id, current_coords, from_coords)
    
    ##play("doorbell.mp3")
    waiting(id)
    
    ##Tar drönare från pickup plats till drop off
    ##play("space-odyssey.mp3")
    partOfRun(id, from_coords, to_coords)
    
    ##play("doorbell.mp3")
    waiting(id)

    #Här vill vi har vår check funktion vi kanske måste skriva om delarna som använder sensehat :s
    check()

    ##Denna del sätter sedan status till idle
    updateStatus(id, 'idle', current_coords)

    ##Denna flyttar drönare från a till b och kallar på updateStatus under tiden
    def convert(time_to_convert):
        ftr = [3600, 60, 1]
        return sum([a * b for a, b in zip(ftr, map(int, time_to_convert.split(':')))])

    return current_coords[0], current_coords[1]

def check():
    countdown = 5
    confirmedUser = False
    camera.start_preview()
    while (countdown is not 0 and not confirmedUser):
        filePath = '/home/pi/diggi/EITA65-workspace/LP4/bilder/test1.jpg'
        camera.capture(filePath)
        img = cv2.imread(filePath)
        detector = cv2.QRCodeDetector()
        isthere, points = detector.detect(img)
        if isthere:
            decMessage = ""
            try:
                res = bytes(pyzbar.decode(img)[0].data.decode('unicode_escape')[2:-1], encoding="raw_unicode_escape")
                decMessage = rsa.decrypt(res, privateKey).decode()
                tid = decMessage[:7]
                time_from_pi = convert(tid)
                time_from_drone = convert(datetime.now().strftime("%H:%M:%S"))

                if (abs(time_from_pi - time_from_drone) < 180) or (abs(time_from_pi - time_from_drone - 86400) < 180) or (abs(time_from_pi - time_from_drone + 86400) < 180):
                    if decMessage[9:] == customer:
                        confirmedUser = True
                    else:
                        print("fel användare")
                else:
                    print("gammal QR-kod")
            except:
                print("Detta verkar inte vara en korrekt krypterad QR-kod")

        else:
            print("ser ingen QR-kod")
            #Här behövs try och catches samt en koll av tid och massa formatering och skit
        countdown -= 1
    camera.stop_preview()
    if confirmedUser:
        print("\nLämnar ut paket!")
    else:
        print("\nLämnar inte ut paket")





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

def play(tune):
    pygame.mixer.music.load(tune)
    pygame.mixer.music.play()

def waiting(id):
    updateStatus(id, 'waiting', current_coords)


if __name__ == "__main__":
    # Fill in the IP address of server, in order to location of the drone to the SERVER
    #===================================================================
    SERVER_URL = "http://192.168.0.2:5001/drone"
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
