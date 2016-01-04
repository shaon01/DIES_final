from RobotCommunication import SerialCommands

robot = SerialCommands('/dev/ttyAMA0',115200)
#robot.resetEncoders()
#old = robot.readEncoders()
#print old
print robot.init()


