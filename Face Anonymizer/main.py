import cv2
import os
import argparse
import mediapipe as mp

def blurred_image(image, face_detections):
    Height, Width, _ = image.shape
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output = face_detection.process(image_rgb)

    print(output.detections)

    if output.detections is not None:
        for detection in output.detections:
            location_data = detection.location_data
            bounding_box = location_data.relative_bounding_box

            x1,y1,width,height = bounding_box.xmin,bounding_box.ymin,bounding_box.width,bounding_box.height

            x1 = int(x1*Width)
            y1 = int(y1*Height)
            width = int(width*Width)
            height = int(height*Height)

            image = cv2.rectangle(image, (x1, y1),(x1+width, y1+height), (0,255,0),10)

            #blur faces

            image[y1:y1+height, x1:x1 + width, :] = cv2.blur(image[y1:y1+height, x1:x1 + width, :], (30,30))

    return image

args = argparse.ArgumentParser()

args.add_argument("--mode", default='webcam')
args.add_argument("--filePath", default=None)

args = args.parse_args()

output_dir = './output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


#detect faces
mp_face_detection = mp.solutions.face_detection

with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:

    if args.mode in ["image"]:

        #read image
        image = cv2.imread(args.filePath)

        # Height, Width, _ = image.shape

        image = blurred_image(image, face_detection)
        
        #save images
        cv2.imwrite(os.path.join(output_dir, 'output.png'), image)

    elif args.mode in ['video']:
        cap = cv2.VideoCapture(args.filePath)
        ret, frame  = cap.read()

        output_video = cv2.VideoWriter(os.path.join(out_dir,'output.mp4'),
                                       cv2.VideoWriter_fourcc(*'MP4V'),
                                       25,
                                       (frame.shape[1], frame.shape[0]))
        while ret:
            frame = blurred_image(frame, face_detection)

            output_video.write(frame)

            ret, frame = cap.read()

        cap.release()   
        output_video.release()

    elif args.mode in ['webcam']:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        while ret:
            frame = blurred_image(frame, face_detection)
            cv2.imshow("Blurred webcam", frame)
            cv2.waitKey(25)

            ret,frame = cap.read()

        cap.release()
