import cv2

test = cv2.VideoCapture(0)

while True:
	ret, image = test.read()
	cv2.imshow("please", image)

	if cv2.waitKey(1) == 'q':
		break
test.release()
cv2.closeAllWindows()
