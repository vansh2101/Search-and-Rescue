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


#? Converting the brown color to blue
res_brown[mask_brown > 0] = (0, 255, 255)

#? Converting the green color to yellow
res_green[mask_green > 0] = (255, 255, 0)


#? Adding the two masks
mask_res = cv2.add(mask_brown, mask_green)

#? Separating the triangles from the image
huts = cv2.bitwise_and(img, img, mask=cv2.bitwise_not(mask_res))

#? Adding all the images to get the resultant image
res = cv2.add(res_brown, res_green)
img_res = cv2.add(res, huts)


#? Displaying the image
cv2.imshow('image', img)
cv2.imshow('res', img_res)


cv2.waitKey(0)
cv2.destroyAllWindows()