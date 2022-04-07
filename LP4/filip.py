import cv2

def displayBbox(im, bbox):
    if bbox is not None:
        bbox = [bbox[0].astype(int)]
        n = len(bbox[0])
        for i in range(n):
            cv2.line(im, tuple(bbox[0][i]), tuple(bbox[0][(i+1) % n]), (0,255,0), 3)

if __name__ == '__main__':
    img = cv2.imread('testF.png')
    detector = cv2.QRCodeDetector()
    res, points, _ = detector.detectAndDecode(img)
    # Detected outputs.
    if len(res) > 0:
        print('Output : ', res)
        print('Bounding Box : ', points)
        displayBbox(img, points)
    else:
        print('QRCode not detected')

cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
