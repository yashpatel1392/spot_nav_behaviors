#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from spot_nav_flexbe_states.return_lease import ReturnLease
from spot_nav_flexbe_states.setup_spot import SetupSpot
from spot_nav_flexbe_states.upload_map import UploadMap
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jul 31 2023
@author: Yash P
'''
class SpotMapUploadTestSM(Behavior):
	'''
	Spot Map Upload Test
	'''


	def __init__(self):
		super(SpotMapUploadTestSM, self).__init__()
		self.name = 'Spot Map Upload Test'

		# parameters of this behavior
		self.add_parameter('graph_path', 'spot-sdk/spot_maps/nerve_first_floor_map/downloaded_graph')
		self.add_parameter('upload_graph', False)

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:904 y:114, x:331 y:244
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:132 y:59
			OperatableStateMachine.add('SetupSpot',
										SetupSpot(),
										transitions={'continue': 'UploadMap', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client', 'lease': 'lease', 'power_client': 'power_client', 'robot_command_client': 'robot_command_client', 'license_client': 'license_client', 'robot': 'robot', 'lease_obj': 'lease_obj'})

			# x:425 y:27
			OperatableStateMachine.add('UploadMap',
										UploadMap(path_to_graph=self.graph_path, should_upload=self.upload_graph),
										transitions={'success': 'ReturnLease', 'failed': 'failed'},
										autonomy={'success': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'graph_nav_client': 'graph_nav_client'})

			# x:687 y:33
			OperatableStateMachine.add('ReturnLease',
										ReturnLease(),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'lease_obj': 'lease_obj'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
