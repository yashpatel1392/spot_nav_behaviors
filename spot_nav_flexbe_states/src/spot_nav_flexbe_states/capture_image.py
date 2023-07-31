#!/usr/bin/env python
import rospy

from flexbe_core import EventState, Logger
from bosdyn.client.util import *
from bosdyn.client.lease import LeaseClient, LeaseKeepAlive
from bosdyn.client.robot_state import RobotStateClient
from bosdyn.client.graph_nav import GraphNavClient
from bosdyn.client.power import PowerClient
from bosdyn.client.robot_command import RobotCommandBuilder, RobotCommandClient
from bosdyn.client.license import LicenseClient
from bosdyn.client.image import ImageClient
import time, os, io
from PIL import Image


class CaptureImage(EventState):
    '''
    Example for a state to demonstrate which functionality is available for state implementation.
    This example lets the behavior wait until the given target_time has passed since the behavior has been started.

    -- target_time 	float 	Time which needs to have passed since the behavior started.

    <= continue 			Given time has passed.
    <= failed 				Example for a failure outcome.

    '''

    def __init__(self, path):
        # Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
        super(CaptureImage, self).__init__(outcomes = ['continue', 'failed'],
                                            input_keys = ['image_client'])
        self._path = path

    def _save_image(self, image, path):
        name = 'front-cam-capture.jpg'
        if path is not None and os.path.exists(path):
            path = os.path.join(os.getcwd(), path)
            name = os.path.join(path, name)
            print("Saving image to: ", name)
        else:
            print("Saving image to working directory as ", name)

        try:
            image = Image.open(io.BytesIO(image.data))
            image.save(name)
        except Exception as exc:
            logger = bosdyn.client.util.get_logger()
            logger.warning('Exception thrown saving image. %r', exc)

    def execute(self, userdata):
        # This method is called periodically while the state is active.
        return 'continue'
        

    def on_enter(self, userdata):
        # This method is called when the state becomes active, i.e. a transition from another state to this one is taken.
        # It is primarily used to start actions which are associated with this state.
        
        # Following code can be used for listing image sources
        
        # img_sources = userdata.image_client.list_image_sources()
        # print("----------------------------------------------------\n\n")
        # print("Image Sources:\n")
        # print(img_sources)
        # print("----------------------------------------------------\n")
        
        image_response = userdata.image_client.get_image_from_sources(['frontleft_fisheye_image'])
        self._save_image(image_response[0].shot.image, self._path)
       

    def on_exit(self, userdata):
        # This method is called when an outcome is returned and another state gets active.
        # It can be used to stop possibly running processes started by on_enter.

        pass # Nothing to do in this example.


    def on_start(self):
        # This method is called when the behavior is started.
        # If possible, it is generally better to initialize used resources in the constructor
        # because if anything failed, the behavior would not even be started.

        pass


    def on_stop(self):
        # This method is called whenever the behavior stops execution, also if it is cancelled.
        # Use this event to clean up things like claimed resources.

        pass # Nothing to do in this example.
        
