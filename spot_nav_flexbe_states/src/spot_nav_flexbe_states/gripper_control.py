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
                                         block_until_arm_arrives, blocking_stand)
from bosdyn.client.lease import LeaseClient, LeaseKeepAlive
import time


class GripperControl(EventState):
    """
    This state continues running until a "continue" message is published to the 
    topic, whose name is passed as an input parameter. 

    -- stow        boolean      boolean for indicating whether to stow or unstow the arm.

    <= success                  indicates successful completion of navigation.
    <= failed                   indicates unsuccessful completion of navigation.

    """

    def __init__(self, fraction):
        # Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.

        super(GripperControl, self).__init__(outcomes=['success', 'failure'],
                                            input_keys=['robot_command_client', 'robot', 'lease'])
        self._fraction = fraction


    def execute(self, userdata):
        # This method is called periodically while the state is active.
        # Main purpose is to check state conditions and trigger a corresponding outcome.
        # If no outcome is returned, the state will stay active.
        with LeaseKeepAlive(userdata.lease):
            print("Opening the gripper......................")            
            # open the gripper
            gripper_command = RobotCommandBuilder.claw_gripper_open_fraction_command(float(self._fraction))
            # gripper_command = RobotCommandBuilder.claw_gripper_open_command()
            command_id = userdata.robot_command_client.robot_command(gripper_command)
            block_until_arm_arrives(userdata.robot_command_client, command_id, 3.0)
            print("Finished opening the gripper......................")
            
            # time.sleep(5)
            
            # print("CLosing the gripper......................")            
            # # close the gripper
            # gripper_command = RobotCommandBuilder.claw_gripper_open_fraction_command(0.0)
            # # gripper_command = RobotCommandBuilder.claw_gripper_close_command()
            # command_id = userdata.robot_command_client.robot_command(gripper_command)
            # block_until_arm_arrives(userdata.robot_command_client, command_id, 3.0)
            # print("Finished closing the gripper......................")

    
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
