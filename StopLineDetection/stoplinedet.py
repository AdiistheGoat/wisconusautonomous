import cv2
import numpy as np
import glob
import math

import cv2 
 
# Create a video capture object, in this case we are reading the video from a file
vid_capture = cv2.VideoCapture('/Users/adityagoyal/Desktop/WA /videos/11.mp4')
 
if (vid_capture.isOpened() == False):
  print("Error opening the video file")
# Read fps and frame count
else:
  # Get frame rate information
  # You can replace 5 with CAP_PROP_FPS as well, they are enumerations
  fps = vid_capture.get(5)
  print('Frames per second : ', fps,'FPS')
 
  # Get frame count
  # You can replace 7 with CAP_PROP_FRAME_COUNT as well, they are enumerations
  frame_count = vid_capture.get(7)
  print('Frame count : ', frame_count)
 
while(vid_capture.isOpened()):
  # vid_capture.read() methods returns a tuple, first element is a bool 
  # and the second is frame
  ret, frame = vid_capture.read()
  if ret == True:
    #cv2.imshow("Frame",frame)

    # sorted to process in numerical order
    image = frame

    if image is None:
        print(f"Error: Could not load image from image_path")
        
    else:
          
        height = image.shape[0]
        width = image.shape[1]
        
        imageCopy = image.copy()   # copy of image
        
        roiOrig = imageCopy[height//2:, width//3: 2*width//3]   # roi needed from original image
        
        image1 = cv2.cvtColor(roiOrig, cv2.COLOR_BGR2HSV)  # converting the roi to hsv space for color segmentation
           
        # cant do anything more here
        # the mask filters out some of the dotted lines.
        lower1 = np.array([0, 0, 230])
        upper1 = np.array([180, 30, 255])
    
        lower_mask = cv2.inRange(image1, lower1, upper1)  
    
        full_mask = lower_mask 
    
        #image = cv2.bitwise_and(image, image1, mask=full_mask)
        #cv2.imshow("masked Image",image)
      
        #roi = image[height//2:, width//3: 2*width//3]
    
        gray_image = cv2.cvtColor(roiOrig, cv2.COLOR_BGR2GRAY)
        
        
        
        # This line sets pixel values in gray_image to 0 where the pixel value is less than 5/6 of the maximum pixel 
        # value in gray_image. This operation likely aims to threshold the image, keeping only the brightest pixels.
        # i dont why it was not working for 5/6. prolly there is one point which has really high intensity.
        
        #dont know if this has much effect. the color mask does much more of the filtering.
        gray_image_intensity = np.where(gray_image > 5* (np.max(gray_image)/6), gray_image, 0)
        #cv2.imshow("modifiedGrayImg",gray_image)
        
        
      
        #print(image1.shape)
        #print(gray_image_intensity.shape)
        gray_image_intensity_3d = cv2.cvtColor(gray_image_intensity, cv2.COLOR_GRAY2BGR)
        gray_image_segmented = cv2.bitwise_and(gray_image_intensity_3d, image1, mask=full_mask)
        #cv2.imshow("gray masked",gray_image)
        
     
        blank = np.zeros_like(gray_image) # is it doing all zeroes

        # applying max  gaussian blur has a good amoutn of effect. using greater blur to remove slim lines.
        #blurred_image = cv2.GaussianBlur(gray_image, (3 ,3), 0)
        # gaussian blur may just adjust the no of votes. 
        
        kernel = np.ones((3,3),np.uint8)      
        #edgesRemove_image = cv2.erode(gray_image_segmented,None, iterations=2)
        opening = cv2.morphologyEx(gray_image_segmented, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernel)
        #cv2.imshow("fo4m[]",blurred_image
        

       # Adjust Canny edge detection parameters to not detect weaker edges.
        threshold1 = 150
        threshold2 = 200
        apertureSize = 3  # why did a smaller aperture size work for sixth image
        L2gradient = True  # Use L2 gradient

        # Apply Canny edge detection
        edges = cv2.Canny(closing, threshold1, threshold2, apertureSize=apertureSize, L2gradient=L2gradient)


        #edges = cv2.Canny(gray_image, 250, 400, apertureSize=7)
        # applies the Canny edge detection algorithm to gray_image. It detects edges in the image using the Canny edge detection technique,
        cv2.imshow("edgesImg",edges)       
          
          
        color_image = np.copy(roiOrig)
        
        #creates a deep copy of the region of interest (ROI) and assigns it to color_image
        
        #lines = cv2.HoughLines(edges, 3, np.pi/180, 180)
             
        lines = cv2.HoughLinesP(edges, 3, np.pi / 180, 170, None, 100, 30)
        
        if lines is not None and len(lines) < 15 and len(lines)>2:
            # Filter lines based on angle
            for line in lines:
                for x1, y1, x2, y2 in line:
                    xDiff = x2-x1
                    yDiff = y2-y1     
                    rad = np.abs(math.atan(yDiff/xDiff))
                    angle = np.abs((rad * 180 / np.pi))
                    if(angle<5):
                        cv2.line(blank, (x1, y1), (x2, y2), (255, 0, 0), 4)
                        cv2.line(color_image, (x1, y1), (x2, y2), (255, 0, 0), 3)
  
                    # Convert theta to degrees (from radians)
                    #angle = np.abs((theta * 180 / np.pi) - 90)  # Adjusting to measure angle from horizontal
                    
                    # Keep lines within a ±15 degree angle from the horizontal
                    #if  angle < 5:
                        # Calculate line endpoints to draw
                        #a = np.cos(theta)
                        #b = np.sin(theta)
                        #x0 = a * rho
                        #y0 = b * rho
                        #x1 = int(x0 + 1000 * (-b))
                        #y1 = int(y0 + 1000 * (a))
                        #x2 = int(x0 - 1000 * (-b))
                        #y2 = int(y0 - 1000 * (a))
    
                        # Draw the line
                    
                        
        #cv2.imshow("copymaskedimage",imageCopy)
        cv2.imshow("blank",blank)
        maskedDet = gray_image * blank # Assuming blank is a binary image (containing only 0s and 255s), where the pixels that match between the gray_image and the blank image are retained (set to 255), while non-matching pixels are set to 0.
        blank = blank & gray_image  # to contain only the pixels that match between the original blank and the gray_image.

        row1 = np.hstack((roiOrig, cv2.cvtColor(gray_image_intensity, cv2.COLOR_GRAY2BGR),gray_image_segmented,))
  
        row2 = np.hstack((opening,closing, cv2.cvtColor(maskedDet, cv2.COLOR_GRAY2BGR), cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR),color_image))
        
        # Concatenate the two rows to get a 2x3 grid
        row2_resized = cv2.resize(row2, (row1.shape[1], row2.shape[0]))
        grid = np.vstack((row1, row2_resized))
        # Optionally, display the processed image
        cv2.imshow("Processed Frames as Video", grid)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit early   # millisecodns it has tow ait before egtting the enxt image
            break
        print("lrf04 r4")
cv2.destroyAllWindows()
