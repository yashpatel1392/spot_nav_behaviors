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
from spot_nav_flexbe_states.arm_stow_unstow import ArmStowUnstow
from spot_nav_flexbe_states.dock import Dock
from spot_nav_flexbe_states.return_lease import ReturnLease
from spot_nav_flexbe_states.setup_spot import SetupSpot
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri October 20 2023
@author: Yash P
'''
class SpotArmStowUnstowTestSM(Behavior):
	'''
	Spot Arm Stow Unstow Test
	'''


	def __init__(self):
		super(SpotArmStowUnstowTestSM, self).__init__()
		self.name = 'Spot Arm Stow Unstow Test'

		# parameters of this behavior
		self.add_parameter('true', True)
		self.add_parameter('dock_id', 520)
		self.add_parameter('waittime', 10)
		self.add_parameter('false', False)

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:83 y:430, x:679 y:249
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:125 y:177
			OperatableStateMachine.add('Setup',
										SetupSpot(),
										transitions={'continue': 'AcquireLease', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client', 'lease': 'lease', 'power_client': 'power_client', 'robot_command_client': 'robot_command_client', 'license_client': 'license_client', 'robot': 'robot', 'image_client': 'image_client'})

			# x:644 y:433
			OperatableStateMachine.add('Dock',
										Dock(should_dock=self.true, dock_id=self.dock_id),
										transitions={'continue': 'ReturnLease', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'robot_command_client': 'robot_command_client', 'license_client': 'license_client', 'robot': 'robot'})

			# x:263 y:332
			OperatableStateMachine.add('ReturnLease',
										ReturnLease(),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'lease_obj': 'lease_obj'})

			# x:583 y:50
			OperatableStateMachine.add('Undock',
										Dock(should_dock=self.false, dock_id=self.dock_id),
										transitions={'continue': 'unstow', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'robot_command_client': 'robot_command_client', 'license_client': 'license_client', 'robot': 'robot'})

			# x:1056 y:158
			OperatableStateMachine.add('WaitFor10',
										WaitState(wait_time=self.waittime),
										transitions={'done': 'stow'},
										autonomy={'done': Autonomy.Off})

			# x:936 y:328
			OperatableStateMachine.add('stow',
										ArmStowUnstow(stow=self.true),
										transitions={'success': 'Dock', 'failure': 'failed'},
										autonomy={'success': Autonomy.Off, 'failure': Autonomy.Off},
										remapping={'robot_command_client': 'robot_command_client', 'robot': 'robot', 'lease': 'lease'})

			# x:828 y:60
			OperatableStateMachine.add('unstow',
										ArmStowUnstow(stow=self.false),
										transitions={'success': 'WaitFor10', 'failure': 'failed'},
										autonomy={'success': Autonomy.Off, 'failure': Autonomy.Off},
										remapping={'robot_command_client': 'robot_command_client', 'robot': 'robot', 'lease': 'lease'})

			# x:323 y:54
			OperatableStateMachine.add('AcquireLease',
										AcquireLease(),
										transitions={'continue': 'Undock', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'lease_obj': 'lease_obj'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
