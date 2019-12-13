#!/usr/bin/env python

'''
Copyright (c) 2015, Mark Silliman
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

# A very basic TurtleBot script that moves TurtleBot forward indefinitely. Press CTRL + C to stop.  To run:
# On TurtleBot:
# roslaunch turtlebot_bringup minimal.launch
# On work station:
# python goforward.py

import rospy
from geometry_msgs.msg import Twist
from kobuki_msgs.msg import BumperEvent
class GoForward():
    def __init__(self):

	self.safety=0
	self.bhit=0
        # initiliaze
        rospy.init_node('GoForward', anonymous=False)

	# tell user how to stop TurtleBot
	rospy.loginfo("To stop TurtleBot CTRL + C")

        # What function to call when you ctrl + c    
        rospy.on_shutdown(self.shutdown)
        
	# Create a publisher which can "talk" to TurtleBot and tell it to move
        # Tip: You may need to change cmd_vel_mux/input/navi to /cmd_vel if you're not using TurtleBot2
        self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
     
	sub = rospy.Subscriber("/mobile_base/events/bumper", BumperEvent, self.BumperEventCallback)
	#TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ
        r = rospy.Rate(5);

        # Twist is a datatype for velocity
        move_cmd = Twist()
	# let's go forward at 0.2 m/s
        move_cmd.linear.x = 0.2
	# let's turn at 0 radians/s
	move_cmd.angular.z = 0

	# as long as you haven't ctrl + c keeping doing...
        while not rospy.is_shutdown():
	    sub = rospy.Subscriber("/mobile_base/events/bumper", BumperEvent, self.BumperEventCallback)
	    if(self.bhit>0 and self.safety==0):
		print("bumper is hit, not moving forward")
		self.safety=1
		self.cmd_vel.publish(Twist())
	    elif(self.bhit>0 and self.safety==1):
                print("bumper still hit")
                self.cmd_vel.publish(Twist())
	    elif(self.bhit==0 and self.safety==1):
		print("bumper was hit but now unhit")
		print("safety value is %d", %(self.safety))
		for i in range (0,10):
			r.sleep()
		self.safety=2	
	    elif(self.bhit==0 and self.safety==2)
                print("safety value is %d", %(self.safety))
                self.safety=0
                move_cmd.linear.x=0.2
		self.cmd_vel.publish(move_cmd)
	    elif (self.bhit==0 and self.safety==0):
		move_cmd.linear.x=0.2
		self.cmd_vel.publish(move_cmd)
	    else:
                self.safety=1
            r.sleep()
                        
    def BumperEventCallback(self, data):
	if(data.state==BumperEvent.RELEASED):
		state="unhit"
		if(data.bumper==BumperEvent.LEFT):
			self.bhit=set_bit(self.bhit,2,0)
		elif(data.bumper==BumperEvent.CENTER):
			self.bhit=set_bit(self.bhit,1,0)
		else:
			self.bhit=set_bit(self.bhit,0,0)    
	else:
		state="hit"
		if(data.bumper==BumperEvent.LEFT):
                        self.bhit=set_bit(self.bhit,2,1)
		elif(data.bumper==BumperEvent.CENTER):			
			self.bhit=set_bit(self.bhit,1,1)
		else:
			self.bhit=set_bit(self.bhit,0,1)  
	rospy.loginfo("%s bumper was %s." %(data.bumper,state))

    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop TurtleBot")
	# a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
        self.cmd_vel.publish(Twist())
	# sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
        rospy.sleep(1)

def set_bit(v,index,x):
	mask=1<<index
	v &= ~mask
	if x:
		v|=mask
	return v
 
if __name__ == '__main__':
    try:
        GoForward()
    except Exception as e:
	print(e)
        rospy.loginfo("GoForward node terminated.")

