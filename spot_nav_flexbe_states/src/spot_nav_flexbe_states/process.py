#!/usr/bin/env python
import argparse
import sys
from flexbe_core import EventState, Logger

import bosdyn.client
import bosdyn.client.lease
import bosdyn.client.util
from bosdyn.api import estop_pb2, image_pb2, manipulation_api_pb2
from bosdyn.client.estop import EstopClient
from bosdyn.client.robot_command import (RobotCommandBuilder, RobotCommandClient,
                                         block_until_arm_arrives, blocking_stand)
from bosdyn.client.lease import LeaseClient, LeaseKeepAlive
import numpy as np
import cv2








# Global fields
g_img_click = None
g_img = None

def cv_mouse_callback(event, x, y, flags, param):
    global g_img_click, g_img
    copy_img = g_img.copy()
    
    print("IMAGE TITLE PARAM: ", param)
    
    if event == cv2.EVENT_LBUTTONUP:
        g_img_click = (x, y)
    else:
        color = (30, 30, 30)
        thickness = 2
        # image_title = 'hand image'
        height = copy_img.shape[0]
        width = copy_img.shape[1]
        cv2.line(copy_img, (0, y), (width, y), color, thickness)
        cv2.line(copy_img, (x, 0), (x, height), color, thickness)
        cv2.imshow(param, copy_img)




class ProcessImageGrasp(EventState):
    """
    This state would display the image captured from the robot and would let the user click on an
    object which would be grasped.

    -- None

    ># image_response                   list of the image responses from the robot

    #> image                            processed image
    #> click_x                          X coordinate of the clicked object, which will grasped
    #> click_y                          Y coordinate of the clicked object, which will grasped

    """

    def __init__(self):
        # Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.

        super(ProcessImageGrasp, self).__init__(outcomes=['success', 'failure'],
                                            input_keys=['image_response'],
                                            output_keys=['click_x', 'click_y', 'image'])
        self._img = None
        # self._img_click = None
        self._img_title = ''
        self._image = None

    def execute(self, userdata):
        # This method is called periodically while the state is active.
        # Main purpose is to check state conditions and trigger a corresponding outcome.
        # If no outcome is returned, the state will stay active.
        
        global g_img_click, g_img
        
        g_img_click = None
        g_img = self._img
        cv2.imshow(self._img_title, self._img)
        
        while g_img_click is None:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == ord('Q'):
                print('"q" pressed, exiting.')
                break
        
        if g_img_click is not None:
            print(f'Picking object at image location ({g_img_click[0]}, {g_img_click[1]})')
        
        print("image.shot.transforms_snapshot: ", self._image.shot.transforms_snapshot)
        print("image.shot.frame_name_image_sensor: ", self._image.shot.frame_name_image_sensor)
        print("image.source.pinhole: ", self._image.source.pinhole)
        
        
        # print("image.shot.transforms_snapshot: ", image.shot.transforms_snapshot)
        # print("image.shot.frame_name_image_sensor: ", image.shot.frame_name_image_sensor)
        # print("image.source.pinhole: ", image.source.pinhole)
        
        
        userdata.click_x = g_img_click[0]
        userdata.click_y = g_img_click[1]
        userdata.image = self._image
        
        cv2.destroyAllWindows()
        
        return 'success'

    
    def on_enter(self, userdata):
        # This method is called when the state becomes active, i.e. a transition from another state to this one is taken.
        
        # Took some lines of code from arm_grasp example from spot_sdk
        
        # Get/process the image
        self._image = userdata.image_response[0]
        if self._image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_DEPTH_U16:
            dtype = np.uint16
        else:
            dtype = np.uint8

        self._img = np.fromstring(self._image.shot.image.data, dtype=dtype)
        
        if self._image.shot.image.format == image_pb2.Image.FORMAT_RAW:
            self._img = self._img.reshape(self._image.shot.image.rows, self._image.shot.image.cols)
        else:
            self._img = cv2.imdecode(self._img, -1)

        # Display the image
        self._img_title = 'Select Object'
        cv2.namedWindow(self._img_title)
        cv2.setMouseCallback(self._img_title, cv_mouse_callback, self._img_title)
        
        pass # Nothing to do here


    def on_exit(self, userdata):
        # This method is called when an outcome is returned and another state gets active.
        pass


    def on_stop(self):
        # This method is called whenever the behavior stops execution, also if it is cancelled.
        pass
