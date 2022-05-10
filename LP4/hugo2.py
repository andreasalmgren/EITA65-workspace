import qrcode, cv2
import pyzbar.pyzbar as pyzbar

img = cv2.imread('testKrypto30.png')

print((pyzbar.decode(img)[0].data))
