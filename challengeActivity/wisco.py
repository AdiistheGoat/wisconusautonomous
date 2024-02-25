import cv2 as cv 
import numpy as np

image = cv.imread('red.png') #reads the image. formatting the "image" does not change the original image
 
result = image.copy()  # copies the image
 
image1 = cv.cvtColor(image, cv.COLOR_BGR2HSV)  # converting image from grey scale to HSV scale
#cv.imshow('image', image1)  # shows the image which has converted from BGR TO HSV scale

# finding hsv value for red
#red = np.uint8([[[0,95,85]]])
#hsv_red = cv.cvtColor(red,cv.COLOR_BGR2HSV)
#print( hsv_red )
 
#The red color, in OpenCV, has the hue values approximately in the range of 0 to 10 and 160 to 180 but we will set to 35 according to our previous code output

# lower boundary RED color range values; Hue (0 - 10)  --- 1st criteria
lower1 = np.array([30, 230, 165])
upper1 = np.array([40, 245, 255])
 
# upper boundary RED color range values; Hue (160 - 180)  --- 2nd criteria
lower2 = np.array([160,230,165])
upper2 = np.array([179,245,255])
 
 # generates mask--- (0 for values which dont fall in range and 255 for values which fall in range.)
 # 255 represents color pixels and 0 represents non color pixels. 
 
lower_mask = cv.inRange(image1, lower1, upper1)  
upper_mask = cv.inRange(image1, lower2, upper2)
full_mask = lower_mask + upper_mask   # combining the masks and then overlaping it on the image, (ORring the criteria)
result = cv.bitwise_and(result, result, mask=full_mask)

#Convert the image to grayscale, # to make intensity same before thresholding. We can use "result" but 
#converting to grayscale first is better
result1 = cv.cvtColor(result, cv.COLOR_BGR2GRAY) 

#0 represents black, and 255 represents white.
#For every pixel, the same threshold value is applied. If the pixel value is smaller than the threshold, it is set to 0, 
# otherwise it is set to a maximum value
ret,binary_image = cv.threshold(result1, 45, 255, cv.THRESH_BINARY)
binary_image_correct_type = binary_image.astype('uint8')  # converting to correct format
 
#splitting the images so that the algorithim connects/draws the lines between the contours only on one side of the image
height, width = binary_image_correct_type.shape
half_width = width//2
left_section_contour = binary_image_correct_type[:, :half_width]
right_section_contour = binary_image_correct_type[:, half_width:]
#cv.imshow('Left', left_section)
#cv.imshow('Right', right_section)

# We will ddraw contours
height, width, channels = image.shape   # returns a 3rd item/paarmeter if image is not binaryimage
half_width = width//2
left_section_marked = image[:, :half_width]
right_section_marked = image[:, half_width:]

#RETR_TREE
# A binary image is required as an argument for .findContours method
#cv.CHAIN_APPROX_SIMPLE It removes all redundant points and compresses the contour, thereby saving memory.

#contours is a Python list of all the contours in the image.
# contoursLeft contains all the coordinates of the contours on the left side of the image.
# contoursRight contains all the coordinates of the contours on the right side of the image.

contoursleft,imgleft = cv.findContours(left_section_contour, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
contoursright,imright = cv.findContours(right_section_contour, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)


"""The following code is just for reference, like just to see if the find contours method found the right contours
# converting from binary image to BGR so that we can later draw contours on it
contour_image_left = cv.cvtColor(left_section_contour, cv.COLOR_GRAY2BGR)
contour_image_right = cv.cvtColor(right_section_contour, cv.COLOR_GRAY2BGR)

# pls note that we are not overwriting the image  ## we can't color on binary pic. that is why we converted binary to colored 
cv.drawContours(contour_image_left, contoursleft, -1, (0,255,0), 3)
cv.drawContours(contour_image_right, contoursright, -1, (0,255,0), 3)

cv.imshow('Left', contour_image_left)
cv.imshow('Right',contour_image_right)
"""

color = (0, 255, 0)  # Green color in BGR


# interpolating/joining contours in separate 2 images - left and right

#using a for loop to draw join all the contours on the left side of the image
num_points = 1
x1=0
y1=0
x2=0
y2=0
for contour in contoursleft:

    for point in contour:
      if(num_points%2==1):
        x1, y1 = point[0]

      else:
        x2,y2 = point[0]   
      
      if(num_points!=1):
        cv.line(left_section_marked, (x1,y1), (x2,y2), color, thickness=2)
      
      num_points += 1  
       
#using a for loop to draw join all the contours on the right side of the image       
num_points = 1
x1=0
y1=0
x2=0
y2=0
for contour in contoursright:

    for point in contour:
      if(num_points%2==1):
        x1, y1 = point[0]
          
      else:
        x2,y2 = point[0]   
      
      if(num_points!=1):
        cv.line(right_section_marked, (x1,y1), (x2,y2), color, thickness=2)
      
      num_points += 1  

    
    

# Convert image data type to uint8
image_uint8 = np.uint8(image)

# Save the image with detected boundaries
cv.imwrite('answer.png', image_uint8)

# Display the image with detected boundaries
cv.imshow('resultContours', image_uint8)
 
#cv.imshow('mask', full_mask)
#cv.imshow('result', result)
#cv.imshow('resultGray', result1)
#cv.imshow('resultBinary', binary_image)

#cv.imshow('Left1', left_section_marked)
#cv.imshow('Right1',right_section_marked)

cv.waitKey(0)
cv.destroyAllWindows()
