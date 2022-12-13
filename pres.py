# FUNCTION TO SPLIT PRESENTATION PAGES INTO PNG
def pres_split():
    from pdf2image import convert_from_path
    from pathlib import Path
    import os
    import glob

    # Clearing Presentation Folder
    files = glob.glob('presentation/*')
    for f in files:
        os.remove(f)
    
    # Store Pdf with convert_from_path function
    images = convert_from_path('static/assets/pres/pres.pdf')
    
    # Path for saving pngs
    save_path = Path("presentation")

    for i in range(len(images)):
        # Save pages as png
        images[i].save(save_path/ f'{i+1}.png', 'PNG')



# FUNCTION TO CONTROL PRESENTATION
def presentation():
    import os
    import cv2
    import numpy as np
    from cvzone.HandTrackingModule import HandDetector
    import autopy

    # VARIABLES
    wCam, hCam = 1280, 720
    wScr, hScr = autopy.screen.size()
    slide = 0
    command_line = 400
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
            # IMPORTING & DISPLAYING PRESENTATION
            path_presentation = sorted(os.listdir("presentation"), key=len)
            path_slide = os.path.join("presentation", path_presentation[slide])
            current_slide = cv2.imread(path_slide)
            current_slide = cv2.resize(current_slide, (int(wScr), int(hScr)))

            # HAND RECOGNITION & COMMAND ZONE
            hands, video_img = detector.findHands(video_img)
            cv2.line(video_img,(0, command_line), (wCam, command_line), (0,0,0), 5)

            # ADDING WINDOW WITH PRESENTATION & CAMERA
            h, w, _ = current_slide.shape
            hs, ws = int(video_img.shape[0]/6) , int(video_img.shape[1]/6)
            pres_cam = cv2.resize(video_img, (ws, hs))
            current_slide[0:hs,w-ws:w] = pres_cam

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

                if cy<=command_line: 

                    ### left command ###
                    if (fingers_up == [1,0,0,0,0]) & (slide>0):
                        annotations, annotations_index, annotations_start = clear_annotations()
                        slide -=1
                        command_pause = True

                    ### right command ###
                    if (fingers_up == [0,0,0,0,1]) & (slide<(len(path_presentation)-1)):
                        annotations, annotations_index, annotations_start = clear_annotations()
                        slide +=1
                        command_pause = True

                ### pointer command ###
                if fingers_up == [0,1,1,0,0]:
                    cv2.circle(current_slide, index_finger, 4, (0,0,255), cv2.FILLED)
                
                ### anotation command ###
                if fingers_up == [0,1,0,0,0]:
                    if annotations_start == False:
                        annotations_start = True
                        annotations_index +=1
                        annotations.append([])
                    cv2.circle(current_slide, index_finger, 4, (0,0,255), cv2.FILLED)
                    annotations[annotations_index].append(index_finger)  
                else:
                    annotations_start = False

                ### erase command ###
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
                    cv2.line(current_slide, annotations[i][j-1], annotations[i][j], (0,0,0), 5)

            # COMMAND PAUSE
            if command_pause == True:
                time_paused +=1
                if time_paused > 20:
                    command_pause = False
                    time_paused = 0

            # # DISPLAY
            # cv2.imshow("Presentation", current_slide)

            # # BREAK KEY
            # key = cv2.waitKey(1)
            # if key == ord("q"):
            #     break

            # # RELEASING CAMERA & CLOSING WINDOWS
            # cap.release()
            # cv2.destroyAllWindows()

            ret, buffer = cv2.imencode('.jpg', current_slide)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')