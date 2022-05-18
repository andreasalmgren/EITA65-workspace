from datetime import datetime
import qrcode, rsa, cv2
import pyzbar.pyzbar as pyzbar


# HAMTA TIDEN
now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

#GENERERA QR-KOD

with open('publicKey.txt', 'rb') as f:
    publicKey = rsa.PublicKey.load_pkcs1(f.read(), format='PEM')
print(type(publicKey))

klartext = current_time + ' ' + "Unik identifierare"
krypto = rsa.encrypt(klartext.encode(), publicKey)
print(klartext)


img = qrcode.make(str(krypto))
img.save("dd.png")

