# FUNCTION TO CONTROL WHITEBOARD
def whiteboard():
    import cv2
    import numpy as np
    from cvzone.HandTrackingModule import HandDetector
    import autopy

    # VARIABLES
    wCam, hCam = 1280, 720
    wScr, hScr = autopy.screen.size()
    command_pause = False
    time_paused = 0
    annotations = [[]]
    annotations_index = -1
    annotations_start = False

    # FUNCTIONS
    def clear_annotations():
        return [[]], -1, False

    # ACESSING CAMERA
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    # HAND DETECTOR
    detector = HandDetector(detectionCon=0.8, maxHands=1)

    while True:
            # CAPTURING VIDEO
        sucess, video_img = cap.read()
        video_img = cv2.flip(video_img, 1) 

        if not sucess:
            break

        else:
            # IMPORTING & DISPLAYING WHITEBOARD BACKGROUND
            path_backgroung = r"static\assets\pres\whiteboard-backgroung.jpg"
            background = cv2.imread(path_backgroung)
            background = cv2.resize(background, (int(wScr), int(hScr)))

            # HAND RECOGNITION
            hands, video_img = detector.findHands(video_img)

            # ADDING WINDOW WITH WHITEBOARD & CAMERA
            h, w, _ = background.shape
            hs, ws = int(video_img.shape[0]/6) , int(video_img.shape[1]/6)
            mini_cam = cv2.resize(video_img, (ws, hs))
            background[0:hs,w-ws:w] = mini_cam

            # GESTURE RECOGNITION
            if hands and command_pause is False:
                hand = hands[0]
                fingers_up = detector.fingersUp(hand)
                cx, cy = hand["center"]
                lmlist = hand["lmList"]
                
                ### range of movement ###
                x_val = int(np.interp(lmlist[8][0], [wCam/2, wCam-100], [0, wCam]))
                y_val = int(np.interp(lmlist[8][1], [200, hCam-200], [0, hCam]))
                index_finger = x_val, y_val

                ### pointer command ###
                if fingers_up == [0,1,1,0,0]:
                    cv2.circle(background, index_finger, 4, (0,0,255), cv2.FILLED)
                
                ### anotation command ###
                if fingers_up == [0,1,0,0,0]:
                    if annotations_start == False:
                        annotations_start = True
                        annotations_index +=1
                        annotations.append([])
                    cv2.circle(background, index_finger, 4, (0,0,255), cv2.FILLED)
                    annotations[annotations_index].append(index_finger)  
                else:
                    annotations_start = False

                ### erase last annotation command ###
                if (fingers_up == [0,1,1,1,0]) & (annotations != [[]]):
                    annotations.pop(-1)
                    annotations_index -=1
                    command_pause = True

                ### erase all annotations command ###
                if (fingers_up == [0,0,0,0,0]) & (annotations != [[]]):
                    annotations, annotations_index, annotations_start = clear_annotations()
                    command_pause = True

            # ANNOTATION DISPLAY
            for i in range(1,len(annotations)):
                for j in range(1,len(annotations[i])):
                    cv2.line(background, annotations[i][j-1], annotations[i][j], (0,0,0), 5)

            # COMMAND PAUSE
            if command_pause == True:
                time_paused +=1
                if time_paused > 20:
                    command_pause = False
                    time_paused = 0

            # # DISPLAY
            # cv2.imshow("White Board", background)

            # # BREAK KEY
            # key = cv2.waitKey(1)
            # if key == ord("q"):
            #     break

            # # RELEASING CAMERA & CLOSING WINDOWS
            # cap.release()
            # cv2.destroyAllWindows()

            ret, buffer = cv2.imencode('.jpg', background)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')