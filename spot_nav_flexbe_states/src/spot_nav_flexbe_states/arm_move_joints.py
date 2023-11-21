#!/usr/bin/env python
import argparse
import sys
from flexbe_core import EventState, Logger

import bosdyn.client
import bosdyn.client.lease
import bosdyn.client.util
from bosdyn.api import estop_pb2, arm_command_pb2, robot_command_pb2, synchronized_command_pb2
from bosdyn.client.estop import EstopClient
from bosdyn.client.robot_command import (RobotCommandBuilder, RobotCommandClient,
                                         block_until_arm_arrives, blocking_stand)
from bosdyn.client.lease import LeaseClient, LeaseKeepAlive
from bosdyn.util import duration_to_seconds
import time

class ArmMoveJoints(EventState):
    """
    This state continues running until a "continue" message is published to the 
    topic, whose name is passed as an input parameter. 

    <= success                  indicates successful completion of navigation.
    <= failed                   indicates unsuccessful completion of navigation.

    """

    def __init__(self, sh0, sh1, el0, el1, wr0, wr1):
        # Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.

        super(ArmMoveJoints, self).__init__(outcomes=['success', 'failure'],
                                            input_keys=['robot_command_client', 'robot', 'lease', 'state_client'])
        self._sh0 = float(sh0)
        self._sh1 = float(sh1)
        self._el0 = float(el0)
        self._el1 = float(el1)
        self._wr0 = float(wr0)
        self._wr1 = float(wr1)
        

    # This function is taken from the examples
    def make_robot_command(self, arm_joint_traj):
        joint_move_command = arm_command_pb2.ArmJointMoveCommand.Request(trajectory=arm_joint_traj)
        arm_command = arm_command_pb2.ArmCommand.Request(arm_joint_move_command=joint_move_command)
        sync_arm = synchronized_command_pb2.SynchronizedCommand.Request(arm_command=arm_command)
        arm_sync_robot_cmd = robot_command_pb2.RobotCommand(synchronized_command=sync_arm)
        return RobotCommandBuilder.build_synchro_command(arm_sync_robot_cmd)


    def print_feedback(self, feedback_resp):
        joint_move_feedback = feedback_resp.feedback.synchronized_feedback.arm_command_feedback.arm_joint_move_feedback

        print(f'  planner_status = {joint_move_feedback.planner_status}')
        print(f'  time_to_goal = {duration_to_seconds(joint_move_feedback.time_to_goal):.2f} seconds.')

        # Query planned_points to determine target pose of arm
        print('  planned_points:')
        for idx, points in enumerate(joint_move_feedback.planned_points):
            pos = points.position
            pos_str = f'sh0 = {pos.sh0.value:.3f}, sh1 = {pos.sh1.value:.3f}, el0 = {pos.el0.value:.3f}, ' \
                    f'el1 = {pos.el1.value:.3f}, wr0 = {pos.wr0.value:.3f}, wr1 = {pos.wr1.value:.3f}'
            print(f'    {idx}: {pos_str}')
        return duration_to_seconds(joint_move_feedback.time_to_goal)



    def execute(self, userdata):
        # This method is called periodically while the state is active.
        # Main purpose is to check state conditions and trigger a corresponding outcome.
        # If no outcome is returned, the state will stay active.
        with LeaseKeepAlive(userdata.lease):
            print("Unstowing the arm..........................")
            unstow = RobotCommandBuilder.arm_ready_command()
            unstow_command_id = userdata.robot_command_client.robot_command(unstow)
            block_until_arm_arrives(userdata.robot_command_client, unstow_command_id, 3.0)
            print("---------------------------------")
            print("\n\nRobot State: ", userdata.state_client.get_robot_state())
            
            print(f'\nMoving the arm to the given joint positions: sh0: [{self._sh0}], sh1: [{self._sh1}], el0: [{self._el0}], el1: [{self._el1}], wr0: [{self._wr0}], wr1: [{self._wr1}]\n')            
            traj_point = RobotCommandBuilder.create_arm_joint_trajectory_point(self._sh0, self._sh1, self._el0, self._el1, self._wr0, self._wr1)
            arm_joint_traj = arm_command_pb2.ArmJointTrajectory(points=[traj_point])
            command = self.make_robot_command(arm_joint_traj)
            cmd_id = userdata.robot_command_client.robot_command(command)
            
            feedback_resp = userdata.robot_command_client.robot_command_feedback(cmd_id)
            print("------------------------------------------------------------------------------------------")
            print('Feedback: ')           
            time_to_goal = self.print_feedback(feedback_resp)
            print("------------------------------------------------------------------------------------------\n")         
                        
            block_until_arm_arrives(userdata.robot_command_client, cmd_id, time_to_goal + 3.0)
            print("\n\nRobot State: ", userdata.state_client.get_robot_state())
            
            print("Stowing the arm..........................")
            stow = RobotCommandBuilder.arm_stow_command()
            stow_command_id = userdata.robot_command_client.robot_command(stow)
            block_until_arm_arrives(userdata.robot_command_client, stow_command_id, 3.0)

        return 'success'

        

    def on_enter(self, userdata):                
        pass # Nothing to do here


    def on_exit(self, userdata):
        # This method is called when an outcome is returned and another state gets active.
        pass


    def on_stop(self):
        # This method is called whenever the behavior stops execution, also if it is cancelled.
        pass
