import struct, time
import kbhit
from RobotCommunication import SerialCommands
import pickle

robot = SerialCommands('/dev/ttyAMA0',115200)
kb = kbhit.KBHit()
enc = open('encoder.data', 'w')
print robot.init()

distance = 2
ticks = distance*100*61.7


old = struct.unpack('<ii',robot.readEncoders())
robot.startLineFollowing(50)

done = 0
while (done < ticks): 
        
        data =  robot.readEncoders()
        if len(data) == 8:
	        new = struct.unpack('<ii',data)
	        done = ((new[0]-old[0]))
	        #print dist
	        time.sleep(0.05)
        
        
'''
    data =  robot.readEncoders()
    if len(data) == 8:
        val = struct.unpack('<ii',data)
        pickle.dump(val, enc)
        
    time.sleep(0.1)
    
       
    if kb.kbhit():  ### check if the key is pressed
        key = kb.getch()
        if key == 'l':   ##if pressed "r" go from left to right lane
            old = struct.unpack('<ii',robot.readEncoders())
            robot.startLineFollowing(50)
            
        if key == 's':   ##if pressed "l" go from right to left lane
            robot.stopLineFollowing()
            robot.init()
            new = struct.unpack('<ii',robot.readEncoders())
            dist = (((new[0]-old[0])+(new[1]-old[1]))/2)*0.0154
            print old
            print new
            print dist
            
        if key == 'q':
            robot.init()
            break
'''     
robot.stopLineFollowing
robot.init()
print 'claculated ticks',ticks
print (new[0]-old[0])
