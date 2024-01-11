#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.wait_state import WaitState
from spot_nav_flexbe_states.acquire_lease import AcquireLease
from spot_nav_flexbe_states.power import Power
from spot_nav_flexbe_states.return_lease import ReturnLease
from spot_nav_flexbe_states.setup_spot import SetupSpot
from spot_nav_flexbe_states.stand_sit import StandSit
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu January 11 2024
@author: Yash P
'''
class SpotSitStandTestSM(Behavior):
	'''
	Spot Sit/Stand Test
	'''


	def __init__(self):
		super(SpotSitStandTestSM, self).__init__()
		self.name = 'Spot Sit/Stand Test'

		# parameters of this behavior
		self.add_parameter('true', True)
		self.add_parameter('waittime', 10)
		self.add_parameter('false', False)

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:45 y:363, x:542 y:144
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:100 y:141
			OperatableStateMachine.add('Setup',
										SetupSpot(),
										transitions={'continue': 'AcquireLease', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client', 'lease': 'lease', 'power_client': 'power_client', 'robot_command_client': 'robot_command_client', 'license_client': 'license_client', 'robot': 'robot', 'image_client': 'image_client'})

			# x:387 y:295
			OperatableStateMachine.add('PowerOFF',
										Power(on=self.false),
										transitions={'success': 'ReturnLease', 'failure': 'failed'},
										autonomy={'success': Autonomy.Off, 'failure': Autonomy.Off},
										remapping={'robot_command_client': 'robot_command_client', 'robot': 'robot', 'lease': 'lease'})

			# x:638 y:9
			OperatableStateMachine.add('PowerON',
										Power(on=self.true),
										transitions={'success': 'Stand', 'failure': 'failed'},
										autonomy={'success': Autonomy.Off, 'failure': Autonomy.Off},
										remapping={'robot_command_client': 'robot_command_client', 'robot': 'robot', 'lease': 'lease'})

			# x:148 y:233
			OperatableStateMachine.add('ReturnLease',
										ReturnLease(),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'lease_obj': 'lease_obj'})

			# x:652 y:342
			OperatableStateMachine.add('Sit',
										StandSit(stand=self.false),
										transitions={'success': 'PowerOFF', 'failure': 'failed'},
										autonomy={'success': Autonomy.Off, 'failure': Autonomy.Off},
										remapping={'robot_command_client': 'robot_command_client', 'robot': 'robot', 'lease': 'lease'})

			# x:938 y:55
			OperatableStateMachine.add('Stand',
										StandSit(stand=self.true),
										transitions={'success': 'WaitFor10', 'failure': 'failed'},
										autonomy={'success': Autonomy.Off, 'failure': Autonomy.Off},
										remapping={'robot_command_client': 'robot_command_client', 'robot': 'robot', 'lease': 'lease'})

			# x:973 y:210
			OperatableStateMachine.add('WaitFor10',
										WaitState(wait_time=self.waittime),
										transitions={'done': 'Sit'},
										autonomy={'done': Autonomy.Off})

			# x:286 y:31
			OperatableStateMachine.add('AcquireLease',
										AcquireLease(),
										transitions={'continue': 'PowerON', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'lease_obj': 'lease_obj'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
