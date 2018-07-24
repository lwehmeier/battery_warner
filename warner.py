#!/usr/bin/python
import math
from math import sin, cos, pi, radians
import rospy
import tf
from std_msgs.msg import Float32, Int32, Int16
import struct
import numpy as np
class Warner:
    def __init__(self, voltage, cycles):
        self.warn = voltage
        self.previous = []
        self.n = cycles
        self.avg = 0.0
    def check(self, voltage):
        voltage=voltage.data
        if voltage <= 0.0:
            print("received invalid voltage, ignoring")
            return True
        self.previous = self.previous[-self.n:]
        self.previous.append(voltage)
        self.avg = sum(self.previous)/self.n
        if self.avg == 0.0 or len(self.previous) < self.n:
            print("waiting for more data...")
            self.previous.append(voltage)
            return
        if self.avg < self.warn:
            print(self.avg)
            return False
        return True


def updateVoltage(v):
    if not mon.check(v):
        rospy.logerr("battery critically low: %s", str(mon.avg))
        pub.publish(Float32(mon.avg))


rospy.init_node('vl6180')
warn = rospy.get_param('~voltage')
rospy.loginfo('Parameter %s has value %s', rospy.resolve_name('~voltage'), warn)
mon = Warner(warn,5)
pt = rospy.get_param('~publisher')
rospy.loginfo('Parameter %s has value %s', rospy.resolve_name('~publisher'), pt)
st = rospy.get_param('~subscriber')
rospy.loginfo('Parameter %s has value %s', rospy.resolve_name('~subscriber'), st)

rospy.Subscriber(st, Float32, updateVoltage, queue_size=5)
pub = rospy.Publisher(pt, Float32, queue_size=5)
r = rospy.Rate(2)
rospy.spin()
