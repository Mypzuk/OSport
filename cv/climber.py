# climber.py

# Сторонние модули
import cv2
import mediapipe as mp
import matplotlib.pyplot as plt


async def check_climber(name:str):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)
    video = cv2.VideoCapture(f"cv/cvmedia/{name}")

    count = 0
    left_leg_open = True
    right_leg_open = True
    last_leftleg = 'NoPose'
    last_rightleg = 'NoPose'
    # Var: 1) NoPose 2) LeftBent 3) LeftStr 4) RightBent 5) RightStr

    while video.isOpened():
        ret, image = video.read()

        if not ret:
            break

        image_height, image_width, _ = image.shape
        results = pose.process(image)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            leftKnee = (int(results.pose_landmarks.landmark[25].x * image_width),
                        int(results.pose_landmarks.landmark[25].y * image_height))
            rightKnee = (int(results.pose_landmarks.landmark[26].x * image_width),
                         int(results.pose_landmarks.landmark[26].y * image_height))
            leftHip = (int(results.pose_landmarks.landmark[23].x * image_width),
                       int(results.pose_landmarks.landmark[23].y * image_height))
            rightHip = (int(results.pose_landmarks.landmark[24].x * image_width),
                        int(results.pose_landmarks.landmark[24].y * image_height))

            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            if (last_leftleg == 'LeftBent' and leftKnee[0] > leftHip[0]) or (
                    last_rightleg == 'RightBent' and rightKnee[0] > rightHip[0]):
                count += 1
            #    print(count)

            if leftKnee[0] < leftHip[0]:
                # print('LeftBent!')
                last_leftleg = 'LeftBent'
            elif leftKnee[0] > leftHip[0]:
                last_leftleg = 'LeftStr'
            if rightKnee[0] < rightHip[0]:
                # print('RightBent!')
                last_rightleg = 'RightBent'
            elif rightKnee[0] > rightHip[0]:
                last_rightleg = 'RightStr'


        # cv2.imshow("Test tracking", image)
        # cv2.waitKey(1)
    
    return count
