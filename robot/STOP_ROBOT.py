from RobotCommunication import SerialCommands

robot = SerialCommands('/dev/ttyAMA0',115200)
print robot.init()


