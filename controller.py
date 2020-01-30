#!/usr/bin/python3

import math

class Controller:
    _x1 = 320.0
    _y1 = 480.0
    _x2 = 320.0
    _y2 = 380.0

    #PID constants
    kp = 1
    ki = 0.1
    kd = 0.2

    lastError = 0
    totalError = 0
    '''
    def controller(x1:float, y1:float, x2:float, y2:float):
        basic = basic_compensation(x1,y1,x2,y2)

    def basic_compensation(x1:float, y1:float, x2:float, y2:float)->float:
        #center the line vector so that both vectors start at the same point
        xdiff = _x1 - x1
        x1 += xdiff
        x2 += xdiff
        #scale the vectors to the same length
        temp_sum = (x2-x1)*(x2-x1)+(y1-y2)*(y1-y2)
        length = math.sqrt(temp_sum)
        print("length: "+str(length))
        xlen = ((x1-x2)/length)*100
        ylen = ((y1-y2)/length)*100
        print("xlen: "+str(xlen))
        print("ylen: "+str(ylen))
        #calculate the distance betwen the endpoints
        x2 = x1-xlen
        y2 = y1-ylen
        if x2 > _x2:
            dist = math.sqrt((abs(x2-_x2)*abs(x2-_x2)+((y2-_y2)*(y2-_y2))))
        else:
            dist = - math.sqrt((abs(x2-_x2)*abs(x2-_x2)+((y2-_y2)*(y2-_y2))))
        print("dist: "+str(dist))
        print("-------------------------------------------")
        return 0
    '''
    def pid(self,value:int)->float:
        error = abs(value-75)
        self.totalError += error

        proportional = error * self.kp
        integral = self.totalError * self.ki
        derivative = (error - self.lastError) * self.kd

        pidReturn = proportional + integral + derivative
        print("value: "+str(value)+" | error: "+str(error)+" | lastError: "+str(self.lastError)+" | totalError: "+str(self.totalError))
        print("PID: "+str(pidReturn)+" | P: "+str(proportional)+" | I: "+str(integral)+" | D: "+str(derivative))
        print("---------------------------------------------")

        if(error == 0):
            self.totalError = 0
        if(self.totalError > 50):
            self.totalError = 50

        self.lastError = error
        return pidReturn