import cv2
import mediapipe as mp

screen_width = 460
screen_height = 860
# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Initialize webcam

def result_display():    # If landmarks are detected, print left and right shoulder coordinates and draw rectangles
    cap = cv2.VideoCapture(0)
    success, frame = cap.read()
    frame = cv2.flip(frame,1)
    frame= cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    frame_height, frame_width, _ = frame.shape
    aspect_ratio = frame_width / frame_height

    # Calculate new width and height based on screen resolution
    new_width = int(screen_height * aspect_ratio)
    new_height = screen_height

    # Resize the frame to match the screen resolution
    frame = cv2.resize(frame, (new_width, new_height))
    # Convert BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame)  
    if results.pose_landmarks:
        left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_shoulder_x, left_shoulder_y = int(left_shoulder.x * frame.shape[1]), int(left_shoulder.y * frame.shape[0])
        left_shoulder = [left_shoulder_x,left_shoulder_y]
    
        right_shoulder_x, right_shoulder_y = int(right_shoulder.x * frame.shape[1]), int(right_shoulder.y * frame.shape[0])
        right_shoulder = [right_shoulder_x,right_shoulder_y]
        shoulder_width =abs(right_shoulder_x-left_shoulder_x)*0.17
        size ="Nan"
        if(shoulder_width>=34 and shoulder_width<=36):
            size = "S"
        elif(shoulder_width>36 and shoulder_width<=39):
            size = "M"
        elif(shoulder_width>39 and shoulder_width<=42):
            size = "L"
        elif(shoulder_width>42 and shoulder_width<=44):
            size = "XL"
        elif(shoulder_width>44 and shoulder_width<=46):
            size = "XXL"
        
        print(size,shoulder_width)
        return size
    
# result_display()