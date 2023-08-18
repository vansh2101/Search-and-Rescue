import cv2
import numpy as np



#* Filtering out the burnt and unburnt area
#? Reading the image
img = cv2.imread('sample.png', cv2.IMREAD_COLOR)

#? Converting to hsv
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


#? Defining the range of colors
lower_brown = np.array([8, 0, 10])
upper_brown = np.array([31, 255, 255])

lower_green = np.array([32, 0, 0])
upper_green = np.array([86, 255, 255])


#? Creating the mask and filtering the image
mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
res_brown = cv2.bitwise_and(img, img, mask=mask_brown)

mask_green = cv2.inRange(hsv, lower_green, upper_green)
res_green = cv2.bitwise_and(img, img, mask=mask_green)


#? Converting the brown color to blue and green to yellow
res_brown[mask_brown > 0] = (0, 255, 255)

res_green[mask_green > 0] = (255, 255, 0)


#? Adding the two masks
mask_res = cv2.add(mask_brown, mask_green)

#? Separating the triangles from the image
huts = cv2.bitwise_and(img, img, mask=cv2.bitwise_not(mask_res))

#? Adding all the images to get the resultant image
img_res = res_green + res_brown + huts


#? Displaying the image
cv2.imshow('image', img)
cv2.imshow('res', img_res)


cv2.waitKey(0)
cv2.destroyAllWindows()



#* Counting the number of huts
def count_triangles(img):
    #? Finding the contours
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #? Defining the variables for counting
    first = True
    count = 0

    #? Running the loop in the range of contours to detect the triangles
    for cnt in contours:
        if first:
            first = False
            continue

        #? Finding the approximated shapes
        arc = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.25*arc, True)

        #? Checking if the shape is a triangle
        if len(approx) == 3:
            count += 1

    return count


huts_burnt = count_triangles(mask_brown)
huts_unburnt = count_triangles(mask_green)

n_houses = [huts_burnt, huts_unburnt]

print('n_houses:', n_houses)