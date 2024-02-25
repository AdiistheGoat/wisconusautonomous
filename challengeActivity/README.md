# Wisconsin Autonomous Perception Coding Challenge

## Answer.png:
![](https://github.com/AdiistheGoat/wisconusautonomous/blob/main/challengeActivity/answer.png)

## Libraries used:
- cv2
- numpy

## Methodolgy:
- Color Space Conversion: The code starts by converting the image from the BGR color space to the HSV color space. This conversion facilitates more effective detection of red objects as HSV separates color information from intensity.

- Color Thresholding: The code defines lower and upper bounds for the red color in the HSV color space. It then creates masks based on these color ranges using the cv.inRange() function. This step isolates the regions in the image that likely contain red objects.

- Mask Combination: After creating individual masks for two ranges of red color (as red can span two ranges due to its circular nature in HSV color space), the code combines these masks using bitwise OR operation to create a single mask covering the entire range of red color.

- Mask Application: The combined mask is applied to the original image using bitwise AND operation. This effectively removes all non-red regions from the image, leaving only the red regions visible.

- Grayscale Conversion and Thresholding: The resulting image is converted to grayscale, followed by thresholding to create a binary image where red regions are represented by white pixels and the rest by black pixels.

- Contour Detection: The binary image is split into left and right sections. Contours are then detected separately in each section using the cv.findContours() function. Contours represent the boundaries of the red regions.

- Contour Joining: Contours within each section are joined by drawing lines between consecutive contour points. This step aims to create continuous outlines around red objects, enhancing their visual representation.

- Output Visualization: Finally, the code saves the image with detected contours and displays it for visual inspection, allowing users to see the result of the contour detection process.

## What did I try and why do I think it did not work:

- I tried to isolate the colors by just converting it into grayscale and then binary threholding it. It was clearly not working. I think it was not working becuase I hadn't seprated the colors beforehand. I realized it's better to isolate the color using by converting the image it into HSV and then generating masks from the HSV generated images using lower and higher ranges(that I had to experiment with a lot) and then Anding those masks with the original image to isolate the red color. 

