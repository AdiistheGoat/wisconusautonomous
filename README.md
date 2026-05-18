# Wisconsin Autonomous Perception Projects

This repository contains my work on a couple of computer vision tasks related to autonomous driving and perception. The projects mainly use OpenCV and NumPy to process images and video and detect useful road features.

## Projects

### `challengeActivity`
This folder contains my solution to a perception coding challenge.

The goal here was to detect red regions in an image and outline them in a useful way. My approach was to:
- convert the image from BGR to HSV
- isolate the red regions using color thresholds
- apply the mask to the image
- convert the result to grayscale and threshold it
- find contours
- split the image into left and right halves
- connect contour points to mark the detected regions

Files:
- `wisco.py` — main script
- `answer.png` — output image
- `README.md` — explanation of the approach

### `StopLineDetection`
This folder contains my work on detecting stop lines from road video frames.

The script processes a video frame by frame and tries to detect horizontal stop lines by:
- selecting a region of interest from the road
- converting the region to HSV
- isolating bright white areas
- filtering by intensity
- applying morphological operations
- detecting edges with Canny
- detecting lines with Hough Transform
- keeping only near-horizontal lines

Files:
- `stoplinedet.py` — main script
- `README.md` — explanation of the approach

## Tools Used

- Python
- OpenCV
- NumPy
- math

## Running the Code

Install dependencies:

```bash
pip install opencv-python numpy
```

Then run the scripts from their folders:

```bash
python wisco.py
```

```bash
python stoplinedet.py
```

Note: some file paths in the scripts may need to be updated to match your local machine.

## Summary

Overall, this repository shows my work in building and testing classical computer vision pipelines for perception-related problems. It helped me get more comfortable with image preprocessing, masking, contour detection, edge detection, and line detection in OpenCV.
