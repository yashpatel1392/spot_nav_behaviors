#!/usr/bin/env python
import rospy

from flexbe_core import EventState, Logger
import bosdyn.client.util
from bosdyn.client.lease import LeaseClient


class SetupSpot(EventState):
	'''
	Example for a state to demonstrate which functionality is available for state implementation.
	This example lets the behavior wait until the given target_time has passed since the behavior has been started.

	-- target_time 	float 	Time which needs to have passed since the behavior started.

	<= continue 			Given time has passed.
	<= failed 				Example for a failure outcome.

	'''

	def __init__(self, username, password):
		# Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
		super(SetupSpot, self).__init__(outcomes = ['continue', 'failed'],
                                  		output_keys=['sdk', 'robot', 'lease'])
		self._sdk = None
		self._robot = None
		self._lease = None
		self._username = username
		self._password = password
	


	def execute(self, userdata):
		# This method is called periodically while the state is active.
		userdata.sdk = self._sdk
		userdata.robot = self._robot
		userdata.lease = self._lease
  
		return 'continue'
		

	def on_enter(self, userdata):
		# This method is called when the state becomes active, i.e. a transition from another state to this one is taken.
		# It is primarily used to start actions which are associated with this state.
		
		self._sdk = bosdyn.client.create_standard_sdk('Spot FlexBe Client')
		self._robot = self._sdk.create_robot(self._username) # check if the hostname should be the username...............
		bosdyn.client.util.authenticate(self._robot) 
  
		# alternative approach from spot's documentation
  
		# self._robot = self._sdk.create_robot('192.0.0.0') # check if the hostname should be the username...............
		# robot.authenticate('username', 'password')
  
		self._lease = self._robot.ensure_client(LeaseClient.default_service_name)
  

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
		
