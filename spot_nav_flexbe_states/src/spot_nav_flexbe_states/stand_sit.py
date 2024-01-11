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


class StandSit(EventState):
    """
    This state continues running until a "continue" message is published to the 
    topic, whose name is passed as an input parameter. 

    -- stow        boolean      boolean for indicating whether to stow or unstow the arm.

    <= success                  indicates successful completion of navigation.
    <= failed                   indicates unsuccessful completion of navigation.

    """

    def __init__(self, stand):
        # Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.

        super(StandSit, self).__init__(outcomes=['success', 'failure'],
                                        input_keys=['robot_command_client', 'robot', 'lease'])
        self._stand =  stand


    def execute(self, userdata):
        # This method is called periodically while the state is active.
        # Main purpose is to check state conditions and trigger a corresponding outcome.
        # If no outcome is returned, the state will stay active.
        with LeaseKeepAlive(userdata.lease):
            if self._stand: # stand
                print("Trying to stand.................")
                blocking_stand(userdata.robot_command_client, timeout_sec=10)
                print("Robot is standing..................")
            else: # sit
                print("Trying to sitting.................")
                blocking_sit(userdata.robot_command_client, timeout_sec=10)
                print("Robot is sitting..................")
                

    
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
