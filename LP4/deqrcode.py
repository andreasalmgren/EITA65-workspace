import cv2, rsa
import pyzbar.pyzbar as pyzbar

def displayBbox(im, bbox):
    if bbox is not None:
        bbox = [bbox[0].astype(int)]
        n = len(bbox[0])
        for i in range(n):
            cv2.line(im, tuple(bbox[0][i]), tuple(bbox[0][(i+1) % n]), (0,255,0), 3)

if __name__ == '__main__':
    img = cv2.imread('testKrypto2.png')
    detector = cv2.QRCodeDetector()
    print(pyzbar.decode(img))
    res = (pyzbar.decode(img)[0].data)

    isthere, points = detector.detect(img)
    #res = detector.decode(img, points)
    #res, points, _ = detector.detectAndDecode(img)
    # Detected outputs.
    #print(detector.detectAndDecode(img))


    if res:
        print('Output : ', res)
        print('Bounding Box : ', points)
        displayBbox(img, points)
        # print((krypto))
        # print((pyzbar.decode(img)[0].data).decode())
        # print(bytes(pyzbar.decode(img)[0].data.decode('unicode_escape')[2:-1], encoding="raw_unicode_escape"))
        # print(type(krypto))
        # print(type(bytes(pyzbar.decode(img)[0].data.decode('unicode_escape')[2:-1], encoding="raw_unicode_escape")))
        # print("test over")
        # print(bytes(pyzbar.decode(img)[0].data.decode('unicode_escape')[2:-1], encoding="raw_unicode_escape") == krypto )
        res = bytes(pyzbar.decode(img)[0].data.decode('unicode_escape')[2:-1], encoding="raw_unicode_escape")
        decMessage = rsa.decrypt(res, privateKey).decode()
        print("decrypted string: ", decMessage)
    else:
        print('QRCode not detected')

cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()