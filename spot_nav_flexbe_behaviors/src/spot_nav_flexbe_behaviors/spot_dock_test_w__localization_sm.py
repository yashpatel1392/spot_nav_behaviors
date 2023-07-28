#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from spot_nav_flexbe_states.dock import Dock
from spot_nav_flexbe_states.localize import Localize
from spot_nav_flexbe_states.setup_spot import SetupSpot
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jul 10 2023
@author: Yash P
'''
class SpotDockTestwLocalizationSM(Behavior):
	'''
	Spot Dock Test
	'''


	def __init__(self):
		super(SpotDockTestwLocalizationSM, self).__init__()
		self.name = 'Spot Dock Test w/ Localization'

		# parameters of this behavior
		self.add_parameter('dock', False)
		self.add_parameter('dock_id', 0)
		self.add_parameter('waypoint_id', '')

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:869 y:295, x:351 y:310
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:159 y:90
			OperatableStateMachine.add('Setup',
										SetupSpot(),
										transitions={'continue': 'Dock', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client', 'lease': 'lease', 'power_client': 'power_client', 'robot_command_client': 'robot_command_client', 'license_client': 'license_client', 'robot': 'robot'})

			# x:652 y:164
			OperatableStateMachine.add('Localize',
										Localize(initial_waypoint=self.waypoint_id),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client'})

			# x:480 y:26
			OperatableStateMachine.add('Dock',
										Dock(should_dock=self.dock, dock_id=self.dock_id),
										transitions={'continue': 'Localize', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'robot_command_client': 'robot_command_client', 'license_client': 'license_client', 'robot': 'robot'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
