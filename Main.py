import cv2
import pyttsx3
from ultralytics import YOLO
import numpy as np
import pytesseract
import sys

# Initialize the text-to-speech engine
tts_engine = pyttsx3.init()

# Load YOLOv8 model
yolo_model = YOLO('yolov8n.pt')

# Load Pose Estimation model
pose_net = cv2.dnn.readNetFromTensorflow("C:\\Users\\dell\\Desktop\\Pose\\human-pose-estimation-opencv-master\\graph_opt.pb")

# Configure the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Constants for Pose Estimation
BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
               "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
               "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
               "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
               ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
               ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
               ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
               ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]

inWidth = 368
inHeight = 368

# Function to convert text to speech
def text_to_speech(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Object Detection
def Object_Detection(model, frame):
    results = model(frame)
    objects = []
    for result in results:
        for obj in result.boxes.data:
            bbox = obj[:4].cpu().numpy()
            conf = obj[4].cpu().numpy()
            class_id = int(obj[5].cpu().numpy())
            name = model.names[class_id]
            objects.append({"name": name, "bbox": bbox, "conf": conf})
    annotated_frame = results[0].plot()
    return objects, annotated_frame

# Function to describe object positions
def describe_positions(objects):
    descriptions = []
    for obj in objects:
        name = obj['name']
        bbox = obj['bbox']
        x_center = bbox[0] + bbox[2] / 2
        y_center = bbox[1] + bbox[3] / 2
        
        if x_center < 640 / 3:
            x_pos = "left"
        elif x_center < 2 * 640 / 3:
            x_pos = "center"
        else:
            x_pos = "right"
        
        if y_center < 480 / 3:
            y_pos = "top"
        elif y_center < 2 * 480 / 3:
            y_pos = "mid"
        else:
            y_pos = "bottom"
        
        descriptions.append(f"there is a {name} in the {y_pos} {x_pos}")

    return ". ".join(descriptions)

# Pose Estimation
def pose_estimated(frame):
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
    
    pose_net.setInput(cv2.dnn.blobFromImage(frame, 1.0, (inWidth, inHeight), (127.5, 127.5, 127.5), swapRB=True, crop=False))
    out = pose_net.forward()
    out = out[:, :19, :, :]  # MobileNet output [1, 57, -1, -1], we only need the first 19 elements

    assert(len(BODY_PARTS) == out.shape[1])

    points = []
    for i in range(len(BODY_PARTS)):
        heatMap = out[0, i, :, :]
        _, conf, _, point = cv2.minMaxLoc(heatMap)
        x = (frameWidth * point[0]) / out.shape[3]
        y = (frameHeight * point[1]) / out.shape[2]
        points.append((int(x), int(y)) if conf > 0.2 else None)

    poses = []
    for pair in POSE_PAIRS:
        partFrom = pair[0]
        partTo = pair[1]
        idFrom = BODY_PARTS[partFrom]
        idTo = BODY_PARTS[partTo]

        if points[idFrom] and points[idTo]:
            cv2.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
            cv2.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)
            cv2.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)
            poses.append((partFrom, partTo))

    t, _ = pose_net.getPerfProfile()
    freq = cv2.getTickFrequency() / 1000
    cv2.putText(frame, '%.2fms' % (t / freq), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    return poses

# Function to map poses to sentences
def poses_to_sentence(poses):
    if ('Neck', 'RShoulder') in poses and ('Neck', 'LShoulder') in poses:
        if ('RShoulder', 'RElbow') in poses and ('LShoulder', 'LElbow') in poses:
            return "The person has raised both arms."
        elif ('RShoulder', 'RElbow') in poses:
            return "The person has raised their right arm."
        elif ('LShoulder', 'LElbow') in poses:
            return "The person has raised their left arm."

    if ('Neck', 'RHip') in poses and ('Neck', 'LHip') in poses:
        if ('RHip', 'RKnee') in poses and ('LHip', 'LKnee') in poses:
            return "The person is standing."

    if ('Neck', 'Nose') in poses:
        return "The person is facing forward."

    if ('Neck', 'RHip') in poses and ('RHip', 'RKnee') in poses and ('RKnee', 'RAnkle') in poses:
        return "The person is kicking with the right leg."

    if ('Neck', 'LHip') in poses and ('LHip', 'LKnee') in poses and ('LKnee', 'LAnkle') in poses:
        return "The person is kicking with the left leg."

    if ('RElbow', 'RWrist') in poses and ('LElbow', 'LWrist') in poses:
        return "The person is waving."

    if ('Neck', 'RHip') in poses and ('RHip', 'RKnee') in poses:
        return "The person is bending their right leg."

    if ('Neck', 'LHip') in poses and ('LHip', 'LKnee') in poses:
        return "The person is bending their left leg."

    if ('RHip', 'RKnee') in poses and ('RKnee', 'RAnkle') in poses:
        return "The person is kicking a ball with their right leg."

    if ('LHip', 'LKnee') in poses and ('LKnee', 'LAnkle') in poses:
        return "The person is kicking a ball with their left leg."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'LShoulder') in poses:
        return "The person has both arms relaxed."

    if ('RShoulder', 'RElbow') in poses and ('LShoulder', 'LElbow') in poses:
        return "The person has both hands."

    if ('Neck', 'RElbow') in poses and ('Neck', 'RWrist') in poses:
        return "The person is touching their right ear with their right hand."

    if ('Neck', 'LElbow') in poses and ('Neck', 'LWrist') in poses:
        return "The person is touching their left ear with their left hand."

    if ('Neck', 'RElbow') in poses and ('Neck', 'RWrist') in poses:
        return "The person is touching their right ear with their right hand."

    if ('Neck', 'LElbow') in poses and ('Neck', 'LWrist') in poses:
        return "The person is touching their left ear with their left hand."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'RElbow') in poses:
        return "The person is scratching their right shoulder with their right hand."

    if ('Neck', 'LShoulder') in poses and ('Neck', 'LElbow') in poses:
        return "The person is scratching their left shoulder with their left hand."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'RElbow') in poses:
        return "The person is scratching their right shoulder with their right hand."

    if ('Neck', 'LShoulder') in poses and ('Neck', 'LElbow') in poses:
        return "The person is scratching their left shoulder with their left hand."

    if ('Neck', 'RHip') in poses and ('Neck', 'RAnkle') in poses:
        return "The person is leaning over to the right."

    if ('Neck', 'LHip') in poses and ('Neck', 'LAnkle') in poses:
        return "The person is leaning over to the left."

    if ('RHip', 'RAnkle') in poses and ('LHip', 'LAnkle') in poses:
        return "The person is sitting on a chair."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'RElbow') in poses:
        return "The person is shaking their right hand."

    if ('Neck', 'LShoulder') in poses and ('Neck', 'LElbow') in poses:
        return "The person is shaking their left hand."

    if ('Neck', 'RElbow') in poses and ('Neck', 'RWrist') in poses:
        return "The person is touching their right ear with their right hand."

    if ('Neck', 'LElbow') in poses and ('Neck', 'LWrist') in poses:
        return "The person is touching their left ear with their left hand."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'RElbow') in poses:
        return "The person is scratching their right shoulder with their right hand."

    if ('Neck', 'LShoulder') in poses and ('Neck', 'LElbow') in poses:
        return "The person is scratching their left shoulder with their left hand."

    if ('Neck', 'RHip') in poses and ('Neck', 'RAnkle') in poses:
        return "The person is leaning over to the right."

    if ('Neck', 'LHip') in poses and ('Neck', 'LAnkle') in poses:
        return "The person is leaning over to the left."

    if ('RHip', 'RAnkle') in poses and ('LHip', 'LAnkle') in poses:
        return "The person is sitting on a chair."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'RElbow') in poses:
        return "The person is shaking their right hand."

    if ('Neck', 'LShoulder') in poses and ('Neck', 'LElbow') in poses:
        return "The person is shaking their left hand."

    if ('Neck', 'RElbow') in poses and ('Neck', 'RWrist') in poses:
        return "The person is touching their right ear with their right hand."

    if ('Neck', 'LElbow') in poses and ('Neck', 'LWrist') in poses:
        return "The person is touching their left ear with their left hand."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'RElbow') in poses:
        return "The person is scratching their right shoulder with their right hand."

    if ('Neck', 'LShoulder') in poses and ('Neck', 'LElbow') in poses:
        return "The person is scratching their left shoulder with their left hand."

    if ('Neck', 'RHip') in poses and ('Neck', 'RAnkle') in poses:
        return "The person is leaning over to the right."

    if ('Neck', 'LHip') in poses and ('Neck', 'LAnkle') in poses:
        return "The person is leaning over to the left."

    if ('RHip', 'RAnkle') in poses and ('LHip', 'LAnkle') in poses:
        return "The person is sitting on a chair."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'RElbow') in poses:
        return "The person is shaking their right hand."

    if ('Neck', 'LShoulder') in poses and ('Neck', 'LElbow') in poses:
        return "The person is shaking their left hand."

    if ('Neck', 'RElbow') in poses and ('Neck', 'RWrist') in poses:
        return "The person is touching their right ear with their right hand."

    if ('Neck', 'LElbow') in poses and ('Neck', 'LWrist') in poses:
        return "The person is touching their left ear with their left hand."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'RElbow') in poses:
        return "The person is scratching their right shoulder with their right hand."

    if ('Neck', 'LShoulder') in poses and ('Neck', 'LElbow') in poses:
        return "The person is scratching their left shoulder with their left hand."

    if ('Neck', 'RHip') in poses and ('Neck', 'RAnkle') in poses:
        return "The person is leaning over to the right."

    if ('Neck', 'LHip') in poses and ('Neck', 'LAnkle') in poses:
        return "The person is leaning over to the left."

    if ('RHip', 'RAnkle') in poses and ('LHip', 'LAnkle') in poses:
        return "The person is sitting on a chair."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'RElbow') in poses:
        return "The person is shaking their right hand."

    if ('Neck', 'LShoulder') in poses and ('Neck', 'LElbow') in poses:
        return "The person is shaking their left hand."

    if ('Neck', 'RElbow') in poses and ('Neck', 'RWrist') in poses:
        return "The person is touching their right ear with their right hand."

    if ('Neck', 'LElbow') in poses and ('Neck', 'LWrist') in poses:
        return "The person is touching their left ear with their left hand."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'RElbow') in poses:
        return "The person is scratching their right shoulder with their right hand."

    if ('Neck', 'LShoulder') in poses and ('Neck', 'LElbow') in poses:
        return "The person is scratching their left shoulder with their left hand."

    if ('Neck', 'RHip') in poses and ('Neck', 'RAnkle') in poses:
        return "The person is leaning over to the right."

    if ('Neck', 'LHip') in poses and ('Neck', 'LAnkle') in poses:
        return "The person is leaning over to the left."

    if ('RHip', 'RAnkle') in poses and ('LHip', 'LAnkle') in poses:
        return "The person is sitting on a chair."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'RElbow') in poses:
        return "The person is shaking their right hand."

    if ('Neck', 'LShoulder') in poses and ('Neck', 'LElbow') in poses:
        return "The person is shaking their left hand."

    if ('Neck', 'RElbow') in poses and ('Neck', 'RWrist') in poses:
        return "The person is touching their right ear with their right hand."

    if ('Neck', 'LElbow') in poses and ('Neck', 'LWrist') in poses:
        return "The person is touching their left ear with their left hand."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'RElbow') in poses:
        return "The person is scratching their right shoulder with their right hand."

    if ('Neck', 'LShoulder') in poses and ('Neck', 'LElbow') in poses:
        return "The person is scratching their left shoulder with their left hand."

    if ('Neck', 'RHip') in poses and ('Neck', 'RAnkle') in poses:
        return "The person is leaning over to the right."

    if ('Neck', 'LHip') in poses and ('Neck', 'LAnkle') in poses:
        return "The person is leaning over to the left."

    if ('RHip', 'RAnkle') in poses and ('LHip', 'LAnkle') in poses:
        return "The person is sitting on a chair."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'RElbow') in poses:
        return "The person is shaking their right hand."

    if ('Neck', 'LShoulder') in poses and ('Neck', 'LElbow') in poses:
        return "The person is shaking their left hand."

    return "The person's pose is unclear."



# OCR
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    return thresh

def Real_time_ocr(frame):
    preprocessed_frame = preprocess_image(frame)
    text = pytesseract.image_to_string(preprocessed_frame)
    return text.strip()

def main():
    cap = cv2.VideoCapture(1)  # Open the default camera
    
    choice = input("Enter 'A' for Object Detection, 'B' for Pose Estimation, 'C' for OCR: ").strip().upper()

    if choice not in ['A', 'B', 'C']:
        print("Invalid choice")
        sys.exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if choice == 'A':
            objects, annotated_frame = Object_Detection(yolo_model, frame)
            if len(objects) > 0:
                descriptions = describe_positions(objects)
                text_to_speech(descriptions)
                print(descriptions)
            cv2.imshow('Object Detection', annotated_frame)

        elif choice == 'B':
            poses = pose_estimated(frame)
            description = poses_to_sentence(poses)
            text_to_speech(description)
            print(description)
            cv2.imshow('Pose Estimation', frame)

        elif choice == 'C':
            text = Real_time_ocr(frame)
            if text:
                text_to_speech(text)
                print(text)
            cv2.imshow('OCR', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
