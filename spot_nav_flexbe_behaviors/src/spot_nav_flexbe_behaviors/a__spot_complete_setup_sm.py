#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from spot_nav_flexbe_states.acquire_lease import AcquireLease
from spot_nav_flexbe_states.dock import Dock
from spot_nav_flexbe_states.get_arm_data import GetArmData
from spot_nav_flexbe_states.localize import Localize
from spot_nav_flexbe_states.navigate import NavigateTo
from spot_nav_flexbe_states.return_lease import ReturnLease
from spot_nav_flexbe_states.setup_spot import SetupSpot
from spot_nav_flexbe_states.upload_map import UploadMap
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon July 20 2023
@author: Yash P
'''
class ASpotCompleteSetupSM(Behavior):
	'''
	Spot Navigation Test with Dock and Map Verification
	'''


	def __init__(self):
		super(ASpotCompleteSetupSM, self).__init__()
		self.name = 'A: Spot Complete Setup'

		# parameters of this behavior
		self.add_parameter('init_waypoint_id', 'blotto-guppy-Jj5vrF7oTWyVx7IRyczxqA==')
		self.add_parameter('goal_waypoint_id', 'teal-drum-Gq4bd4gH8yKFst771bHEtg==')
		self.add_parameter('true', True)
		self.add_parameter('false', False)
		self.add_parameter('dock_id', 520)
		self.add_parameter('change_map', False)
		self.add_parameter('path_to_map', 'spot-sdk/spot_maps/mini_map_back_area/downloaded_graph')

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:101 y:257, x:646 y:215
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:68 y:141
			OperatableStateMachine.add('SetupSpot',
										SetupSpot(),
										transitions={'continue': 'VerifyMapStatus', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client', 'lease': 'lease', 'power_client': 'power_client', 'robot_command_client': 'robot_command_client', 'license_client': 'license_client', 'robot': 'robot', 'image_client': 'image_client', 'manipulation_api_client': 'manipulation_api_client'})

			# x:510 y:22
			OperatableStateMachine.add('AcquireLease',
										AcquireLease(),
										transitions={'continue': 'Undock', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'lease_obj': 'lease_obj'})

			# x:385 y:373
			OperatableStateMachine.add('Dock',
										Dock(should_dock=self.true, dock_id=self.dock_id),
										transitions={'continue': 'ReturnLease', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'robot_command_client': 'robot_command_client', 'license_client': 'license_client', 'robot': 'robot'})

			# x:1067 y:442
			OperatableStateMachine.add('GetArmPose',
										GetArmData(),
										transitions={'success': 'AcquireAgain'},
										autonomy={'success': Autonomy.Off},
										remapping={'state_client': 'state_client'})

			# x:1098 y:25
			OperatableStateMachine.add('Localize',
										Localize(initial_waypoint=self.init_waypoint_id),
										transitions={'continue': 'NavigateToGoal', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client'})

			# x:1121 y:168
			OperatableStateMachine.add('NavigateToGoal',
										NavigateTo(destination_waypoint=self.goal_waypoint_id),
										transitions={'continue': 'ReturnLease1', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client', 'lease': 'lease', 'power_client': 'power_client', 'robot_command_client': 'robot_command_client'})

			# x:589 y:463
			OperatableStateMachine.add('NavigateToStart',
										NavigateTo(destination_waypoint=self.init_waypoint_id),
										transitions={'continue': 'Dock', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client', 'lease': 'lease', 'power_client': 'power_client', 'robot_command_client': 'robot_command_client'})

			# x:202 y:261
			OperatableStateMachine.add('ReturnLease',
										ReturnLease(),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'lease_obj': 'lease_obj'})

			# x:1167 y:307
			OperatableStateMachine.add('ReturnLease1',
										ReturnLease(),
										transitions={'continue': 'GetArmPose', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'lease_obj': 'lease_obj'})

			# x:760 y:29
			OperatableStateMachine.add('Undock',
										Dock(should_dock=self.false, dock_id=self.dock_id),
										transitions={'continue': 'Localize', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'robot_command_client': 'robot_command_client', 'license_client': 'license_client', 'robot': 'robot'})

			# x:271 y:37
			OperatableStateMachine.add('VerifyMapStatus',
										UploadMap(path_to_graph=self.path_to_map, should_upload=self.change_map),
										transitions={'success': 'AcquireLease', 'failed': 'failed'},
										autonomy={'success': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'graph_nav_client': 'graph_nav_client'})

			# x:839 y:432
			OperatableStateMachine.add('AcquireAgain',
										AcquireLease(),
										transitions={'continue': 'NavigateToStart', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'lease_obj': 'lease_obj'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
