#!/usr/bin/env python
import argparse
import sys
from flexbe_core import EventState, Logger

import bosdyn.client
import bosdyn.client.lease
import bosdyn.client.util
from bosdyn.api import estop_pb2, image_pb2, manipulation_api_pb2, geometry_pb2
from bosdyn.client.estop import EstopClient
from bosdyn.client.robot_command import (RobotCommandBuilder, RobotCommandClient,
                                         block_until_arm_arrives, blocking_stand)
from bosdyn.client.lease import LeaseClient, LeaseKeepAlive
import numpy as np
import cv2
from bosdyn.client.manipulation_api_client import ManipulationApiClient
import time

class Grasp(EventState):
    """
    This state is used for grasp the object whose coordinates are received from the process state. 

    -- None

    ># manipulation_api_client          ManipulationApiClient
    ># robot_command_client             RobotCommandClient          
    ># robot                            robot object representing the robot
    ># lease                            Lease object
    ># image                            processed image
    ># click_x                          X coordinate of the clicked object, which will grasped
    ># click_y                          Y coordinate of the clicked object, which will grasped
    
    #> None
    
        
    """

    def __init__(self):
        # Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.

        super(Grasp, self).__init__(outcomes=['success', 'failure'],
                                    input_keys=['manipulation_api_client', 'robot_command_client', 'robot', 'lease', 'image', 'click_x', 'click_y'])


    def execute(self, userdata):
        # This method is called periodically while the state is active.
        # Main purpose is to check state conditions and trigger a corresponding outcome.
        # If no outcome is returned, the state will stay active.
        
        return 'success'

    
    def on_enter(self, userdata):
        # This method is called when the state becomes active, i.e. a transition from another state to this one is taken.
                
        pick_vec = geometry_pb2.Vec2(x=userdata.click_x, y=userdata.click_y)
        grasp = manipulation_api_pb2.PickObjectInImage(pixel_xy=pick_vec, 
                                                       transforms_snapshot_for_camera=userdata.image.shot.transforms_snapshot,
                                                       frame_name_image_sensor=userdata.image.shot.frame_name_image_sensor,
                                                       camera_model=userdata.image.source.pinhole)
        
        # add grasp constraints......................
        print("starting the grasp...............................")
        grasp_request = manipulation_api_pb2.ManipulationApiRequest(pick_object_in_image=grasp)
        cmd_response = userdata.manipulation_api_client.manipulation_api_command(manipulation_api_request=grasp_request)
        
        while True:
            feedback_request = manipulation_api_pb2.ManipulationApiFeedbackRequest(manipulation_cmd_id=cmd_response.manipulation_cmd_id)
            response = userdata.manipulation_api_client.manipulation_api_feedback_command(manipulation_api_feedback_request=feedback_request)
            print(f'Current state: {manipulation_api_pb2.ManipulationFeedbackState.Name(response.current_state)}')
            
            if response.current_state == manipulation_api_pb2.MANIP_STATE_GRASP_SUCCEEDED or response.current_state == manipulation_api_pb2.MANIP_STATE_GRASP_FAILED:
                break

            time.sleep(0.25)
        print("Finished grasping.....................")

    def on_exit(self, userdata):
        # This method is called when an outcome is returned and another state gets active.
        pass


    def on_stop(self):
        # This method is called whenever the behavior stops execution, also if it is cancelled.
        pass
