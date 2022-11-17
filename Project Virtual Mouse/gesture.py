# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 15:28:18 2020

@author: Harshit
"""


import cv2
import numpy as np
import math


class Detect:
    
    def __init__(self,contours,contours1,cx1,cy1,cx2,cy2):
        self.contours = contours
        self.contours1 = contours1
        self.cx1 = cx1
        self.cx2 = cx2
        self.cy1 = cy1
        self.cy2 = cy2
        self.gesture_name = self.gesture_name()
    
    def gesture_name(self):
        if(self.contours == 0 and self.contours1 == 0):
            return "NONE"
        elif(self.contours != 0 and self.contours1 == 0):
            return "RIGHT_CLICK"
        elif(self.contours == 0 and self.contours1 != 0):
            return "MOVE"
        elif(self.contours !=0 and self.contours1 != 0):
            
            dist_x =self.cx2 - self.cx1
            dist_y = self.cy2 - self.cy1
            dist = ((dist_x)**2 + (dist_y**2))**(0.5)
            if dist >= 160 and self.cy1 > self.cy2:
                return "DOWN_SCROLL"
            elif dist >= 160 and self.cy1 <= self.cy2:
                return "UP_SCROLL"
            elif dist>= 60:
                return "PAUSE"
            elif dist >= 20:
                return "LEFT_CLICK"
            else:
                return "NONE"
        else :
            return "NONE"
            
            
            
    