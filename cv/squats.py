# squats.py

# Сторонние модули
import cv2
import mediapipe as mp


async def check_squats(name:str):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    cap = cv2.VideoCapture(f"cv/cvmedia/{name}")
    error = (cap.get(4)/100) * 5 # Степень ошибки = 5
     
    count = 0
    position = None
     
    with mp_pose.Pose(
        min_detection_confidence = 0.7,
        min_tracking_confidence = 0.7) as pose:
     
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break
     
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = True
            results = pose.process(image)
            imlist = []
        
            if (results.pose_landmarks != None):
                mp_drawing.draw_landmarks(image,
                                        results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                for id,im in enumerate(results.pose_landmarks.landmark):
                    h,w,_=image.shape
                    X,Y=int(im.x*w), int(im.y*h)
                    imlist.append([id,X,Y])
                    error_1=-error
                    error_2=error
                if (len(imlist)!=0):
        
                    if (
                            (
                            #imlist[24][2]  <= imlist[26][2] or imlist[23][2]  <= imlist[25][2] 
                            imlist[24][2]  >= imlist[26][2]+error_1 or imlist[23][2]  >= imlist[25][2] +error_1
                            #or imlist[24][2]+error_1  <= imlist[25][2] or imlist[23][2]+error_1  <= imlist[26][2]
                            ) 
                        ):
                        position="down"
        
                    elif (
                            (imlist[24][2]  < imlist[26][2] or imlist[23][2]  < imlist[25][2] 
                            ) 
                        and position=="down"
                        ):
        
                        position="up"
                        count+=1


    return count
