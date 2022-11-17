import cv2
import numpy as np
import helper
import pyautogui

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

car_pointer = helper.capture_histogram()

cap = cv2.VideoCapture(0)
while True:
    
    ret,frame = cap.read()
    frame = cv2.flip(frame,1)
    height,width,ch = frame.shape
    frame = cv2.resize(frame,(640,480), interpolation = cv2.INTER_AREA)
    frame1 = np.copy(frame)  # copy the frame for further use 
    
    roi1 = frame1[0:240,0:275]
    roi2 = frame1[0:240,280:360]
    roi3 = frame1[0:240,365:640]
    
    cv2.line(frame,(0,240),(640,240),(255,255,255),5)
    cv2.line(frame,(275,0),(275,480),(255,255,255),5)
    cv2.line(frame,(365,0),(365,480),(255,255,244),5)
    
    
    mask1,mask_color1,segemented_thresh1 = helper.detect_hand(roi1,car_pointer)
    mask2,mask_color2,segemented_thresh2 = helper.detect_hand(roi2,car_pointer)
    mask3,mask_color3,segemented_thresh3 = helper.detect_hand(roi3,car_pointer)
    
    contours1,_ =cv2.findContours(mask1,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours2,re = cv2.findContours(mask2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours3,re1 = cv2.findContours(mask3,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    
    cx1 = 0
    cx2 = 0
    cx3 = 0
    cy1 = 0
    cy2 = 0
    cy3 = 0
    
    if(len(contours1) != 0):
        largest_area_color1 = 0
        area_color1 = 0
        index_color1 = 0
        for i in range(len(contours1)):
            area_color1 = cv2.contourArea(contours1[i])
            if(area_color1 > largest_area_color1):
                largest_area_color1 = area_color1
                index_color1 = i
                
        x1,y1,w1,h1 = cv2.boundingRect(contours1[index_color1])
        cv2.rectangle(roi1, (x1,y1),(x1+w1,y1+h1),(255,0,0),2)
        centre_x1 = x1+w1/2
        centre_y1 = y1+h1/2
        cx1 = int(centre_x1)
        cy1 = int(centre_y1)
        cv2.circle(roi1,(cx1,cy1),3,(255,0,255),-1)
        pyautogui.keyDown('w')  
        pyautogui.press('a',presses = 1)
        pyautogui.keyUp('w')
    

    elif(len(contours2) != 0):
        largest_area_color2 = 0
        area_color2 = 0
        index_color2 = 0
        for i in range(len(contours2)):
            area_color2 = cv2.contourArea(contours2[i])
            if(area_color2 > largest_area_color2):
                largest_area_color2 = area_color2
                index_color2 = i              
                
        x2,y2,w2,h2 = cv2.boundingRect(contours2[index_color2])
        cv2.rectangle(roi2, (x2,y2),(x2+w2,y2+h2),(255,0,0),2)
        centre_x2 = x2+w2/2
        centre_y2 = y2+h2/2
        cx2 = int(centre_x2)
        cy2 = int(centre_y2)
        cv2.circle(roi2,(cx2,cy2),3,(255,0,255),-1)
        pyautogui.press('w',presses = 1)
        
    
    elif(len(contours3) != 0):
        largest_area_color3 = 0
        area_color3 = 0
        index_color3 = 0
        for i in range(len(contours3)):
            area_color3 = cv2.contourArea(contours3[i])
            if(area_color3 > largest_area_color3):
                largest_area_color3 = area_color3
                index_color3 = i              
                
        x3,y3,w3,h3 = cv2.boundingRect(contours3[index_color3])
        cv2.rectangle(roi3, (x3,y3),(x3+w3,y3+h3),(255,0,0),2)
        centre_x3 = x3+w3/2
        centre_y3 = y3+h3/2
        cx3 = int(centre_x3)
        cy3 = int(centre_y3)
        cv2.circle(roi3,(cx3,cy3),3,(255,0,255),-1)
        pyautogui.keyDown('w') 
        pyautogui.press('d',presses = 1)
        pyautogui.keyUp('w')
        
        
    

    
    
    helper.show('roi1',roi1)
    helper.show("roi2",roi2)
    helper.show("roi3",roi3)
    helper.show("frame",frame)
    helper.show("frame1",frame1)
    

    
    
    
    k = cv2.waitKey(1)
    if k == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
    
    
    
    




