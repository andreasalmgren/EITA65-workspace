from datetime import datetime
import qrcode, rsa, cv2
import pyzbar.pyzbar as pyzbar


# HAMTA TIDEN
now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print(type(current_time))
print("Current Time =", current_time)

#GENERERA QR-KOD

with open('publicKey.txt', 'rb') as f:
    publicKey = rsa.PublicKey.load_pkcs1(f.read(), format='PEM')
print(type(publicKey))

klartext = current_time + ' ' + "Person som har köpt saker"
klartext = "15:40:00 Unik identifierare"

krypto = rsa.encrypt(klartext.encode(), publicKey)
print(str(krypto))


img = qrcode.make(str(krypto))
img.save("SkapadQR.png")

cv2.imshow("SkapadQR.png", cv2.imread("SkapadQR.png"))
cv2.waitKey(0)
cv2.destroyAllWindows()

