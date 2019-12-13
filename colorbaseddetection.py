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
        (rows, cols, channels) = cv_image.shape
        for x in range(rows):
            for y in range(cols):
                if (cv_image(x,y,1)>= 230 and cv_image(x,y,1)<= 255):
                    if(cv_image(x,y,2)>= 145 and cv_image(x,y,1)<= 165):
                        cv_detected_img(x,y,1) = 255
                        cv_detected_img(x,y,2) = 255
                        cv_detected_img(x,y,3) = 255
                    else:
                        cv_detected_img(x,y,1) = 0
                        cv_detected_img(x,y,2) = 0
                        cv_detected_img(x,y,3) = 0
                else:
                    cv_detected_img(x,y,1) = 0
                    cv_detected_img(x,y,2) = 0
                    cv_detected_img(x,y,3) = 0                    
        cv2.imshow("Image window", cv_detected_img)
        cv2.waitKey(3)
        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_detected_img, "bgr8"))
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

