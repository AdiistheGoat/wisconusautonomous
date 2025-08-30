# Stop Line Detection using OpenCV

This project processes video frames to detect **horizontal stop lines** on the road. It uses HSV-based color masking, grayscale intensity filtering, morphological operations, edge detection, and Hough transform to reliably isolate bright, near-horizontal lines in the region where stop lines typically appear.

---

## Libraries Used
- **cv2 (OpenCV):** video capture, image preprocessing, edge and line detection  
- **numpy:** array operations and masking  
- **math:** angle calculation for filtering detected lines  

---

## Methodology

**1. Region of Interest (ROI):**  
Each frame is cropped to the lower half and central third to focus on the roadway area where a stop line is expected.

**2. Color Space Conversion (BGR → HSV):**  
The ROI is converted to HSV color space, which separates brightness from color, making it easier to segment white stop lines.

**3. Color Thresholding:**  
A white mask is created using HSV thresholds (low saturation + high value). This highlights the bright, line-like structures while suppressing darker background pixels.

**4. Grayscale Conversion and Intensity Filtering:**  
The ROI is also converted to grayscale. Only the brightest pixels (above a threshold relative to the maximum intensity) are kept, reducing noise from shadows and less relevant textures.

**5. Mask Application:**  
The HSV-based mask and grayscale intensity filter are combined to further isolate candidate stop line regions.

**6. Morphological Operations:**  
Morphological opening with a small kernel is applied to remove thin noise and enhance solid line structures.

**7. Edge Detection (Canny):**  
The cleaned image is passed through Canny edge detection to extract well-defined line edges.

**8. Line Detection (Hough Transform):**  
The probabilistic Hough transform is used to detect straight lines from the edges.  
- Only **near-horizontal lines** (angle difference < 5° from horizontal) are kept.  
- This ensures that the system detects the broad stop line and ignores vertical or slanted structures.

**9. Visualization:**  
Intermediate results (ROI, masks, morphology, edges) and the final detected stop lines are displayed in a debug grid for inspection.

---

## What Did I Try and Why It Did Not Work

At first, I attempted to detect stop lines directly from the grayscale image using binary thresholding. This approach failed because grayscale could not distinguish between true stop lines and other bright regions (e.g., reflections, lane markings).  

Switching to HSV-based masking allowed me to isolate white pixels more effectively. By combining color filtering, intensity thresholding, and morphological operations, I was able to reliably extract stop lines. Applying the Hough transform with an angle filter finally ensured that only horizontal stop lines were detected.
