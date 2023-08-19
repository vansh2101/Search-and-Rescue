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
def count_triangles(img, red, blue):
    #? Finding the contours
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #? Defining the variables for counting
    first = True
    count = 0
    r = 0
    b = 0

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

            #? Finding the center point of the shape
            mom = cv2.moments(cnt)

            if mom['m00'] != 0:
                x = int(mom['m10']/mom['m00'])
                y = int(mom['m01']/mom['m00'])

                #? Checking if the center point is red or blue
                if red[y][x] == 255:
                    r += 1

                elif blue[y][x] == 255:
                    b += 1

                else:
                    count -= 1


    return count, r, b


#? Defining the range of colors
lower_red = np.array([0, 0, 0])
upper_red = np.array([0, 255, 255])

lower_blue = np.array([115, 150, 0])
upper_blue = np.array([135, 255, 255])

#? Creating the mask and filtering the image to check the color of the triangles
mask_red = cv2.inRange(hsv, lower_red, upper_red)

mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)


#? calling the functions
huts_burnt, red_huts_burnt, blue_huts_burnt = count_triangles(mask_brown, mask_red, mask_blue)
huts_unburnt, red_huts_unburnt, blue_huts_unburnt = count_triangles(mask_green, mask_red, mask_blue)

n_houses = [huts_burnt, huts_unburnt]


#? Calculating the priority of the houses on burnt and unburnt grass
priority_burnt = red_huts_burnt + blue_huts_burnt*2

priority_unburnt = red_huts_unburnt + blue_huts_unburnt*2

priority_houses = [priority_burnt, priority_unburnt]


#? Calculating the priority ratio
priority_ratio = [round(priority_burnt/priority_unburnt, 2)]


#? Printing the results
print('n_houses:', n_houses)
print('priority_houses:', priority_houses)
print('priority_ratio:', priority_ratio)