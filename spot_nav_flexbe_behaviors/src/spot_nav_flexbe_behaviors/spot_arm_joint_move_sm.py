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
from spot_nav_flexbe_states.arm_move_joints import ArmMoveJoints
from spot_nav_flexbe_states.dock import Dock
from spot_nav_flexbe_states.return_lease import ReturnLease
from spot_nav_flexbe_states.setup_spot import SetupSpot
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri November 3 2023
@author: Yash P
'''
class SpotArmJointMoveSM(Behavior):
	'''
	Spot Arm Joint Move
	'''


	def __init__(self):
		super(SpotArmJointMoveSM, self).__init__()
		self.name = 'Spot Arm Joint Move'

		# parameters of this behavior
		self.add_parameter('true', True)
		self.add_parameter('dock_id', 520)
		self.add_parameter('false', False)
		self.add_parameter('sh0', '0.0692')
		self.add_parameter('sh1', '-1.882')
		self.add_parameter('el0', '1.652')
		self.add_parameter('el1', '-0.0691')
		self.add_parameter('wr0', '1.622')
		self.add_parameter('wr1', '1.550')

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:83 y:430, x:543 y:229
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

			# x:806 y:145
			OperatableStateMachine.add('ArmJointMove',
										ArmMoveJoints(sh0=self.sh0, sh1=self.sh1, el0=self.el0, el1=self.el1, wr0=self.wr0, wr1=self.wr1),
										transitions={'success': 'Dock', 'failure': 'failed'},
										autonomy={'success': Autonomy.Off, 'failure': Autonomy.Off},
										remapping={'robot_command_client': 'robot_command_client', 'robot': 'robot', 'lease': 'lease'})

			# x:614 y:350
			OperatableStateMachine.add('Dock',
										Dock(should_dock=self.true, dock_id=self.dock_id),
										transitions={'continue': 'ReturnLease', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'robot_command_client': 'robot_command_client', 'license_client': 'license_client', 'robot': 'robot'})

			# x:243 y:317
			OperatableStateMachine.add('ReturnLease',
										ReturnLease(),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'lease_obj': 'lease_obj'})

			# x:583 y:50
			OperatableStateMachine.add('Undock',
										Dock(should_dock=self.false, dock_id=self.dock_id),
										transitions={'continue': 'ArmJointMove', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'robot_command_client': 'robot_command_client', 'license_client': 'license_client', 'robot': 'robot'})

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
