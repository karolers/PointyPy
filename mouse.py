# FUNCTION TO CONTROL MOUSE
def mouse():
    import cv2
    import numpy as np
    import autopy
    from cvzone.HandTrackingModule import HandDetector

    # VARIABLES
    wCam, hCam = 1280, 720
    wScr, hScr = autopy.screen.size()
    smoothing = 7
    plocX, plocY = 0,0
    clocX, clocY = 0,0

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
            # HAND & GESTURE RECOGNITION
            hands, video_img = detector.findHands(video_img)

            # GESTURE RECOGNITION
            if hands:
                hand = hands[0]
                fingers_up = detector.fingersUp(hand)
                lmlist = hand["lmList"]
                bbox = hand["bbox"]

                ### position of index and middle fingers ###
                if len(lmlist) != 0:
                    x1, y1 = lmlist[8][0], lmlist[8][1]
                    x2, y2 = lmlist[12][0], lmlist[12][1]

                ### moving mouse ###
                if fingers_up[1]==1 and fingers_up[2]==0:

                    ### range of movement ###
                    x3 = int(np.interp(x1, [wCam/2, wCam-100], [0, wScr]))
                    y3 = int(np.interp(y1, [200, hCam-200], [0, hScr]))

                    ### smoothing ###
                    clocX = plocX + (x3 - plocX)/smoothing
                    clocY = plocY + (y3 - plocY)/smoothing

                    ### mooving ###
                    autopy.mouse.move(clocX, clocY)
                    cv2.circle(video_img, (x1, y1), 15, (255,0,255), cv2.FILLED)
                    plocX, plocY = clocX, clocY

                ### clicking ###
                if fingers_up[1]==1 and fingers_up[2]==1:
                    length, info, video_img = detector.findDistance((x1, y1), (x2, y2), video_img)
                    autopy.mouse.toggle(autopy.mouse.Button.LEFT, False)

                    if length>40:
                        cv2.circle(video_img, ((x1+x2)//2, (y1+y2)//2), 15, (0,255,0), cv2.FILLED)
                        autopy.mouse.click()
                    
                ### clicking and draging ###
                if fingers_up[1]==1 and fingers_up[2]==1 and fingers_up[3]==1:
                    autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)

            # # DISPLAY
            # cv2.imshow("Camera", video_img)

            # # BREAK KEY
            # key = cv2.waitKey(1)
            # if key == ord("q"):
            #     break

            # # RELEASING CAMERA & CLOSING WINDOWS
            # cap.release()
            # cv2.destroyAllWindows()

            ret, buffer = cv2.imencode('.jpg', video_img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')