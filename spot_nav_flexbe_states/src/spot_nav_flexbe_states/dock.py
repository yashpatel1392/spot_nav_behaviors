#!/usr/bin/env python
import rospy

from flexbe_core import EventState, Logger
from bosdyn.client.util import *
from bosdyn.client.lease import LeaseClient, LeaseKeepAlive

from bosdyn.client.frame_helpers import get_odom_tform_body
from bosdyn.api.graph_nav import nav_pb2, graph_nav_pb2
from bosdyn.client.robot_state import RobotStateClient
from bosdyn.client.graph_nav import GraphNavClient
from bosdyn.client import robot_command
from bosdyn.client.docking import DockingClient, blocking_dock_robot, blocking_undock, get_dock_id
from bosdyn.client.lease import LeaseClient
from bosdyn.client.license import LicenseClient
import math


class Dock(EventState):
    '''
    This state is used for docking or undocking the robot.
    
    -- should_dock          boolean         true would the dock the robot, while false would undock
    -- dock_id              int             dock id of the docking station

    ># robot_command_client             RobotCommandClient          
    ># robot                            robot object representing the robot
    ># lease                            Lease object
    ># license_client                   LicenseClient    

    #> None

    '''

    def __init__(self, should_dock, dock_id):
        # Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
        super(Dock, self).__init__(outcomes = ['continue', 'failed'],
                                   input_keys = ['lease', 'robot_command_client', 'license_client', 'robot'])
        self._should_dock = should_dock
        self._dock_id = dock_id
        self._return_failure = bool


    def execute(self, userdata):
        print("in execute")
        if self._return_failure:
            return 'failed'
        else:
            return 'continue'
        

    def on_enter(self, userdata):
        # This method is called when the state becomes active, i.e. a transition from another state to this one is taken.
        # It is primarily used to start actions which are associated with this state.
        print("on enter.........")
        
        if not userdata.license_client.get_feature_enabled([DockingClient.default_service_name
                                                ])[DockingClient.default_service_name]:
            print('This robot is not licensed for docking.')
            sys.exit(1)

        with LeaseKeepAlive(userdata.lease): #, must_acquire=True, return_at_exit=True):
        
        # print("acquiring the lease..............")
        # lease_obj = userdata.lease.acquire()
        # print("acquired the lease..............")
        
            userdata.robot.power_on()
            
            if self._should_dock:
                print("docking the robot at ", self._dock_id)
                robot_command.blocking_stand(userdata.robot_command_client)
                blocking_dock_robot(userdata.robot, self._dock_id)
                self._return_failure = False
                print("successfully docked the robot at the given dock id............................")
            else:
                print("undocking the robot....................")
                dock_id = get_dock_id(userdata.robot)
                print("dock_id found is ", dock_id)
                print("dock_id given is ", self._dock_id)
                if dock_id != self._dock_id:
                    print("dock ids doesn't match..........................")
                    self._return_failure = True
                else:
                    blocking_undock(userdata.robot)
                    self._return_failure = False
                    print("successfully undocked the robot from dock id ", dock_id, "......................")
        
        # print("returning the lease................")
        # userdata.lease.return_lease(lease_obj)
        # print("returned the lease................")
            
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
        
