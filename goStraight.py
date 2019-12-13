#!/usr/bin/env python

import rospy
import math 
from math import sin, cos, pi
import tf
from geometry_msgs.msg import Twist, Pose, Point, Quaternion, Vector3
from nav_msgs.msg import Odometry
class GoStraight():
    def __init__(self):
	
	x=0.0
	y=0.0
	th=0.0

	vx=0.1
	vy=-0.1
	vth=0.1

	current_time=rospy.Time.now()
	last_time = rospy.Time.now()
	
        # initiliaze
        rospy.init_node('GoStraight', anonymous=False)

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
		current_time=rospy.Time.now()
		dt = current_time-last_time
		delta_x = (vx*cos(th) - vy*sin(th))*dt
		delta_y = (vy*cos(th) + vx*sin(th))*dt
		delta_th =  vth*dt

		x=+delta_x
		y+=delta_y
		th+=delta_th
		odom_quat = tf.transformations.quaternion_from_euler(0, 0, th)

		odom_broadcaster.sendTransform(
		(x, y, 0.),
		odom_quat,
		current_time,
		"base_link",
		"odom"
		)

		odom = Odometry()
		odom.header.stamp = current_time
		odom.header.frame_id = "odom"

		# set the position
		odom.pose.pose = Pose(Point(x, y, 0.), Quaternion(*odom_quat))

		# set the velocity
		odom.child_frame_id = "base_link"
		odom.twist.twist = Twist(Vector3(vx, vy, 0), Vector3(0, 0, vth))

		# publish the message
		odom_pub.publish(odom)

		last_time = current_time
       		r.sleep()
                        
    

    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop TurtleBot")
	# a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
        self.odom_pub.publish(Odometry())
	# sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
        rospy.sleep(1)

 
if __name__ == '__main__':
    try:
        GoStraight()
    except Exception as e:
	print(e)
        rospy.loginfo("GoStraight node terminated.")

