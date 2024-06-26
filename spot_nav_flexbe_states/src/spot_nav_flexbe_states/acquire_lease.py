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
import time

class AcquireLease(EventState):
    '''
    This state is used for acquiring the lease.

    -- None
    
    ># lease                LeaseClient         lease client
    #> lease_obj                                acquired lease object

    '''

    def __init__(self):
        # Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
        super(AcquireLease, self).__init__(outcomes = ['continue', 'failed'],
                                            input_keys=['lease'],
                                            output_keys=['lease_obj'])
        self._lease_obj = None


    def execute(self, userdata):
        # This method is called periodically while the state is active.
        userdata.lease_obj = self._lease_obj
        return 'continue'
        

    def on_enter(self, userdata):
        # This method is called when the state becomes active, i.e. a transition from another state to this one is taken.
        # It is primarily used to start actions which are associated with this state.        
        self._lease_obj = userdata.lease.acquire()


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
        
