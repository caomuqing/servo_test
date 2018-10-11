#!/usr/bin/env python
# @package: pyHerkulex
# @name: servo.py
# @author: Achu Wilson (achuwilson@gmail.com), Akhil Chandran  (akhilchandran.t.r@gmail.com)
# @version: 0.1

# This is a python library for interfacing the Herkulex range of smart 
# servo motors manufactured by Dongbu Robotics.

# The library was created by Achu Wilson (mailto:achu@sastrarobotics.com) 
# for the internal projects of Sastra Robotics

# This free software is distributed under the GNU General Public License.
# See http://www.gnu.org/licenses/gpl.html for details.

# For usage of this code for  commercial purposes contact Sastra Robotics 
# India Pvt. Ltd. (mailto:contact@sastrarobotics.com)

# This is an example script to connect to a Herkulex bus & scan for the servos

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int16

import herkulex
from herkulex import servo

servo1 = None

def moveServo_cb(data):
	global servo1
	targetPosition = data.data
	goaltime = 2.0
	servo1.set_servo_position(targetPosition, goaltime)

def main():
	global servo1
	rospy.init_node('servo_controller', anonymous=True)
	rate = rospy.Rate(10)  # 10hz
	#connect to the serial port
	herkulex.connect("/dev/ttyUSB0",115200)
	#scan for servos, it returns a tuple with servo id & model number
	servos = herkulex.scan_servos()
	print servos
	servo1 = servo(servos.servoid)
	servo_status = servo1.get_servo_status()
	print "servo status: ", servo_status
	rospy.Subscriber('/servo/cmdpos', Int16, moveServo_cb)
	pub = rospy.Publisher('/servo/pos', Int16, queue_size=10)
	servo_position = servo1.get_servo_position()
	print "servo pos: ", servo_position 
	pub.publish(servo_position)
	rospy.spin()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass