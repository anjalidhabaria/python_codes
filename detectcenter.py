#!/usr/bin/env python

import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import String
from sensor_msgs.msg import Image

class ShowColorImage():
    def __init__(self):

        # initiliaze
        rospy.init_node('ShowColorImage', anonymous=False)

	# tell user how to stop TurtleBot
	rospy.loginfo("To stop TurtleBot CTRL + C")

        # What function to call when you ctrl + c    
        rospy.on_shutdown(self.shutdown)
        
	# Create a publisher which can "talk" to TurtleBot and tell it to move
        # Tip: You may need to change cmd_vel_mux/input/navi to /cmd_vel if you're not using TurtleBot2
        
        self.image_pub = rospy.Publisher('image_topic_2', Image, queue_size=10)
        self.bridge = CvBridge()
        
     
	#TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ
        r = rospy.Rate(1);
	


	# as long as you haven't ctrl + c keeping doing...
        while not rospy.is_shutdown():
                self.image_sub = rospy.Subscriber('image_topic',Image,self.callback)
       		r.sleep()

    def callback(self, data):
        try:
            cv_image=self.bridge.imgmsg_to_cv2(data,"bgr8")
        except CvBridgeError as e:
            print(e)
        gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(gray_image,127,255,0)
        im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX, cY = 0, 0
            cv2.circle(cv_image, (cX, cY), 5, (255, 255, 255), -1)
            cv2.putText(cv_image, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
 
            # display the image
            cv2.imshow("Image window", cv_image)
            cv2.waitKey(0)
        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
        except CvBridgeError as e:
            print(e)
            
    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop TurtleBot")
	# a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
        cv2.destroyAllWindows()
	# sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
        rospy.sleep(1)

 
if __name__ == '__main__':
    try:
        ShowColorImage()
    except Exception as e:
	print(e)
        rospy.loginfo("ShowColorImage node terminated.")

