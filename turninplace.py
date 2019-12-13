#!/usr/bin/env python

import rospy
import cmath
import tf.transformations as tft
import numpy as np
from math import sin, cos, pi, atan
from geometry_msgs.msg import Twist, Pose, Point, Quaternion, Vector3
from nav_msgs.msg import Odometry
class TurningPlaces():
    def __init__(self):

	current_time=rospy.Time.now()
	last_time = rospy.Time.now()

        th = 0.0
        vth = 0.1

	gain = 2
        # initiliaze
        rospy.init_node('TurningPlaces', anonymous=False)

	# tell user how to stop TurtleBot
	rospy.loginfo("To stop TurtleBot CTRL + C")

        # What function to call when you ctrl + c    
        rospy.on_shutdown(self.shutdown)
        
	# Create a publisher which can "talk" to TurtleBot and tell it to move
        # Tip: You may need to change cmd_vel_mux/input/navi to /cmd_vel if you're not using TurtleBot2
        
        self.odom_pub = rospy.Publisher('odom', Odometry, queue_size=10)
     
	#TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ
        r = rospy.Rate(1);
	


	# as long as you haven't ctrl + c keeping doing...
        while not rospy.is_shutdown():
                odom_sub = rospy.Subscriber('/odom', Odometry, self.callback)
		current_time=rospy.Time.now()
		dt = current_time-last_time

                delta_th = vth*dt
                th = th+delta_th
		self.omega = gain*delta_th
		self.saturate(self.omega)
		odom_quat = tft.quaternion_from_euler(0, 0, self.omega)  # or try putting th instead of self.omega here

		odom_broadcaster.sendTransform((0, 0, 0.),odom_quat,current_time,"base_link","odom")

		odom = Odometry()
		odom.header.stamp = current_time
		odom.header.frame_id = "odom"

		# set the position
		odom.pose.pose = Pose(Point(0, 0, 0.), Quaternion(*odom_quat))

		# set the velocity
		odom.child_frame_id = "base_link"
		odom.twist.twist = Twist(Vector3(0, 0, 0), Vector3(0, 0, self.omega)) # or try putting vth instead of self.omega here
	    

		# publish the message
		odom_pub.publish(odom)

		last_time = current_time
       		r.sleep()

        
    def saturate(self.omega):
        omega_max = 2
        if(self.omega>=omega_max):
            self.omega=omega_max

            
    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop TurtleBot")
	# a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
        self.odom_pub.publish(Odometry())
	# sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
        rospy.sleep(1)

 
if __name__ == '__main__':
    try:
        TurningPlaces()
    except Exception as e:
	print(e)
        rospy.loginfo("TurningPlaces node terminated.")

