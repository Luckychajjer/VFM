from math import floor
import os,shutil
import time
import cvzone
import cv2
from cvzone.PoseModule import PoseDetector


cap = cv2.VideoCapture(0)
detector = PoseDetector()

shirtFolderPath = "Resources/Shirts"
listShirts = os.listdir(shirtFolderPath)

fixedRatio = 262 / 190  # widthOfShirt/widthOfPoint11to12
shirtRatioHeightWidth = 581 / 440 #size of t shirt in pixels
imageNumber = 0
imgButtonRight = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)
scale_percent = 35 # percent of original size
width = int(imgButtonRight.shape[1] * scale_percent / 100)
height = int(imgButtonRight.shape[0] * scale_percent / 100)
dim = (width, height)
imgButtonRight = cv2.resize(imgButtonRight,dim)
imgButtonLeft = cv2.resize(imgButtonLeft,dim)
# scale_percent = 
cartbutton = cv2.imread("Resources/shopping-cart-128.png",cv2.IMREAD_UNCHANGED)
cartbutton = cv2.resize(cartbutton,(64,64))
camerabutton = cv2.imread("Resources/camera.png",cv2.IMREAD_UNCHANGED)
camerabutton = cv2.resize(camerabutton,(64,64))

headline= cv2.imread("Resources/wardrobe.jpg",cv2.IMREAD_COLOR)
backbutton= cv2.imread("Resources/back-button.jpg",cv2.IMREAD_COLOR)
buybutton= cv2.imread("Resources/buy-now.jpg",cv2.IMREAD_COLOR)
buybutton = cv2.resize(buybutton,(64,64))
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

while True:
    # img_white = cv2.imread("white-screen.jpg", cv2.IMREAD_COLOR)
    success, img_white = cap.read()
    
    img_white = cv2.flip(img_white,1) #flip verticaly or y axis 
    img_white = cv2.rotate(img_white, cv2.ROTATE_90_CLOCKWISE)#rotate camera image by 90 ccw
    frame1 = detector.findPose(img_white,draw=False)
    lmList, bboxInfo = detector.findPosition(frame1, bboxWithHands=False, draw=False)
    img_white = cvzone.overlayPNG(img_white,cartbutton, (0,150))
    img_white = cvzone.overlayPNG(img_white,camerabutton, (400,150))
    img_white = cvzone.overlayPNG(img_white, imgButtonRight, (420,300))
    img_white= cvzone.overlayPNG(img_white, imgButtonLeft, (0,300))
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
        if leftind[0] <= 60 and leftind[0] >=10 and leftind[1]<=220 and leftind[1]>=160:
            time.sleep(0.75)
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
                    img = cv2.imread("white-screen.jpg", cv2.IMREAD_COLOR)
                    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
                    img[700:828,320:448] = backbutton
                    img[0:80,0:460] = headline

                    for i in range(lencart):
                        img[poslist[i][1]+25:poslist[i][1]+89,poslist[i][2]:poslist[i][2]+64] = buybutton
                        info = cartlist[i].strip('.jpg')
                        img_img = cv2.imread(os.path.join(cartfolder, cartlist[i]), cv2.IMREAD_UNCHANGED)
                        img_img = cv2.resize(img_img,(180,240))
                        img[poslist[i][0]:poslist[i][1],poslist[i][2]:poslist[i][3]] = img_img
                        img = cv2.rectangle(img,(poslist[i][2],poslist[i][0]),(poslist[i][3],poslist[i][1]),(0,0,0), 1)
                        cv2.putText(img,info,(poslist[i][2]+5,poslist[i][1]+20), cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0),1, cv2.LINE_AA)
                        
                    leftind[0] = int(leftind[0]*0.95)
                    leftind[1] = int(leftind[1]*1.34)
                    cv2.putText(img,"^",(leftind[0],leftind[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 1, cv2.LINE_AA)
                    if leftind[0] <= 370 and leftind[0] >=280 and leftind[1]<=800 and leftind[1]>=680:
                        break

                    cv2.namedWindow("Image window", cv2.WND_PROP_FULLSCREEN) #for full screen
                    cv2.setWindowProperty("Image window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                    cv2.resizeWindow("Image window", 1080,1920)
                    cv2.imshow("Image window",img)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            
            time.sleep(0.75)
            cv2.destroyAllWindows()

        if leftind[0] <= 450 and leftind[0] >=360 and leftind[1]<=220 and leftind[1]>=160:
            prev_frame_time  = time.time()
            cv2.destroyAllWindows()
            while(new_frame_time - prev_frame_time <3): 
                img_img = cv2.imread("white-screen.jpg", cv2.IMREAD_COLOR)
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
          
        if rightind[0] <= 60 and rightind[0] >=20 and rightind[1]<=350 and rightind[1]>=310 :
            counterRight += 1
            cv2.ellipse(img_white, (23,323), (23,23), 0, 0,
                        counterRight * selectionSpeed, (0, 255, 0), 10)
            if counterRight * selectionSpeed > 360:
                counterRight = 0
                if imageNumber >0:
                    imageNumber -= 1
                else:
                    imageNumber = len(listShirts) - 1

        elif leftind[0] <=450  and leftind[0] >=405 and leftind[1]<=350 and leftind[1]>=310 :
            counterLeft += 1
            cv2.ellipse(img_white, (443,323), (23,23), 0, 0,
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

    # cv2.imshow("Pose Detection-1",img_white)
    cv2.imshow("Pose Detection",img_white)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()