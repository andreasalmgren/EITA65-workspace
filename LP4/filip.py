import rsa, cv2, qrcode
from datetime import datetime

publicKey, privateKey = rsa.newkeys(1024)


print(publicKey)
print(privateKey)

# HÄMTA TIDEN
now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

#GENERERA QR-KOD
ID = 'Filips Personnummer'
krypto = str(current_time) + ' ' + ID
krypto = rsa.encrypt(krypto.encode(), publicKey)

img = qrcode.make(krypto)

img.save("testKrypto.png")



def displayBbox(im, bbox):
    if bbox is not None:
        bbox = [bbox[0].astype(int)]
        n = len(bbox[0])
        for i in range(n):
            cv2.line(im, tuple(bbox[0][i]), tuple(bbox[0][(i+1) % n]), (0,255,0), 3)

if __name__ == '__main__':
    img = cv2.imread('testKrypto.png')
    detector = cv2.QRCodeDetector()
    res, points, _ = detector.detectAndDecode(img)
    # Detected outputs.
    if len(res) > 0:
        print('Output : ', res)
        print('Bounding Box : ', points)
        displayBbox(img, points)
        decMessage = rsa.decrypt(res, privateKey).decode()
        print("decrypted string: ", decMessage)
    else:
        print('QRCode not detected')

cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

