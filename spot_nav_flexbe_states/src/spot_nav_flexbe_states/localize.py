#!/usr/bin/env python
import rospy

from flexbe_core import EventState, Logger
from bosdyn.client.util import *
from bosdyn.client.lease import LeaseClient, LeaseKeepAlive

from bosdyn.client.frame_helpers import get_odom_tform_body
from bosdyn.api.graph_nav import nav_pb2, graph_nav_pb2
from bosdyn.client.robot_state import RobotStateClient
from bosdyn.client.graph_nav import GraphNavClient
import math


class Localize(EventState):
    '''
    Example for a state to demonstrate which functionality is available for state implementation.
    This example lets the behavior wait until the given target_time has passed since the behavior has been started.


    <= continue 			Given time has passed.
    <= failed 				Example for a failure outcome.

    '''

    def __init__(self, initial_waypoint):
        # Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
        super(Localize, self).__init__(outcomes = ['continue', 'failed'],
                                       input_keys = ['state_client', 'graph_nav_client'])
        self._initial_waypoint = initial_waypoint
        self._state_client = None
                

    def execute(self, userdata):
        localized_state = userdata.graph_nav_client.get_localization_state()
        print("Localized at: ", localized_state)
        
        return 'continue'
        

    def on_enter(self, userdata):
        # This method is called when the state becomes active, i.e. a transition from another state to this one is taken.
        # It is primarily used to start actions which are associated with this state.
        print("on enter.........")
        
        print(self._initial_waypoint)
        
        self._robot_state = userdata.state_client.get_robot_state()
        self._Current_odom_body = get_odom_tform_body(self._robot_state.kinematic_state.transforms_snapshot).to_proto()
        
        localization = nav_pb2.Localization()
        localization.waypoint_id = self._initial_waypoint
        localization.waypoint_tform_body.rotation.w = 1.0
        
        userdata.graph_nav_client.set_localization(
            initial_guess_localization=localization,
            max_distance=0.2,
            max_yaw=20.0 * math.pi / 180.0,
            fiducial_init=graph_nav_pb2.SetLocalizationRequest.FIDUCIAL_INIT_NO_FIDUCIAL,
            ko_tform_body=self._Current_odom_body)
        
        print("done on enter............")


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
        
