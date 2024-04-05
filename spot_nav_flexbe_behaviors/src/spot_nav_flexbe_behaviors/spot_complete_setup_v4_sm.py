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
from spot_nav_flexbe_states.capture_image import CaptureImage
from spot_nav_flexbe_states.counter import CounterState
from spot_nav_flexbe_states.dock import Dock
from spot_nav_flexbe_states.localize import Localize
from spot_nav_flexbe_states.navigate import NavigateTo
from spot_nav_flexbe_states.return_lease import ReturnLease
from spot_nav_flexbe_states.setup_spot import SetupSpot
from spot_nav_flexbe_states.upload_map import UploadMap
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu March 21 2024
@author: Yash P
'''
class SpotCompleteSetupv4SM(Behavior):
	'''
	Spot Navigation Test with Dock and Map Verification
	'''


	def __init__(self):
		super(SpotCompleteSetupv4SM, self).__init__()
		self.name = 'Spot Complete Setup v4'

		# parameters of this behavior
		self.add_parameter('init_waypoint_id', 'matte-ape-bNBbkPwfxYyRffew6.f1Dg==')
		self.add_parameter('goal_waypoint_id', 'skimpy-gaur-MNwYmUO39hVr4JGSeJZ3Mw==')
		self.add_parameter('true', True)
		self.add_parameter('false', False)
		self.add_parameter('reps', 1)
		self.add_parameter('dock_id', 520)
		self.add_parameter('change_map', False)
		self.add_parameter('path_to_map', 'spot-sdk/spot_maps/first_floor_map/downloaded_graph')
		self.add_parameter('image_path', '../spot_images')
		self.add_parameter('image_source', 'hand_color_image')

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:62 y:257, x:531 y:215
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.num_reps_IN = self.reps

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:58 y:425, x:589 y:178
		_sm_container_0 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['state_client', 'graph_nav_client', 'lease', 'power_client', 'robot_command_client', 'num_reps_IN', 'robot', 'image_client'])

		with _sm_container_0:
			# x:123 y:87
			OperatableStateMachine.add('CounterCheck',
										CounterState(decrement=self.false),
										transitions={'success': 'NavigateToDest', 'failed': 'failed', 'end': 'finished'},
										autonomy={'success': Autonomy.Off, 'failed': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'num_reps': 'num_reps_IN', 'num_reps_remaining': 'num_reps_OUT'})

			# x:302 y:242
			OperatableStateMachine.add('DecrementCounter',
										CounterState(decrement=self.true),
										transitions={'success': 'CounterCheck', 'failed': 'failed', 'end': 'finished'},
										autonomy={'success': Autonomy.Off, 'failed': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'num_reps': 'num_reps_OUT', 'num_reps_remaining': 'num_reps_IN'})

			# x:542 y:28
			OperatableStateMachine.add('NavigateToDest',
										NavigateTo(destination_waypoint=self.goal_waypoint_id),
										transitions={'continue': 'CaptureImage', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client', 'lease': 'lease', 'power_client': 'power_client', 'robot_command_client': 'robot_command_client'})

			# x:583 y:343
			OperatableStateMachine.add('NavigateToStartPos',
										NavigateTo(destination_waypoint=self.init_waypoint_id),
										transitions={'continue': 'DecrementCounter', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client', 'lease': 'lease', 'power_client': 'power_client', 'robot_command_client': 'robot_command_client'})

			# x:871 y:180
			OperatableStateMachine.add('CaptureImage',
										CaptureImage(path=self.image_path, image_source=self.image_source),
										transitions={'continue': 'NavigateToStartPos', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'image_client': 'image_client', 'image_response': 'image_response'})



		with _state_machine:
			# x:68 y:141
			OperatableStateMachine.add('SetupSpot',
										SetupSpot(),
										transitions={'continue': 'VerifyMapStatus', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client', 'lease': 'lease', 'power_client': 'power_client', 'robot_command_client': 'robot_command_client', 'license_client': 'license_client', 'robot': 'robot', 'image_client': 'image_client', 'manipulation_api_client': 'manipulation_api_client'})

			# x:806 y:309
			OperatableStateMachine.add('Container',
										_sm_container_0,
										transitions={'finished': 'Dock', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client', 'lease': 'lease', 'power_client': 'power_client', 'robot_command_client': 'robot_command_client', 'num_reps_IN': 'num_reps_IN', 'robot': 'robot', 'image_client': 'image_client'})

			# x:483 y:379
			OperatableStateMachine.add('Dock',
										Dock(should_dock=self.true, dock_id=self.dock_id),
										transitions={'continue': 'ReturnLease', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'robot_command_client': 'robot_command_client', 'license_client': 'license_client', 'robot': 'robot'})

			# x:834 y:139
			OperatableStateMachine.add('Localize',
										Localize(initial_waypoint=self.init_waypoint_id),
										transitions={'continue': 'Container', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client'})

			# x:209 y:288
			OperatableStateMachine.add('ReturnLease',
										ReturnLease(),
										transitions={'continue': 'finished', 'failed': 'failed'},
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

			# x:510 y:22
			OperatableStateMachine.add('AcquireLease',
										AcquireLease(),
										transitions={'continue': 'Undock', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'lease_obj': 'lease_obj'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
