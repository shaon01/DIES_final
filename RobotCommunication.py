#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Library usage example :

# from RobotCommunication import SerialCommands
# robot = SerialCommands('/dev/ttyAMA0',115200)
# print robot.init()

# functions :
# init() -> 6
# readRawIRSensors() -> 10
# readCalibratedIRSensors() -> 10
# calibrateIRSensors() -> 10
# resetIRCalibration() -> 0
# getLineEstimatedPosition() -> 2
# readEncoders() -> 8
# resetEncoders() -> 0      /!\ Returns Nothing but Returns 'R' when done ... DOCUMENTATION ERROR
# autoCalibrate() -> 1 (Returns 'c' when done)
# startLineFollowing(max_speed, a, b, c, d) -> 0
# stopLineFollowing() -> 0
# setMotor1Speed(speed) -> 0    /!\ Speeds between -127 and 127 (0 is stop)
# setMotor2Speed(speed) -> 0    /!\ Speeds between -127 and 127 (0 is stop)

__version__ = "0.2"
__author__ = "Group 1"
__status__ = "Development"

import serial
import struct
import time

##for cruise control
cruise_distance = 500 #the distance we want to maintain in mm
v_max =100 ##  maximum speed in mm/s. motor speed 100 = 155 mm/s 
v_curr = 10
a_max = 16
d_a_max = 10
class SerialCommands(object):
    def __init__(self, hardware, com_speed):
        self.hardware = hardware
        self.com_speed = com_speed
        self.previous_speed=0
        self.previous_distance=2000

    """
    Sends the slave name and code version, e.g. “4pi1.0”. This command also sets
    motor speeds to 0 and stops PID line following, if active, so it is useful
    as an initialization command.
    """
    def init(self):
        return self.sendCommand('\x81',6)

    """
    Reads all five IR sensors and sends the raw values as a sequence of two-byte
    ints, in the range 0-2000
    """
    def readRawIRSensors(self):
        return self.sendCommand('\x86',10)

    """
    Reads all five IR sensors and sends calibrated values as a sequence of
    two-byte ints, in the range 0-1000
    """
    def readCalibratedIRSensors(self):
        return self.sendCommand('\x87',10)

    """"
    Performs one round of calibration on the sensors, reads all five IR sensors,
    and sends calibrated values as a sequence of two-byte ints, in the range
    0-1000. This should be called multiple times, as the robot moves over a
    range from white to black.
    """
    def calibrateIRSensors(self):
        return self.sendCommand('\xB4',10)

    """
    Resets the calibration. This should always be used when connecting to a
    slave, in case the master reset without a slave reset, for example in case
    of a power glitch.
    """
    def resetIRCalibration(self):
        return self.sendCommand('\xB5',0)

    """
    Reads all five IR sensors using calibrated values and estimates the position
    of a black line under the robot. The value, which is sent back as a two-byte
    integer, is 0 when the line is under sensor PC0 or farther to the left, 1000
    when the line is directly under sensor PC1, up to 4000 when it is under
    sensor PC4 or farther to the right. See Section 19 of of the Pololu AVR
    Library Command Reference for the formula used to estimate position.
    """
    def getLineEstimatedPosition(self):
        return self.sendCommand('\xB6',2)

    """
    Reads the encoder values from motor 1 and 2. The value which is sent back
    is.First left encoder as 4-byte intege then right encoder as 4-byte integer.
    """
    def readEncoders(self):
        return self.sendCommand('\xB7',8)

    """
    Resets the encoder values. Returns the character ‘r’ when complete.
    """
    def resetEncoders(self):
        return self.sendCommand('\xB8',0)

    """
    Turns the robot left and right while calibrating. For use when the robot it
    positioned over a line. Returns the character ‘c’ when complete.
    """
    def autoCalibrate(self):
        return self.sendCommand('\xB8',1)

    """
    Sets up PID parameters and begins line following. The first data byte sets
    the maximum motor speed. The next four bytes, a, b, c, and d, represent the
    PID parameters. Specifically, the difference in the motor speeds will be set
    to (L-2000)×a/b + D×c/d, where L is the position of the line as described
    above, and D is the derivative of L. The integral term is not implemented in
    this program.
    """
    def startLineFollowing(self, max_speed): #### a= 20;b=127;c=0;d=1
        if (max_speed > 127):
            raise ValueError('ERROR : Max speed have to be under 127 !')
            return 1
        return self.sendCommand('\xBB'+chr(max_speed)+chr(20)+chr(127)+chr(0)+chr(1),0)

    """
    Stops PID line following, setting motor speeds to 0.
    """
    def stopLineFollowing(self):
        return self.sendCommand('\xBC',0)

    """
    Sets motor M1 turning forward with a speed of 0(off) up to +-127(full speed)
    or backward with a speed of 0 (off) up to -127 (full speed).
    This command stops the line following program.
    """
    def motor1(self,motor_speed):
        if(motor_speed < 0):
            direction = '\xC1'
        else:
            direction = '\xC2'
        return self.sendCommand(direction+chr(abs(motor_speed)),0)

    """
    Sets motor M2 turning forward with a speed of 0(off) up to +-127(full speed)
    or backward with a speed of 0 (off) up to -127 (full speed).
    This command stops the line following program.
    """
    def motor2(self,motor_speed):
        if(motor_speed < 0):
            direction = '\xC5'
        else:
            direction = '\xC6'
        return self.sendCommand(direction+chr(abs(motor_speed)),0)
    '''    
    cruiseControl will take distance to object as an input. If it has enough time to break then it will speed up
    or else start to deaccelarate.   
    '''
    def cruiseControl(self,cam_distance):   
    
        global v_curr   
        brk_dist =  cam_distance 
        ctr_dist = ((0.5*v_curr*v_curr)/d_a_max )+cruise_distance  # calculate the critcal distance
        print 'critical distance:',ctr_dist
        
        if (ctr_dist < brk_dist):   #if there is enough distance it will speed up
            v_curr = min(v_max, v_curr+a_max)
            self.startLineFollowing(int(v_curr*0.645))
           
            
        else:   #if not enough distance then starts to speed down
            v_curr = max(1, v_curr - d_a_max)
            self.startLineFollowing(int(v_curr*0.645))
            
        
        return (v_curr)
        
    def cruiseControl2(self,cam_distance):   
    
        global v_curr
     
        if(cam_distance>800):
            if(self.previous_speed>=v_curr):
                cam_distance=0
        print 'previous distance ', self.previous_distance
        print 'cam distance ', cam_distance
        print self.previous_speed, v_curr
        if(self.previous_distance>=cam_distance):
            if (self.previous_speed>=v_curr):
                print self.previous_speed, v_curr
                self.previous_speed=v_curr
                v_curr= max(1, v_curr - d_a_max)
                print self.previous_speed, v_curr

            else :
                self.previous_speed=v_curr
                v_curr=(v_curr+self.previous_speed)/2;
        else:
            self.previous_speed=v_curr
            v_curr = min(v_max, v_curr+a_max)
        self.previous_distance=cam_distance
        
        self.startLineFollowing(int(v_curr*0.645))
            
        
        return (v_curr)
        
    def fixedDistance(self,dist_to_go):   # to go a fixed distance call this function

        data = self.readEncoders()
        dist = 0
        
        while (len(data)!=8):
            data = self.readEncoders()
            time.sleep(0.1)
                    
        old = struct.unpack('<ii',data)
        data = 0
            
        self.startLineFollowing(100)
        
        while(dist <= dist_to_go):
            
            data = self.readEncoders()
            time.sleep(0.1)
            while (len(data)!=8):  
                time.sleep(0.1)         ###reading encoders
                data = self.readEncoders()
                                    
            new = struct.unpack('<ii',data)
            data = 0
                                
            dist = (((new[1]- old[1]) + (new[0] - old[0]))/2)*0.1627   # take the average of encoders and multipy by 1 tick = 0.1627mm
            print dist
        
        self.init()

    def laneChange(self,direction, speed):    ##lane switch
        self.init() 
        ### ROTATE
        self.motor1(-30*direction)
        self.motor2(30*direction)
        time.sleep(0.3)
        
        ##### SWITCH LANE
        if speed < 10:
            speed = 10          
        self.motor1(-speed)
        self.motor2(-speed)
        dist = 1000
        time.sleep(0.1)
        
        while(dist>100): #line change stops when middel sensor is less then the value
            
            data = self.readCalibratedIRSensors()
            if len(data) == 10:
                new = struct.unpack('<hhhhh',data)
                dist = new[2]
                #print new
            
            time.sleep(0.05)
                        
        self.init()
        #time.sleep(0.5)
        #self.startLineFollowing(20) ##switch to line following again 
        
    """
    USED INTERNALY TO SEND COMMANDS AND FETCH THE ANSWERS.
    /!\  USE THE FUNCTIONS ABOVE INSTEAD OF SENDING COMMANDS VIA THIS ONE  /!\
    """     
    def sendCommand(self, command, response_size):
        s = serial.Serial(self.hardware, self.com_speed, timeout=1)
        s.open()
        s.flushInput()
        s.flushOutput()
        s.write(command)
        response = False
        if (response_size > 0):
            while True:
                toRead = s.inWaiting()
                if (toRead >= response_size):
                    response = s.readline(toRead)
                    break
        s.close()
        return response

