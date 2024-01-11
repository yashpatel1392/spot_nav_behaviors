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
from spot_nav_flexbe_states.arm_stow_unstow import ArmStowUnstow
from spot_nav_flexbe_states.gripper_control import GripperControl
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
class SpotGripperTestv3SM(Behavior):
	'''
	Spot Gripper Test
	'''


	def __init__(self):
		super(SpotGripperTestv3SM, self).__init__()
		self.name = 'Spot Gripper Test v3'

		# parameters of this behavior
		self.add_parameter('true', True)
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
		# x:36 y:447, x:617 y:200
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

			# x:1095 y:221
			OperatableStateMachine.add('ArmJointMove',
										ArmMoveJoints(sh0=self.sh0, sh1=self.sh1, el0=self.el0, el1=self.el1, wr0=self.wr0, wr1=self.wr1),
										transitions={'success': 'GripperDemo', 'failure': 'failed'},
										autonomy={'success': Autonomy.Off, 'failure': Autonomy.Off},
										remapping={'robot_command_client': 'robot_command_client', 'robot': 'robot', 'lease': 'lease', 'state_client': 'state_client'})

			# x:1087 y:416
			OperatableStateMachine.add('GripperDemo',
										GripperControl(),
										transitions={'success': 'stow', 'failure': 'failed'},
										autonomy={'success': Autonomy.Off, 'failure': Autonomy.Off},
										remapping={'robot_command_client': 'robot_command_client', 'robot': 'robot', 'lease': 'lease'})

			# x:307 y:390
			OperatableStateMachine.add('PowerOFF',
										Power(on=self.false),
										transitions={'success': 'ReturnLease', 'failure': 'failed'},
										autonomy={'success': Autonomy.Off, 'failure': Autonomy.Off},
										remapping={'robot_command_client': 'robot_command_client', 'robot': 'robot', 'lease': 'lease'})

			# x:566 y:3
			OperatableStateMachine.add('PowerON',
										Power(on=self.true),
										transitions={'success': 'Stand', 'failure': 'failed'},
										autonomy={'success': Autonomy.Off, 'failure': Autonomy.Off},
										remapping={'robot_command_client': 'robot_command_client', 'robot': 'robot', 'lease': 'lease'})

			# x:96 y:300
			OperatableStateMachine.add('ReturnLease',
										ReturnLease(),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'lease_obj': 'lease_obj'})

			# x:572 y:485
			OperatableStateMachine.add('Sit',
										StandSit(stand=self.false),
										transitions={'success': 'PowerOFF', 'failure': 'failed'},
										autonomy={'success': Autonomy.Off, 'failure': Autonomy.Off},
										remapping={'robot_command_client': 'robot_command_client', 'robot': 'robot', 'lease': 'lease'})

			# x:839 y:14
			OperatableStateMachine.add('Stand',
										StandSit(stand=self.true),
										transitions={'success': 'unstow', 'failure': 'failed'},
										autonomy={'success': Autonomy.Off, 'failure': Autonomy.Off},
										remapping={'robot_command_client': 'robot_command_client', 'robot': 'robot', 'lease': 'lease'})

			# x:819 y:459
			OperatableStateMachine.add('stow',
										ArmStowUnstow(stow=self.true),
										transitions={'success': 'Sit', 'failure': 'failed'},
										autonomy={'success': Autonomy.Off, 'failure': Autonomy.Off},
										remapping={'robot_command_client': 'robot_command_client', 'robot': 'robot', 'lease': 'lease'})

			# x:1070 y:81
			OperatableStateMachine.add('unstow',
										ArmStowUnstow(stow=self.false),
										transitions={'success': 'ArmJointMove', 'failure': 'failed'},
										autonomy={'success': Autonomy.Off, 'failure': Autonomy.Off},
										remapping={'robot_command_client': 'robot_command_client', 'robot': 'robot', 'lease': 'lease'})

			# x:323 y:54
			OperatableStateMachine.add('AcquireLease',
										AcquireLease(),
										transitions={'continue': 'PowerON', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'lease_obj': 'lease_obj'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
