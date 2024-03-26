import cv2
import numpy as np
import math

def show(window_name,image_array):
    
    '''
    
    Returns

    Parameters
    ----------
    window_name : STRING
        The window name you to show.
    image_array : np.array() image file.
        Image file  you want to show on windows.

    -------
    None.

    '''  
    cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
    cv2.imshow(window_name,image_array)

def subtractor(roi,roi_b):
    roi_bw = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
    roi_b_bw = cv2.cvtColor(roi_b,cv2.COLOR_BGR2GRAY)
    
    i = cv2.absdiff(roi_b_bw, roi_bw)
    _,i = cv2.threshold(i,10,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    kernel =  np.ones((4,4),np.uint8)
    i = cv2.dilate(i, kernel, iterations=2)
    
    #show("i",i)
    
    ans = cv2.bitwise_and(roi,roi,mask = i)
    
    return ans

def capture_histogram(source = 0):
    object_color = None
    cap = cv2.VideoCapture(source)
    while True:
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (1000, 600))

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, "Place region of the hand inside box and press `c`",
                    (5, 50), font, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.rectangle(frame, (500, 100), (580, 180), (105, 105, 105), 2)
        box = frame[105:175, 505:575]

        cv2.imshow("Capture Histogram", frame)
        key = cv2.waitKey(10)
        if key == ord('c'):
            object_color = box
            cv2.destroyAllWindows()
            break
        if key == 27:
            cv2.destroyAllWindows()
            cap.release()
            break
    object_color_hsv = cv2.cvtColor(object_color, cv2.COLOR_BGR2HSV)
    object_hist = cv2.calcHist([object_color_hsv], [0, 1], None,[12, 15], [0, 180, 0, 256])
    cv2.normalize(object_hist, object_hist, 0, 255, cv2.NORM_MINMAX)
    cap.release()
    return object_hist


def locate_object(frame, object_hist):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # apply back projection to image using object_hist as
    # the model histogram
    object_segment = cv2.calcBackProject(
        [hsv_frame], [0, 1], object_hist, [0, 180, 0, 256], 1)

    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    cv2.filter2D(object_segment, -1, disc, object_segment)

    _, segment_thresh = cv2.threshold(
        object_segment, 30, 255, cv2.THRESH_BINARY)

    # apply some image operations to enhance image
    kernel =  np.ones((5,5),np.uint8)
    kernel_e = np.ones((4,4),np.uint8)
    eroded = cv2.erode(segment_thresh, kernel, iterations=1)
    dilated = cv2.dilate(eroded, kernel_e, iterations=1)
    closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)

    # masking
    masked = cv2.bitwise_and(frame, frame, mask=closing)

    return closing, masked, segment_thresh

def detect_hand(frame, hist):
    detected_hand, masked, raw = locate_object(frame, hist)
    return detected_hand,masked,raw