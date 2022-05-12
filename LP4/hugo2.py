import qrcode, cv2
import pyzbar.pyzbar as pyzbar

img = cv2.imread('test35.jpg')

# print(pyzbar.decode(img))
#print((pyzbar.decode(img)[0].data))

res = bytes(pyzbar.decode(img)[0].data.decode('unicode_escape')[2:-1], encoding="raw_unicode_escape")
print(res)