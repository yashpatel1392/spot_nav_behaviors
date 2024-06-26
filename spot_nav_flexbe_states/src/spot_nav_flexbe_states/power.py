#!/usr/bin/env python
import argparse
import sys
from flexbe_core import EventState, Logger

import bosdyn.client
import bosdyn.client.lease
import bosdyn.client.util
from bosdyn.api import estop_pb2
from bosdyn.client.estop import EstopClient
from bosdyn.client.robot_command import (RobotCommandBuilder, RobotCommandClient,
                                         block_until_arm_arrives, blocking_stand, blocking_sit)
from bosdyn.client.lease import LeaseClient, LeaseKeepAlive
import time


class Power(EventState):
    """
    This state is used for powering on/off the robot.

    -- on                 boolean       true would turn the robot, while false would power it off           

    ># robot_command_client             RobotCommandClient          
    ># robot                            robot object representing the robot
    ># lease                            Lease object

    #> None

    """

    def __init__(self, on):
        # Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.

        super(Power, self).__init__(outcomes=['success', 'failure'],
                                        input_keys=['robot_command_client', 'robot', 'lease'])
        self._on = on


    def execute(self, userdata):
        # This method is called periodically while the state is active.
        # Main purpose is to check state conditions and trigger a corresponding outcome.
        # If no outcome is returned, the state will stay active.
        with LeaseKeepAlive(userdata.lease):
            if self._on: # on
                print("Trying to power on.................")
                userdata.robot.power_on(timeout_sec=20)
                print("Robot is on..................")
            else: # off
                print("Trying to power off.................")
                userdata.robot.power_off(cut_immediately=False, timeout_sec=20)
                print("Robot is off..................")
                

    
        return 'success'

    def on_enter(self, userdata):
        # This method is called when the state becomes active, i.e. a transition from another state to this one is taken.
        
        pass # Nothing to do here


    def on_exit(self, userdata):
        # This method is called when an outcome is returned and another state gets active.
        pass


    def on_stop(self):
        # This method is called whenever the behavior stops execution, also if it is cancelled.
        pass
