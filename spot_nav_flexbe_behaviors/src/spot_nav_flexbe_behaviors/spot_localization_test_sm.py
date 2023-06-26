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
from spot_nav_flexbe_states.setup_spot import SetupSpot
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jun 26 2023
@author: Yash P
'''
class SpotLocalizationTestSM(Behavior):
	'''
	Spot Localization Test
	'''


	def __init__(self):
		super(SpotLocalizationTestSM, self).__init__()
		self.name = 'Spot Localization Test'

		# parameters of this behavior
		self.add_parameter('init_waypoint', 'eighty-drum-3hz7jJNJ81RLN5fJavoEhg==')

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:835 y:206, x:372 y:400
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
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client'})

			# x:500 y:127
			OperatableStateMachine.add('Localize',
										Localize(initial_waypoint=self.init_waypoint),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
