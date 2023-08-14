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
from spot_nav_flexbe_states.pause import PauseState
from spot_nav_flexbe_states.return_lease import ReturnLease
from spot_nav_flexbe_states.setup_spot import SetupSpot
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jul 10 2023
@author: Yash P
'''
class SpotDockTestwPauseSM(Behavior):
	'''
	Spot Dock Test
	'''


	def __init__(self):
		super(SpotDockTestwPauseSM, self).__init__()
		self.name = 'Spot Dock Test w/ Pause'

		# parameters of this behavior
		self.add_parameter('dock', False)
		self.add_parameter('dock_id', 0)
		self.add_parameter('topic', '')

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1131 y:335, x:522 y:318
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:65 y:178
			OperatableStateMachine.add('Setup',
										SetupSpot(),
										transitions={'continue': 'AcquireLease', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client', 'lease': 'lease', 'power_client': 'power_client', 'robot_command_client': 'robot_command_client', 'license_client': 'license_client', 'robot': 'robot', 'image_client': 'image_client'})

			# x:554 y:17
			OperatableStateMachine.add('Dock',
										Dock(should_dock=self.dock, dock_id=self.dock_id),
										transitions={'continue': 'Pause', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'robot_command_client': 'robot_command_client', 'license_client': 'license_client', 'robot': 'robot'})

			# x:784 y:23
			OperatableStateMachine.add('Pause',
										PauseState(topic=self.topic),
										transitions={'success': 'ReturnLease'},
										autonomy={'success': Autonomy.Off})

			# x:1022 y:76
			OperatableStateMachine.add('ReturnLease',
										ReturnLease(),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'lease_obj': 'lease_obj'})

			# x:280 y:32
			OperatableStateMachine.add('AcquireLease',
										AcquireLease(),
										transitions={'continue': 'Dock', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'lease_obj': 'lease_obj'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
