#!/usr/bin/python

# Start up ROS pieces.
PKG = 'rosbag_recoder'
import roslib
roslib.load_manifest(PKG)
import rosbag
import rospy
import cv2 as cv
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import os
import sys


class ImageCreator():
    # Must have __init__(self) function for a class, similar to a C++ class constructor.
    def __init__(self):
        self.image_counter1 = 0
        self.image_counter2 = 0
        self.lastCaptureTime_left =0
        self.lastCaptureTime_right = 0
        self.recording_image_rate = 2
        # Get parameters when starting node from a launch file.
        if len(sys.argv) < 1:
            save_dir = rospy.get_param('save_dir')
            filename = rospy.get_param('filename')
            rospy.loginfo("Bag filename = %s", filename)
        # Get parameters as arguments to 'rosrun my_package bag_to_images.py <save_dir> <filename>', where save_dir and filename exist relative to this executable file.e.g rosrun bag_images bag_to_images.py /home/aayushsingla/catkin_ws/src/bag_imagesbag_images subset.bag
        # the running directory should have subset.bag
        else:
            save_dir = os.path.join(sys.path[0], sys.argv[1])
            filename = os.path.join(sys.path[0], sys.argv[2])
            rospy.loginfo("Bag filename = %s", filename)

        # Use a CvBridge to convert ROS images to OpenCV images so they can be saved.
        self.bridge = CvBridge()

        # open the name file
        fh = open(str(save_dir) + "stereo_calib.xml", "w")

        # Write start tags
        fh.write('<?xml version="1.0"?>\n')
        fh.write('<opencv_storage>\n')
        fh.write('<imagelist>\n')

        # Open bag file.
        with rosbag.Bag(filename, 'r') as bag:
            for topic, msg, t in bag.read_messages():

                #For future use
                if topic == "/ranger_finder/data":
                    range=msg.dist



                if topic == "/stereo_camera/left/image_raw":
                    print 'left'
                    print msg.header.stamp.to_sec()
                    try:
                        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
                    except CvBridgeError, e:
                        print e
                    timestr = "%.9f" % msg.header.stamp.to_sec()
                    image_name = str(save_dir)+'left'+str(self.image_counter1)+".jpg"
                    cv.imwrite(image_name, cv_image)
                    self.image_counter1 += 1
                    fh.write('"'+image_name +'"\n')
                       #self.lastCaptureTime_left = msg.header.stamp.to_nsec()

                if topic == "/stereo_camera/right/image_raw":
                    print 'right'
                    print msg.header.stamp.to_sec()
                    try:
                        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
                    except CvBridgeError, e:
                        print e

                    image_name = str(save_dir) + 'right' + str(self.image_counter2) + ".jpg"
                    cv.imwrite(image_name, cv_image)
                    self.image_counter2 += 1
                    fh.write('"' + image_name + '"\n')
                    #     self.lastCaptureTime_right = msg.header.stamp.to_nsec()

        #Write end tags
        fh.write('</imagelist>\n')
        fh.write('</opencv_storage>\n')
        fh.close()


# Main function.
if __name__ == '__main__':
    # Initialize the node and name it.
    rospy.init_node(PKG)
    # Go to class functions that do all the heavy lifting. Do error checking.
    try:
        image_creator = ImageCreator()
    except rospy.ROSInterruptException:
        pass
