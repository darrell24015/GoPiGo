#!/usr/bin/env python

#################################################################################
#  autoPilot.py									#
#  Darrell Little								#
#  04/07/2017									#
#  Based on "Programming Autonomy - 						#
#  Robotics with Python Raspberry Pi and GoPiGo p.6"				#
#  https://pythonprogramming.net/programming-autonomous-robot-gopigo-tutorial/	#
#################################################################################

from gopigo import *
import time
import random

min_distance = 35
fwdSpeed = 150
revSpeed = 175

# Blink both LED
def blink():
    for x in range(0, 4):
	led_on(0)
        led_on(1)
        time.sleep(0.5)
        led_off(0)
        led_off(1)

def autoPilot():
    # Continuously loop unless REVERSE repeats too many times
    max_reverse = 2
    reverse_attempt = 0
    no_problem = True
    # When REVERSE needed, choose random rotate right or rotate left
    rot_choices = [right_rot, left_rot]
    
    while no_problem:
        servo(90)
        time.sleep(0.5)
        dist = us_dist(15)
        if dist > min_distance:
            print('Forward is clear', dist)
	    # Reset reverse_attempt if able to move forward
	    reverse_attempt = 0
            set_speed(fwdSpeed)
            fwd()
            time.sleep(0.5)
        else:
            print('Obstacle detected', dist)
            stop()
            servo(45)
            time.sleep(1)
            left_dir = us_dist(15)
            time.sleep(1)
            servo(145)
            right_dir = us_dist(15)
            time.sleep(1)

            if left_dir > right_dir and left_dir > min_distance:
                print('Choose left!')
		# Reset reverse_attempt if able to turn left
            	reverse_attempt = 0
                set_speed(fwdSpeed)
                left()
                time.sleep(1)
            elif left_dir < right_dir and right_dir > min_distance:
                print('Choose Right!')
		# Reset reverse_attempt if able to turn right
            	reverse_attempt = 0
                set_speed(fwdSpeed)
                right()
                time.sleep(1)
            else:
                if reverse_attempt < max_reverse:
			print('No clear path, REVERSE!')
			blink()
			set_speed(revSpeed)
                	bwd()
                	time.sleep(1)
                	rotation = rot_choices[random.randrange(0,2)]
                	rotation()
			# Increment for each attempt at REVERSE
			reverse_attempt += 1
                	time.sleep(1)
		else:
			stop()
			servo(90)
			print('Houston, we have a problem!')
			print('Stopping Program')
			disable_servo()
			no_problem = False
            stop()
                
stop()
enable_servo()
servo(90)
print('Wait for sensor to stabilize')
time.sleep(1)
print('One ... ', us_dist(15))
time.sleep(1)
print('Two ... ', us_dist(15))
time.sleep(1)
print('Three ... ', us_dist(15))
time.sleep(1)
print('GoPiGo!')

try:
    autoPilot()

except KeyboardInterrupt:
    stop()
    servo(90)
    print('Stopping Program')
    disable_servo()
