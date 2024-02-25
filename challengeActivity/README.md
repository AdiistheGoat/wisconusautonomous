# Wisconsin Autonomous Perception Coding Challenge


## Answer.png:
![](https://github.com/AdiistheGoat/wisconusautonomous/blob/main/challengeActivity/answer.png)


## Libraries used:
- cv2
- numpy

## Methodolgy:


## What did I try and why do I think it did not work:

- I tried to isolate the colors by just converting it into grayscale and then binary threholding it. It was clearly not working. I think it was not working becuase I hadn't seprated the colors beforehand. I realized it's better to isolate the color using by converting the image it into HSV and then generating masks from the HSV generated images using lower and higher ranges(that I had to experiment with a lot) and then Anding those masks with the original image to isolate the red color. 

