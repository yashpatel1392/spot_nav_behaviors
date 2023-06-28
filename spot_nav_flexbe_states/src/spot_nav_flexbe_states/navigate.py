#!/usr/bin/env python
import rospy

from flexbe_core import EventState, Logger
from bosdyn.api.graph_nav import nav_pb2, graph_nav_pb2
from bosdyn.client.graph_nav import GraphNavClient
from bosdyn.client.lease import LeaseClient, LeaseKeepAlive
from bosdyn.client.power import PowerClient, power_on_motors, safe_power_off_motors, robot_state_pb2, power_pb2
from bosdyn.client.robot_state import RobotStateClient
from bosdyn.client.robot_command import RobotCommandBuilder, RobotCommandClient
from bosdyn.client.exceptions import ResponseError
import time

class NavigateTo(EventState):
	'''
	Example for a state to demonstrate which functionality is available for state implementation.
	This example lets the behavior wait until the given target_time has passed since the behavior has been started.

	-- target_time 	float 	Time which needs to have passed since the behavior started.

	<= continue 			Given time has passed.
	<= failed 				Example for a failure outcome.

	'''

	def __init__(self, destination_waypoint):
		# Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
		super(NavigateTo, self).__init__(outcomes = ['continue', 'failed'],
                                   		input_keys = ['state_client', 'graph_nav_client', 'lease', 'power_client', 'robot_command_client'])
		self._destination_waypoint = destination_waypoint
		self._started_powered_on = bool
		self._powered_on = bool
		


	# Taken from spot-sdk examples
	def _check_success(self, command_id=-1, graph_nav_client=None):
		"""Use a navigation command id to get feedback from the robot and sit when command succeeds."""
		if command_id == -1:
			# No command, so we have no status to check.
			return False
		status = graph_nav_client.navigation_feedback(command_id)
		if status.status == graph_nav_pb2.NavigationFeedbackResponse.STATUS_REACHED_GOAL:
			# Successfully completed the navigation commands!
			return True
		elif status.status == graph_nav_pb2.NavigationFeedbackResponse.STATUS_LOST:
			print('Robot got lost when navigating the route, the robot will now sit down.')
			return True
		elif status.status == graph_nav_pb2.NavigationFeedbackResponse.STATUS_STUCK:
			print('Robot got stuck when navigating the route, the robot will now sit down.')
			return True
		elif status.status == graph_nav_pb2.NavigationFeedbackResponse.STATUS_ROBOT_IMPAIRED:
			print('Robot is impaired.')
			return True
		else:
			# Navigation command is not complete yet.
			return False

	def check_is_powered_on(self, state_client):
		"""Determine if the robot is powered on or off."""
		power_state = state_client.get_robot_state().power_state
		self._powered_on = (power_state.motor_power_state == power_state.STATE_ON)
		return self._powered_on

	def toggle_power(self, should_power_on, state_client, power_client, robot_command_client):
		"""Power the robot on/off dependent on the current power state."""
		is_powered_on = self.check_is_powered_on(state_client)
		if not is_powered_on and should_power_on:
			# Power on the robot up before navigating when it is in a powered-off state.
			power_on_motors(power_client)
			motors_on = False
			while not motors_on:
				future = state_client.get_robot_state_async()
				state_response = future.result(
					timeout=10)  # 10 second timeout for waiting for the state response.
				if state_response.power_state.motor_power_state == robot_state_pb2.PowerState.STATE_ON:
					motors_on = True
				else:
					# Motors are not yet fully powered on.
					time.sleep(.25)
		elif is_powered_on and not should_power_on:
			# Safe power off (robot will sit then power down) when it is in a
			# powered-on state.
			safe_power_off_motors(robot_command_client, state_client)
		else:
			# Return the current power state without change.
			return is_powered_on
		# Update the locally stored power state.
		self.check_is_powered_on(state_client)
		return self._powered_on

	def execute(self, userdata):
		# This method is called periodically while the state is active.
		# Main purpose is to check state conditions and trigger a corresponding outcome.
		# If no outcome is returned, the state will stay active.
  
		print("acquiring the lease.........................................")
		with LeaseKeepAlive(userdata.lease, must_acquire=True, return_at_exit=True):
			print("turning the power on...........................................")
			if not self.toggle_power(should_power_on=True, state_client=userdata.state_client, power_client=userdata.power_client, robot_command_client=userdata.robot_command_client):
				print("not powered on..........")
				return 'failed'

			nav_to_cmd_id = None
			is_finished = False

			print("entering while loop...........")
			while not is_finished:
				try:
					print("issuing nav command................")
					nav_to_cmd_id = userdata.graph_nav_client.navigate_to(self._destination_waypoint, 1.0,
																		command_id=nav_to_cmd_id)
					print("done issuing nav command................")
				except ResponseError as e:
					print(f'Error while navigating {e}')
					break

				time.sleep(.5)
				print("is_finished BEFORE checking: ", is_finished)
				is_finished = self._check_success(nav_to_cmd_id, userdata.graph_nav_client)
				print("is_finished AFTER checking: ", is_finished)

			if self._powered_on and not self._started_powered_on:
				print("turning power down..........................")
				self.toggle_power(should_power_on=False, state_client=userdata.state_client, power_client=userdata.power_client, robot_command_client=userdata.robot_command_client)

			print("powered off.........")
 
		return 'continue' # One of the outcomes declared above.
		

	def on_enter(self, userdata):
		# This method is called when the state becomes active, i.e. a transition from another state to this one is taken.
		# It is primarily used to start actions which are associated with this state.

		power_state = userdata.state_client.get_robot_state().power_state
		self._started_powered_on = (power_state.motor_power_state == power_state.STATE_ON)
		self._powered_on = self._started_powered_on

		
	def on_exit(self, userdata):
		# This method is called when an outcome is returned and another state gets active.
		# It can be used to stop possibly running processes started by on_enter.

		pass # Nothing to do in this example.


	def on_start(self):
		# This method is called when the behavior is started.
		pass


	def on_stop(self):
		# This method is called whenever the behavior stops execution, also if it is cancelled.
		# Use this event to clean up things like claimed resources.

		pass # Nothing to do in this example.
		
