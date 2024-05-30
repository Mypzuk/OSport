# bicycle.py

# Сторонние модули
import cv2
import mediapipe as mp


async def check_bicycle(name:str):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)
    video = cv2.VideoCapture(f"cv/cvmedia/{name}")

    res = []
    count = 0
    last_leftleg = 'NoPose'
    last_rightleg = 'NoPose'
    # Var: 1) NoPose 2) LeftBent 3) LeftStr 4) RightBent 5) RightStr
    last_side = 'None'
    # Var: 1) None 2) Right 3) Left

    def distanceCalculate(p1, p2):
        """p1 and p2 in format (x1,y1) and (x2,y2) tuples"""
        dis = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
        return dis

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
            leftElbow = (int(results.pose_landmarks.landmark[13].x * image_width),
                        int(results.pose_landmarks.landmark[13].y * image_height))
            rightElbow = (int(results.pose_landmarks.landmark[14].x * image_width),
                        int(results.pose_landmarks.landmark[14].y * image_height))

            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)


            if leftKnee[0] < leftHip[0]:
                last_leftleg = 'LeftBent'
            elif leftKnee[0] > leftHip[0]:
                last_leftleg = 'LeftStr'
            if rightKnee[0] < rightHip[0]:
                last_rightleg = 'RightBent'
            elif rightKnee[0] > rightHip[0]:
                last_rightleg = 'RightStr'

            if last_leftleg == 'LeftBent' and distanceCalculate(rightElbow,leftKnee) < 300:
                res.append('Left')
            if last_rightleg == 'RightBent' and distanceCalculate(leftElbow,rightKnee) < 100:
                res.append('Right')

        # cv2.imshow("Test tracking", image)
        # cv2.waitKey(1)
#    print(res)
    for i in range(len(res)):
        if i < len(res) - 1:
            if res[i] != res[i + 1]:
                count += 1
    
    return count + 1
