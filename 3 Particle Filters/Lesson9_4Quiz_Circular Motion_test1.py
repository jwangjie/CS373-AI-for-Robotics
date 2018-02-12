# -----------------
# USER INSTRUCTIONS
#
# Write a function in the class robot called move()
#
# that takes self and a motion vector (this
# motion vector contains a steering* angle and a
# distance) as input and returns an instance of the class
# robot with the appropriate x, y, and orientation
# for the given motion.
#
# *steering is defined in the video
# which accompanies this problem.
#
# For now, please do NOT add noise to your move function.
#
# Please do not modify anything except where indicated
# below.
#
# There are test cases which you are free to use at the
# bottom. If you uncomment them for testing, make sure you
# re-comment them before you submit.

from math import *
import random
# --------
# 
# the "world" has 4 landmarks.
# the robot's initial coordinates are somewhere in the square
# represented by the landmarks.
#
# NOTE: Landmark coordinates are given in (y, x) form and NOT
# in the traditional (x, y) format!

landmarks  = [[0.0, 100.0], [0.0, 0.0], [100.0, 0.0], [100.0, 100.0]] # position of 4 landmarks
world_size = 100.0 # world is NOT cyclic. Robot is allowed to travel "out of bounds"
max_steering_angle = pi/4 # You don't need to use this value, but it is good to keep in mind the limitations of a real car.

# ------------------------------------------------
# 
# this is the robot class
#

class robot:

    # --------

    # init: 
    #	creates robot and initializes location/orientation 
    #

    def __init__(self, length = 10.0): 
	# length can be initialized to be any random number like all variables in the __init__ function such as self.x 
	# self.y etc., but must be initialized by numbers in the function. 

        self.x = random.random() * world_size # initial x position
        self.y = random.random() * world_size # initial y position
        self.orientation = random.random() * 2.0 * pi # initial orientation
        self.length = length # length of robot
        self.bearing_noise  = 0.0 # initialize bearing noise to zero
        self.steering_noise = 0.0 # initialize steering noise to zero
        self.distance_noise = 0.0 # initialize distance noise to zero
    
    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))
    # --------
    # set: 
    #	sets a robot coordinate
    #

    def set(self, new_x, new_y, new_orientation):

        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError, 'Orientation must be in [0..2pi]'
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)


    # --------
    # set_noise: 
    #	sets the noise parameters
    #

    def set_noise(self, new_b_noise, new_s_noise, new_d_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.bearing_noise  = float(new_b_noise)
        self.steering_noise = float(new_s_noise)
        self.distance_noise = float(new_d_noise)
    
    ############# ONLY ADD/MODIFY CODE BELOW HERE ###################

    # --------
    # move:
    #   move along a section of a circular path according to motion
    #
    
    def move(self, motion, tolerance = 0.001):
      
      steering = motion[0]
      distance = motion[1]
      
      if abs(steering) > max_steering_angle:
        raise ValueError, 'Exceeding max steering angle'
        
      if distance < 0.0:
        raise ValueError, 'Moving backwards is not valid'
        
      # make a new copy
      res =robot()
      res.length         = self.length
      res.bearing_noise  = self.bearing_noise
      res.steering_noise = self.steering_noise
      res.distance_noise = self.distance_noise
      
      # apply noise
      steering2 = random.gauss(steering, self.steering_noise)
      distance2 = random.gauss(distance, self.distance_noise)
      
      # Execute motion
      turn = tan(steering2) * distance2 / res.length
      
      if abs(turn) < tolerance:
        # approximate by straight line motion
        
        res.x = self.x + (distance2 * cos(self.orientation))
        res.y = self.y + (distance2 * sin(self.orientation))
        res.orientation = (self.orientation + turn) % (2.0 * pi)
        
      else:
        # approximate bicycle model for motion
        
        radius = distance2 /turn
        cx = self.x - (sin(self.orientation) * radius)
        cy = self.y + (cos(self.orientation) * radius)
        res.orientation = (self.orientation + turn) % (2.0 * pi)
        res.x = cx + (sin(res.orientation) * radius)
        res.y = cy - (cos(res.orientation) * radius)
        
      return res

        
## --------
## TEST CASE:
## 
## 1) The following code should print:
##       Robot:     [x=0.0 y=0.0 orient=0.0]
##       Robot:     [x=10.0 y=0.0 orient=0.0]
##       Robot:     [x=19.861 y=1.4333 orient=0.2886]
##       Robot:     [x=39.034 y=7.1270 orient=0.2886]
##
##
length = 20.
bearing_noise  = 0.0
steering_noise = 0.0
distance_noise = 0.0
##
myrobot = robot(length)
myrobot.set(0.0, 0.0, 0.0)
myrobot.set_noise(bearing_noise, steering_noise, distance_noise)
##
motions = [[0.0, 10.0], [pi / 6.0, 10], [0.0, 20.0]]

print 'Robot:    ', myrobot
##
T = len(motions)
##
# print 'Robot:    ', myrobot
for t in range(T):
    myrobot = myrobot.move(motions[t])
    print 'Robot:    ', myrobot
