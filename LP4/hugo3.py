import cv2


def displayBox(im, box):
    if box is not None:
        box = [box[0].astype(int)]
        n = len(box[0])
        for i in range(n):
            cv2.line(im, tuple(box[0][i]), tuple(box[0][(i + 1) % n]), (0,255,0), 3)

if __name__ == '__main__':
    img = cv2.imread('test35.jpg')
    detector = cv2.QRCodeDetector()
    res, points, _ = detector.detectAndDecode(img)

    if len(res) > 0:
        print('Output: ', res)
        print('Box: ', points)
        displayBox(img, points)
    else: 
        print('QRCode not detected')

cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
