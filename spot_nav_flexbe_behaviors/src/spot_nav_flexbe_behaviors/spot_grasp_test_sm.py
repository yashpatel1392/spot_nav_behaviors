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
from spot_nav_flexbe_states.arm_move_joints import ArmMoveJoints
from spot_nav_flexbe_states.arm_stow_unstow import ArmStowUnstow
from spot_nav_flexbe_states.capture_image import CaptureImage
from spot_nav_flexbe_states.grasp import Grasp
from spot_nav_flexbe_states.gripper_control import GripperControl
from spot_nav_flexbe_states.power import Power
from spot_nav_flexbe_states.process import ProcessImageGrasp
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
class SpotGraspTestSM(Behavior):
	'''
	Spot Grasp Test
	'''


	def __init__(self):
		super(SpotGraspTestSM, self).__init__()
		self.name = 'Spot Grasp Test'

		# parameters of this behavior
		self.add_parameter('true', True)
		self.add_parameter('false', False)
		self.add_parameter('sh0', '0.0692')
		self.add_parameter('sh1', '-1.882')
		self.add_parameter('el0', '1.652')
		self.add_parameter('el1', '-0.0691')
		self.add_parameter('wr0', '1.622')
		self.add_parameter('wr1', '1.550')
		self.add_parameter('path', '../spot_images')
		self.add_parameter('image_source', 'frontleft_fisheye_image')
		self.add_parameter('wait_time', 5)

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:27 y:309, x:617 y:200
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:80 y:100
			OperatableStateMachine.add('Setup',
										SetupSpot(),
										transitions={'continue': 'AcquireLease', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client', 'lease': 'lease', 'power_client': 'power_client', 'robot_command_client': 'robot_command_client', 'license_client': 'license_client', 'robot': 'robot', 'image_client': 'image_client', 'manipulation_api_client': 'manipulation_api_client'})

			# x:956 y:548
			OperatableStateMachine.add('ArmJointMove',
										ArmMoveJoints(sh0=self.sh0, sh1=self.sh1, el0=self.el0, el1=self.el1, wr0=self.wr0, wr1=self.wr1),
										transitions={'success': 'GripperDemo', 'failure': 'failed'},
										autonomy={'success': Autonomy.Off, 'failure': Autonomy.Off},
										remapping={'robot_command_client': 'robot_command_client', 'robot': 'robot', 'lease': 'lease', 'state_client': 'state_client'})

			# x:1104 y:17
			OperatableStateMachine.add('CaptureImage',
										CaptureImage(path=self.path, image_source=self.image_source),
										transitions={'continue': 'Process', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'image_client': 'image_client', 'image_response': 'image_response'})

			# x:1167 y:391
			OperatableStateMachine.add('Grasp',
										Grasp(),
										transitions={'success': 'Wait5Seconds', 'failure': 'failed'},
										autonomy={'success': Autonomy.Off, 'failure': Autonomy.Off},
										remapping={'manipulation_api_client': 'manipulation_api_client', 'robot_command_client': 'robot_command_client', 'robot': 'robot', 'lease': 'lease', 'image': 'image', 'click_x': 'click_x', 'click_y': 'click_y'})

			# x:732 y:585
			OperatableStateMachine.add('GripperDemo',
										GripperControl(),
										transitions={'success': 'stow', 'failure': 'failed'},
										autonomy={'success': Autonomy.Off, 'failure': Autonomy.Off},
										remapping={'robot_command_client': 'robot_command_client', 'robot': 'robot', 'lease': 'lease'})

			# x:146 y:362
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

			# x:1159 y:214
			OperatableStateMachine.add('Process',
										ProcessImageGrasp(),
										transitions={'success': 'Grasp', 'failure': 'failed'},
										autonomy={'success': Autonomy.Off, 'failure': Autonomy.Off},
										remapping={'image_response': 'image_response', 'click_x': 'click_x', 'click_y': 'click_y', 'image': 'image'})

			# x:123 y:226
			OperatableStateMachine.add('ReturnLease',
										ReturnLease(),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'lease_obj': 'lease_obj'})

			# x:187 y:537
			OperatableStateMachine.add('Sit',
										StandSit(stand=self.false),
										transitions={'success': 'PowerOFF', 'failure': 'failed'},
										autonomy={'success': Autonomy.Off, 'failure': Autonomy.Off},
										remapping={'robot_command_client': 'robot_command_client', 'robot': 'robot', 'lease': 'lease'})

			# x:837 y:3
			OperatableStateMachine.add('Stand',
										StandSit(stand=self.true),
										transitions={'success': 'CaptureImage', 'failure': 'failed'},
										autonomy={'success': Autonomy.Off, 'failure': Autonomy.Off},
										remapping={'robot_command_client': 'robot_command_client', 'robot': 'robot', 'lease': 'lease'})

			# x:1171 y:499
			OperatableStateMachine.add('Wait5Seconds',
										WaitState(wait_time=self.wait_time),
										transitions={'done': 'ArmJointMove'},
										autonomy={'done': Autonomy.Off})

			# x:494 y:579
			OperatableStateMachine.add('stow',
										ArmStowUnstow(stow=self.true),
										transitions={'success': 'Sit', 'failure': 'failed'},
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
