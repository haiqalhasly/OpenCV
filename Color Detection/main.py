#import Computer Vision library, Pillow and util file. Pillow is Python Imaging Library where it uses is mainly for basic image task.
import cv2 
from PIL import Image
from util import get_limits


blue = [255, 0, 0] # in BGR 
cap = cv2.VideoCapture(0) #to open the webcam in your computer. 0 means 1 cam, 1 = 2 cam, etc.  

while True:
    
    #Take a picture with the webcam right now, then tell me if it worked (ret) and give me the picture itself (frame).
    ret, frame = cap.read()

    #we convert from BGR to HSV because HSV is better to detect just color (hue) without adjusting the brightness and saturation 
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #determine upper limit and lower limit of our color. In this case, its blue
    lowerLimit, upperLimit = get_limits(color = blue)

    #this is mask where it job is to make the color we detect into white and everything else is black. We use it to simplify (bbox)boundaryBox application.
    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    #convert openCV mask to PIL
    mask_ = Image.fromarray(mask)

    #here is where we actually use the boundary box
    bbox = mask_.getbbox()

    
    if bbox is not None:
        #we will get the bounding box coordinate so that it will show specifically white area that is within the box
        x1,y1,x2,y2 = bbox

        #'frame is our main image', 0,255,255 is the color of the box (green), '5' is the thickness of the box
        cv2.rectangle(frame, (x1,y1), (x2,y2), (0, 255, 0), 5)

    print(bbox)

    cv2.imshow('Color Detection', frame)

#all the things you need to do when using cv
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
#we stop camera connection aka release
cap.release()

#destroy windows
cv2.destroyAllWindows()
