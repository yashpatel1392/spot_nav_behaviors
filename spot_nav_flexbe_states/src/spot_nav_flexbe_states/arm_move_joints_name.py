#!/usr/bin/env python
import argparse
import sys
from flexbe_core import EventState, Logger
import json

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

class ArmMoveJointsName(EventState):
    """
    This state is used for moving the arm to a saved position by specifying the name of the saved
    position. 

    -- pose_name            String      name of the saved arm position
    
    ># robot_command_client             RobotCommandClient          
    ># robot                            robot object representing the robot
    ># lease                            Lease object
    ># state_client                     RobotStateClient    
    
    #> None
    
    """

    def __init__(self, pose_name):
        # Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.

        super(ArmMoveJointsName, self).__init__(outcomes=['success', 'failure'],
                                            input_keys=['robot_command_client', 'robot', 'lease', 'state_client'])
        self._pose_name = pose_name
        self._sh0 = 0.0
        self._sh1 = 0.0
        self._el0 = 0.0
        self._el1 = 0.0
        self._wr0 = 0.0
        self._wr1 = 0.0
        

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

        print("------------------------------")
        print("sh0: ", self._sh0)
        print("sh1: ", self._sh1)
        print("el0: ", self._el0)
        print("el1: ", self._el1)
        print("wr0: ", self._wr0)
        print("wr1: ", self._wr1)
        print("------------------------------")

        return 'success'

        

    def on_enter(self, userdata):
        if self._pose_name:
            try:
                with open('../spot-arm-positions/arm_data.json', 'r') as file:
                    current_data = json.load(file)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                current_data = {}
            
            if self._pose_name not in current_data:
                return 'failure'
            else:
                self._sh0 = current_data[self._pose_name]["sh0"]
                self._sh1 = current_data[self._pose_name]["sh1"]
                self._el0 = current_data[self._pose_name]["el0"]
                self._el1 = current_data[self._pose_name]["el1"]
                self._wr0 = current_data[self._pose_name]["wr0"]
                self._wr1 = current_data[self._pose_name]["wr1"]


    def on_exit(self, userdata):
        # This method is called when an outcome is returned and another state gets active.
        pass


    def on_stop(self):
        # This method is called whenever the behavior stops execution, also if it is cancelled.
        pass
