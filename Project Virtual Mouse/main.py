import cv2
import numpy as np
import helper
import gesture
import pyautogui

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

"""
instructions 
- after starting , the first frame captures - background ,press 'c' to capture
- next window is the captured image - press 'q' to quit
- next two window is to capture two different colors
- reference video - provided in zip
- if only second color is detected then it is used for mouse cursor movements
- if both first color and second color is detected then it is used for scrolling
- similarly click events are defined , by joining both the colors. 
"""


right_click_cnt = 0
left_click_cnt = 0
gesture_prev = None
background = None
cap1 = cv2.VideoCapture(0)

while True:
    ret1,frame1 = cap1.read()
    frame1 = cv2.flip(frame1,1)
    helper.show("frame1",frame1)
    k1 = cv2.waitKey(1) & 0xFF
    if k1 == ord('c'):
        background = frame1
        print('captured')
        print(background.shape)
        break

cap1.release()
cv2.destroyAllWindows() 

while True:
    helper.show('background',background)
    k2 = cv2.waitKey(1) & 0xFF
    if k2 == ord('q'):
        break
cv2.destroyAllWindows() 

hand_hist = helper.capture_histogram() #captures histogramog the palm
hand_hist2 = helper.capture_histogram()

cap = cv2.VideoCapture(0)
while True:
    
    ret,frame = cap.read()
    frame = cv2.flip(frame,1)
    height,width,ch = frame.shape 
    output_window = np.zeros([height,width],dtype = np.uint8)
    
    x_i = int(1/2*width+30)
    y_i = int(1/3*height-100)
    w_i = int(1/2*width -50)
    h_i = int(2/3*height+50)
    
    top_left_corner = (x_i,y_i)
    top_right_corner = (x_i + w_i,y_i + h_i)
    color = (0,255,0)
    thickness = 1
    
    roi = frame[y_i:y_i+h_i - 2,x_i:x_i+w_i-2] # first row then column so first y1 then x1
 
    frame1 = frame.copy()
    frame1 = cv2.rectangle(frame1,top_left_corner,top_right_corner,color,thickness)
    
    
    #now we need to detect the hands
    roi_b = background[y_i:y_i+h_i - 2,x_i:x_i+w_i-2]
    ans = helper.subtractor(roi, roi_b)
    mask,mask_color,segemented_thresh = helper.detect_hand(ans,hand_hist)
    mask1,mask_color_1,segment_thresh1 =helper.detect_hand(ans,hand_hist2)
    
    contours,_ =cv2.findContours(mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours1,re = cv2.findContours(mask1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    print(len(contours))
    print(len(contours1))
    cx1 = 0
    cx2 = 0
    cy1 = 0
    cy2 = 0
    
    if(len(contours) != 0):
        largest_area_color1 = 0
        area_color1 = 0
        index_color1 = 0
        for i in range(len(contours)):
            area_color1 = cv2.contourArea(contours[i])
            if(area_color1 > largest_area_color1):
                largest_area_color1 = area_color1
                index_color1 = i
                
        x1,y1,w1,h1 = cv2.boundingRect(contours[index_color1])
        cv2.rectangle(roi, (x1,y1),(x1+w1,y1+h1),(0,255,0),2)
        centre_x1 = x1+w1/2
        centre_y1 = y1+h1/2
        cx1 = int(centre_x1)
        cy1 = int(centre_y1)
        cv2.circle(roi,(cx1,cy1),3,(0,255,255),-1)
    

    if(len(contours1) != 0):
        largest_area_color2 = 0
        area_color2 = 0
        index_color2 = 0
        for i in range(len(contours1)):
            area_color2 = cv2.contourArea(contours1[i])
            if(area_color2 > largest_area_color2):
                largest_area_color2 = area_color2
                index_color2 = i              
                
        x2,y2,w2,h2 = cv2.boundingRect(contours1[index_color2])
        cv2.rectangle(roi, (x2,y2),(x2+w2,y2+h2),(255,0,0),2)
        centre_x2 = x2+w2/2
        centre_y2 = y2+h2/2
        cx2 = int(centre_x2)
        cy2 = int(centre_y2)
        cv2.circle(roi,(cx2,cy2),3,(255,0,255),-1)
        
    gesture_present = gesture.Detect(len(contours),len(contours1),cx1,cy1,cx2,cy2)
    
    if(gesture_prev != None):
        cv2.putText(output_window,"PRESENT: " + gesture_present.gesture_name + " " + str(gesture_present.cx1) + " " + str(gesture_present.cx2),(20,30),cv2.FONT_HERSHEY_SIMPLEX ,1,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(output_window,"PREV: "  + gesture_prev.gesture_name + " " + str(gesture_prev.cx1) + " " + str(gesture_prev.cx2),(20,70),cv2.FONT_HERSHEY_SIMPLEX ,1,(255,255,255),2,cv2.LINE_AA)       
    else:
        cv2.putText(output_window,"PRESENT: " + gesture_present.gesture_name,(20,30),cv2.FONT_HERSHEY_SIMPLEX ,1,(255,255,255),2,cv2.LINE_AA)
    
    
    threshold = 3
    if(gesture_prev != None):
        G1 = gesture_present.gesture_name;
        G2 = gesture_prev.gesture_name;
        
        if(G1 == "PAUSE"):
            right_click_cnt = 0
            left_click_cnt = 0
        elif (G1 == "MOVE" and G2 == "PAUSE"): 
            pass
            #right_click_cnt = 0
            #left_click_cnt = 0
        elif (G1 == "MOVE" and G2 == "MOVE"):
            
            offset_x = gesture_present.cx2 - gesture_prev.cx2
            offset_y = gesture_present.cy2 - gesture_prev.cy2   
            if abs(offset_x) <= 5:
                offset_x = 0   
            if abs(offset_y) <=5:
                offset_y = 0  
            pyautogui.moveRel(3*offset_x,3*offset_y,duration = 0)
            #right_click_cnt = 0
            #left_click_cnt = 0
        
        elif (G1 == "RIGHT_CLICK" and G2 == "PAUSE"):
            
            if(right_click_cnt <= 0):
                pyautogui.rightClick()
                
            right_click_cnt += 1
       
        elif (G1 == "RIGHT_CLICK" and G2 == "RIGHT_CLICK"):
            
            if(right_click_cnt == 0):
                pyautogui.rightClick()
                
            right_click_cnt += 1
                     
        elif(G1 == "UP_SCROLL" or G2 == "UP_SCROLL"):
            pyautogui.scroll(10)

        
        elif(G1 == "DOWN_SCROLL" or G2 == "DOWN_SCROLL"):
            pyautogui.scroll(-10)

        
        elif(G1 == "LEFT_CLICK" and G2 == "PAUSE"):
            
            if(left_click_cnt == 0):
                pyautogui.leftClick()
                left_click_cnt+=1
            
        elif(G1 == "LEFT_CLICK" and G2 == "LEFT_CLICK"):
            
            offset_x = gesture_present.cx2 - gesture_prev.cx2
            offset_y = gesture_present.cy2 - gesture_prev.cy2   
            if abs(offset_x) <= 5:
                offset_x = 0   
            if abs(offset_y) <= 5:
                offset_y = 0
                
            if(left_click_cnt == 0):
                pyautogui.leftClick()
                
            
            if(left_click_cnt >= 5):
                pyautogui.dragRel(3*offset_x,3*offset_y, duration=0)
            
            left_click_cnt += 1;
        
        


    helper.show("frame1",frame1)
    helper.show("frame",frame)
    helper.show('roi',roi)
    helper.show("output_window",output_window)
    
    gesture_prev = gesture_present

    
    k = cv2.waitKey(100)
    if k == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()


