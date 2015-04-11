#!/usr/bin/python
import glob
import cv2
import cv_bridge
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import Int32, Float32
import rospkg

from os import listdir
from os.path import isfile, join
from os import sys
from PyQt4.QtCore import SIGNAL, QTimer

class FramePlayer: 
	def __init__(self, vid_directory, repeat): 
		self.image_publisher = rospy.Publisher("/robot/xdisplay", Image, queue_size=100)
		files = sorted([ f for f in listdir(vid_directory) ])
		self.images = [cv2.imread(vid_directory + f) for f in files]
		self.rate = rospy.Rate(50)
		self.repeat = repeat
		self.repetitions = 0

		self.velocity = (1/20.0)

		self.current_frame = 0


	def play(self): 
		self.timer = rospy.Timer(rospy.Duration(self.velocity), self.play_cb)

	def play_cb(self, time): 
		if (self.current_frame >= len(self.images)):
			self.repetitions += 1
			if (self.repetitions > self.repeat): 
				exit()
			else: 
				self.current_frame = 0
				
		image = self.images[self.current_frame]
		msg = cv_bridge.CvBridge().cv2_to_imgmsg(image, encoding="bgr8")
		self.image_publisher.publish(msg)
		self.current_frame = self.current_frame + 1




def main(): 
	if (len(sys.argv) < 2): 
		print("usage: play_frames.py <frame_dir (ends in /)> <repeatNum>")
		return

	rospy.init_node('frame_player', anonymous=True)

	vid_directory = sys.argv[1]
	repeat = int(sys.argv[2])
	fp = FramePlayer(vid_directory, repeat)
	fp.play()
	rospy.sleep(repeat * fp.velocity * (len(fp.images)) + fp.velocity * 2)

main()
