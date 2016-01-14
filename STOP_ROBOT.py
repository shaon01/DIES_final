from RobotCommunication import SerialCommands
import time

robot = SerialCommands('/dev/ttyAMA0',115200)
#robot.resetEncoders()
#old = robot.readEncoders()
#print old
#robot.autoCalibrate()
#time.sleep(5)
print robot.init()
#robot.fixedDistance(2000)



