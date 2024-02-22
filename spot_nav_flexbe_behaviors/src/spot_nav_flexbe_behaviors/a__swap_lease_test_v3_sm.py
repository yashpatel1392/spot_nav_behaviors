#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from spot_nav_flexbe_states.pause import PauseState
from spot_nav_flexbe_states.setup_spot import SetupSpot
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Feb 20 2024
@author: Yash P
'''
class ASwapLeaseTestv3SM(Behavior):
	'''
	Swap Lease Test v3
	'''


	def __init__(self):
		super(ASwapLeaseTestv3SM, self).__init__()
		self.name = 'A: Swap Lease Test v3'

		# parameters of this behavior
		self.add_parameter('topic', 'cont')

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:790 y:138, x:380 y:269
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:172 y:118
			OperatableStateMachine.add('Setup',
										SetupSpot(),
										transitions={'continue': 'pause', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client', 'lease': 'lease', 'power_client': 'power_client', 'robot_command_client': 'robot_command_client', 'license_client': 'license_client', 'robot': 'robot', 'image_client': 'image_client', 'manipulation_api_client': 'manipulation_api_client'})

			# x:486 y:118
			OperatableStateMachine.add('pause',
										PauseState(topic=self.topic),
										transitions={'success': 'finished'},
										autonomy={'success': Autonomy.Off},
										remapping={'state_client': 'state_client'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
