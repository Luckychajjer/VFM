from math import floor
import os,shutil
import time
import cvzone
import cv2
from cvzone.PoseModule import PoseDetector
from temp import result_display

cap = cv2.VideoCapture(0)
detector = PoseDetector()

shirtFolderPath = "Resources/Shirts"
listShirts = os.listdir(shirtFolderPath)

fixedRatio = 262 / 190  # widthOfShirt/widthOfPoint11to12
shirtRatioHeightWidth = 581 / 440 #size of t shirt in pixels
imageNumber = 0
backbutton= cv2.imread("Resources/back-button.jpg",cv2.IMREAD_COLOR)
buybutton= cv2.imread("Resources/reclick.jpg",cv2.IMREAD_COLOR)
# buybutton = cv2.resize(buybutton,(90,45))
poslist = [[90,330,40,220],[90,330,240,420],[430,670,40,220],[430,670,240,420]]
new_frame_time=0
prev_frame_time =0
counterRight = 0
counterLeft = 0
selectionSpeed = 20
count =0

cartfolder = 'cart'

# if os.path.exists(cartfolder):
#     shutil.rmtree(cartfolder)
#     os.makedirs('cart')

size = result_display()

while True:
    img_white = cv2.imread("startpage.jpg", cv2.IMREAD_COLOR)
    success, img = cap.read()
    img = cv2.flip(img,1)
    img= cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    img_white = cv2.rotate(img_white, cv2.ROTATE_90_CLOCKWISE)#rotate camera image by 90 ccw
    frame1 = detector.findPose(img,draw=False)
    lmList, bboxInfo = detector.findPosition(frame1, bboxWithHands=False, draw=False)
    if lmList:
        lm11 = lmList[11][:2]
        lm12 = lmList[12][:2]
        leftind = lmList[19]
        rightind = lmList[20]
        imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)
        widthOfShirt = int((lm11[0] - lm12[0]) * fixedRatio)
        currentScale = (lm11[0] - lm12[0]) / 190
        offset = int(44 * currentScale), int(48 * currentScale)

        try:
            imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtRatioHeightWidth)))
            img_white = cvzone.overlayPNG(img_white, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
        except:
            pass

        cv2.putText(img_white,"^",(leftind[0],leftind[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(img_white,"^",(rightind[0],rightind[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 1, cv2.LINE_AA)
        if rightind[0] <= 100 and rightind[0] >=10 and rightind[1]<=145 and rightind[1]>=20:
            time.sleep(0.75) #within cart page
            cv2.destroyAllWindows()
            cartlist = os.listdir("cart")
            lencart = 4 if len(cartlist)>4 else len(cartlist)
            while True:
                success, img_white = cap.read()
    
                img_white = cv2.flip(img_white,1) #flip verticaly or y axis 
                img_white = cv2.rotate(img_white, cv2.ROTATE_90_CLOCKWISE)#rotate camera image by 90 ccw
                frame1 = detector.findPose(img_white,draw=False)
                lmList, bboxInfo = detector.findPosition(frame1, bboxWithHands=False, draw=False)
                if lmList:
                    leftind = lmList[19]
                    img = cv2.imread("black-screen-new-c.jpg", cv2.IMREAD_COLOR)
                    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

                    for i in range(lencart):
                        img[poslist[i][1]+25:poslist[i][1]+70,poslist[i][2]:poslist[i][2]+90] = buybutton
                        info = cartlist[i].strip('.jpg')
                        img_img = cv2.imread(os.path.join(cartfolder, cartlist[i]), cv2.IMREAD_UNCHANGED)
                        img_img = cv2.resize(img_img,(180,240))
                        img[poslist[i][0]:poslist[i][1],poslist[i][2]:poslist[i][3]] = img_img
                        cv2.putText(img,info,(poslist[i][2]+5,poslist[i][1]+20), cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,255),1, cv2.LINE_AA)
                        cv2.putText(img,f'Size:{size}',(poslist[i][2]+100,poslist[i][1]+50), cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),1, cv2.LINE_AA)
                        
                    leftind[0] = int(leftind[0]*0.95)
                    leftind[1] = int(leftind[1]*1.34)
                    cv2.putText(img,"^",(leftind[0],leftind[1]), cv2.FONT_HERSHEY_PLAIN, 1, (100, 255, 0), 1, cv2.LINE_AA)
                    if leftind[0] <= 80 and leftind[0] >=10 and leftind[1]<=125 and leftind[1]>=20:  
                        break
                   

                    cv2.namedWindow("Image window", cv2.WND_PROP_FULLSCREEN) #for full screen
                    cv2.setWindowProperty("Image window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                    cv2.resizeWindow("Image window", 1080,1920)      
                    cv2.imshow("Image window",img)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            
            time.sleep(0.75)
            cv2.destroyAllWindows()

        if leftind[0] <= 450 and leftind[0] >=360 and leftind[1]<=145 and leftind[1]>=20:
            prev_frame_time  = time.time()#within camera page
            cv2.destroyAllWindows()
            while(new_frame_time - prev_frame_time <3): 
                img_img = cv2.imread("black-screen.jpg", cv2.IMREAD_COLOR)
                new_frame_time = time.time()
                x = floor((new_frame_time-prev_frame_time))
                x = 3-x
                cv2.putText(img_img,f"{x}",(300,350), cv2.FONT_HERSHEY_DUPLEX, 12, (100, 255, 0), 10, cv2.LINE_AA)
                cv2.namedWindow("Image window", cv2.WND_PROP_FULLSCREEN) #for full screen
                cv2.setWindowProperty("Image window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.resizeWindow("Image window", 1080,1920)
                cv2.imshow("Image window",img_img)
                cv2.waitKey(1)

            cv2.destroyAllWindows()
            success, img = cap.read()
            img = cv2.flip(img,1)
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            img= cvzone.overlayPNG(img, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
            
            info = listShirts[imageNumber].strip('.png')
            cv2.imwrite(os.path.join(cartfolder , f'{info}.jpg'), img)
          
        if rightind[0] <= 60 and rightind[0] >=20 and rightind[1]<=470 and rightind[1]>=420 :
            counterRight += 1 #lefthand gesture
            cv2.ellipse(img_white, (40,434), (21,21), 0, 0,
                        counterRight * selectionSpeed, (0, 255, 0), 10)
            if counterRight * selectionSpeed > 360:
                counterRight = 0
                if imageNumber >0:
                    imageNumber -= 1
                else:
                    imageNumber = len(listShirts) - 1

        elif leftind[0] <=450  and leftind[0] >=395 and leftind[1]<=470 and leftind[1]>=420 :
            counterLeft += 1 #righthand gesture
            cv2.ellipse(img_white, (418,432), (21,21), 0, 0,
                        counterLeft * selectionSpeed, (0, 255, 0), 10)
            if counterLeft * selectionSpeed > 360:
                counterLeft = 0
                if imageNumber < len(listShirts) - 1:
                    imageNumber += 1
                else:
                    imageNumber = 0

        else:
            counterRight = 0
            counterLeft = 0
    
    cv2.namedWindow('Pose Detection', cv2.WND_PROP_FULLSCREEN) #for full screen
    cv2.setWindowProperty('Pose Detection', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN) # for fullscreen
    cv2.resizeWindow('Pose Detection', 1080,1920) #1920,1080 or  1080,720 for horizontal

    # cv2.namedWindow('Pose Detection-1', cv2.WND_PROP_FULLSCREEN) #for full screen
    # cv2.setWindowProperty('Pose Detection-1', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN) # for fullscreen
    # cv2.resizeWindow('Pose Detection-1', 1920,1080)

    # cv2.imshow("Pose Detection-1",img)
    cv2.imshow("Pose Detection",img_white)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()