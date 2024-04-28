import cv2

# Load the image and convert it to grayscale
img = cv2.imread('test.jpg')

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Detect people in the image
locations, confidence = hog.detectMultiScale(img)

# Draw rectangles around the detected people
for (x, y, w, h) in locations:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 5)

# Display the resulting frame
cv2.imshow('People', img)
cv2.waitKey(0)
cv2.destroyAllWindows()