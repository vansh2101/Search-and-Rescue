import cv2
import numpy as np


#? Reading the image
img = cv2.imread('sample.png', cv2.IMREAD_COLOR)

#? Converting to hsv
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


#? Defining the range of brown color
lower_brown = np.array([10, 0, 30])
upper_brown = np.array([31, 255, 255])

#? Defining the range of green color
lower_green = np.array([36, 0, 0])
upper_green = np.array([86, 255, 255])


#? Creating the mask and filtering the image for brown color
mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
res_brown = cv2.bitwise_and(img, img, mask=mask_brown)

#? Creating the mask and filtering the image for green color
mask_green = cv2.inRange(hsv, lower_green, upper_green)
res_green = cv2.bitwise_and(img, img, mask=mask_green)


# res = cv2.add(res_brown, res_green)


#? Displaying the image
cv2.imshow('image', img)
# cv2.imshow('res', res)
# cv2.imshow('mask_brown', mask_brown)
cv2.imshow('res_brown', res_brown)
# cv2.imshow('mask_green', mask_green)
cv2.imshow('res_green', res_green)


cv2.waitKey(0)
cv2.destroyAllWindows()