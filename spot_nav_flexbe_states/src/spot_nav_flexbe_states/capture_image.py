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
from datetime import datetime
from scipy import ndimage
from bosdyn.api import image_pb2


class CaptureImage(EventState):
    '''
    sources: all (for getting images from all of the following sources), back_fisheye_image, frontleft_fisheye_image, frontright_fisheye_image, hand_color_image, left_fisheye_image, right_fisheye_image

    -- image_source 	string 	    specify the image source(s) to capture image from 

    <= continue 			Given time has passed.
    <= failed 				Example for a failure outcome.

    '''

    def __init__(self, path, image_source):
        # Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
        super(CaptureImage, self).__init__(outcomes = ['continue', 'failed'],
                                            input_keys = ['image_client'],
                                            output_keys = ['image_response'])
        self._path = path
        self._angle_dict = {
            'back_fisheye_image': 0,
            'frontleft_fisheye_image': -78,
            'frontright_fisheye_image': -102,
            'left_fisheye_image': 0,
            'right_fisheye_image': 180
        }
        self._image_source = image_source

    def _save_image(self, image, path, source_name):
        currentDateTime = datetime.now()
        currentTime = currentDateTime.strftime("%H-%M-%S")
                
        name = str(currentDateTime.month) + "-" + str(currentDateTime.day) + "-" + str(currentDateTime.year) + "_" + currentTime + "_" + source_name + ".jpg"
        
        if path is not None and os.path.exists(path):
            path = os.path.join(os.getcwd(), path)
            name = os.path.join(path, name)

        try:
            image = Image.open(io.BytesIO(image.data))
            image.save(name)
            print("Saving image to: ", name)
            if self._angle_dict[source_name] != 0:
                rotated_image = image.rotate(self._angle_dict[source_name])
                rotated_img_name = str(currentDateTime.month) + "-" + str(currentDateTime.day) + "-" + str(currentDateTime.year) + "_" + currentTime + "_" + source_name + "_ROTATED.jpg"
                rotated_img_name = os.path.join(path, rotated_img_name)
                rotated_image.save(rotated_img_name)
                print("Saving rotated image to: ", name)
                
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
        
        # currentDateTime = datetime.now()
        # currentTime = currentDateTime.strftime("%H:%M:%S")
        # self._path = self._path + "/" + str(currentDateTime.month) + "-" + str(currentDateTime.day) + "-" + str(currentDateTime.year) + "/" +  currentTime
        
        if not os.path.exists(self._path):
            os.makedirs(self._path)
            
        if self._image_source == 'all':
            self._source_list = ['back_fisheye_image', 'frontleft_fisheye_image', 'frontright_fisheye_image', 
                                'hand_color_image', 'left_fisheye_image', 'right_fisheye_image']
        else:
            self._source_list = self._image_source.split(', ')

        for source in self._source_list:
            image_response = userdata.image_client.get_image_from_sources([source])
            userdata.image_response = image_response
            self._save_image(image_response[0].shot.image, self._path, source)
       

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
        