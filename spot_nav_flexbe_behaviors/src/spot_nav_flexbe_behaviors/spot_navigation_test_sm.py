#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from spot_nav_flexbe_states.localize import Localize
from spot_nav_flexbe_states.navigate import NavigateTo
from spot_nav_flexbe_states.pause import PauseState
from spot_nav_flexbe_states.setup_spot import SetupSpot
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jun 26 2023
@author: Yash P
'''
class SpotNavigationTestSM(Behavior):
	'''
	Spot Navigation Test
	'''


	def __init__(self):
		super(SpotNavigationTestSM, self).__init__()
		self.name = 'Spot Navigation Test'

		# parameters of this behavior
		self.add_parameter('init_waypoint_id', 'eighty-drum-3hz7jJNJ81RLN5fJavoEhg==')
		self.add_parameter('goal_waypoint_id', 'cushy-dodo-SrmNEAcdcTsAepg.hh0FkA==')
		self.add_parameter('pause_topic', 'pause_topic')

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1187 y:459, x:372 y:400
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:121 y:126
			OperatableStateMachine.add('Setup',
										SetupSpot(),
										transitions={'continue': 'Localize', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client', 'lease': 'lease', 'power_client': 'power_client', 'robot_command_client': 'robot_command_client'})

			# x:980 y:187
			OperatableStateMachine.add('Navigate',
										NavigateTo(destination_waypoint=self.goal_waypoint_id),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client', 'lease': 'lease', 'power_client': 'power_client', 'robot_command_client': 'robot_command_client'})

			# x:723 y:117
			OperatableStateMachine.add('Pause',
										PauseState(topic=self.pause_topic),
										transitions={'success': 'Navigate'},
										autonomy={'success': Autonomy.Off})

			# x:461 y:76
			OperatableStateMachine.add('Localize',
										Localize(initial_waypoint=self.init_waypoint_id),
										transitions={'continue': 'Pause', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
