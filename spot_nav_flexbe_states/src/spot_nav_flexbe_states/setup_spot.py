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

class SetupSpot(EventState):
	'''
	Example for a state to demonstrate which functionality is available for state implementation.
	This example lets the behavior wait until the given target_time has passed since the behavior has been started.

	-- target_time 	float 	Time which needs to have passed since the behavior started.

	<= continue 			Given time has passed.
	<= failed 				Example for a failure outcome.

	'''

	def __init__(self):
		# Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
		super(SetupSpot, self).__init__(outcomes = ['continue', 'failed'],
                                  		output_keys=['state_client', 'graph_nav_client', 'lease', 'power_client', 'robot_command_client', 'license_client', 'robot', 'lease_obj'])
		self._sdk = None
		self._robot = None
		self._lease = None
		self._state_client = None
		self._graph_nav_client = None
		self._power_client = None
		self._robot_command_client = None
		self._license_client = None
		self._lease_obj = None


	def execute(self, userdata):
		# This method is called periodically while the state is active.
		# with LeaseKeepAlive(self._lease, must_acquire=True, return_at_exit=True):
			# userdata.sdk = self._sdk
			# userdata.robot = self._robot
			# userdata.lease = self._lease
		self._lease_obj = self._lease.acquire()
		userdata.lease_obj = self._lease_obj
		userdata.state_client = self._state_client
		userdata.graph_nav_client = self._graph_nav_client
		userdata.lease = self._lease
		userdata.power_client = self._power_client
		userdata.robot_command_client = self._robot_command_client
		userdata.license_client = self._license_client
		userdata.robot = self._robot
		return 'continue'
		

	def on_enter(self, userdata):
		# This method is called when the state becomes active, i.e. a transition from another state to this one is taken.
		# It is primarily used to start actions which are associated with this state.
		
		print("Creating sdk.................")
		self._sdk = bosdyn.client.create_standard_sdk('Spot FlexBe Client')
		print("Done creating sdk.................")
		
		print("Creating robot object.................")
		self._robot = self._sdk.create_robot('192.168.80.3') # check if the hostname should be the spot's ip or core's...............
		print("Done creating robot object.................")

		print("Authenticating robot.................")
		bosdyn.client.util.authenticate(self._robot)
		print("Done authenticating robot.................")
		
		# This is how to specify spot's credentials (if dont want to type everytime!)
		# export BOSDYN_CLIENT_USERNAME=user 
		# export BOSDYN_CLIENT_PASSWORD=password

		print("Creating lease object.................")
		self._lease = self._robot.ensure_client(LeaseClient.default_service_name)
		print("Done creating lease object.................")
  
		print("Creating state client.................")
		self._state_client = self._robot.ensure_client(RobotStateClient.default_service_name)
		print("Done creating state client.................")
  
		print("Creating graph nav client.................")
		self._graph_nav_client = self._robot.ensure_client(GraphNavClient.default_service_name)
		print("Creating graph nav client.................")
  
		self._power_client = self._robot.ensure_client(PowerClient.default_service_name)
		self._robot_command_client = self._robot.ensure_client(RobotCommandClient.default_service_name)
		self._license_client = self._robot.ensure_client(LicenseClient.default_service_name)

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
		
