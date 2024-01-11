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
from spot_nav_flexbe_states.capture_image import CaptureImage
from spot_nav_flexbe_states.power import Power
from spot_nav_flexbe_states.return_lease import ReturnLease
from spot_nav_flexbe_states.setup_spot import SetupSpot
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Jan 11 2024
@author: Yash P
'''
class ProcessImagev2SM(Behavior):
	'''
	Process Image
	'''


	def __init__(self):
		super(ProcessImagev2SM, self).__init__()
		self.name = 'Process Image v2'

		# parameters of this behavior
		self.add_parameter('true', True)
		self.add_parameter('false', False)
		self.add_parameter('path', '../spot_images')
		self.add_parameter('image_source', 'frontleft_fisheye_image')

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:100 y:471, x:518 y:234
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:51 y:175
			OperatableStateMachine.add('Setup',
										SetupSpot(),
										transitions={'continue': 'AcquireLease', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client', 'lease': 'lease', 'power_client': 'power_client', 'robot_command_client': 'robot_command_client', 'license_client': 'license_client', 'robot': 'robot', 'image_client': 'image_client'})

			# x:834 y:117
			OperatableStateMachine.add('CaptureImage',
										CaptureImage(path=self.path, image_source=self.image_source),
										transitions={'continue': 'PowerOFF', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'image_client': 'image_client', 'image_response': 'image_response'})

			# x:504 y:413
			OperatableStateMachine.add('PowerOFF',
										Power(on=self.false),
										transitions={'success': 'ReturnLease', 'failure': 'failed'},
										autonomy={'success': Autonomy.Off, 'failure': Autonomy.Off},
										remapping={'robot_command_client': 'robot_command_client', 'robot': 'robot', 'lease': 'lease'})

			# x:524 y:13
			OperatableStateMachine.add('PowerON',
										Power(on=self.true),
										transitions={'success': 'CaptureImage', 'failure': 'failed'},
										autonomy={'success': Autonomy.Off, 'failure': Autonomy.Off},
										remapping={'robot_command_client': 'robot_command_client', 'robot': 'robot', 'lease': 'lease'})

			# x:199 y:381
			OperatableStateMachine.add('ReturnLease',
										ReturnLease(),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'lease_obj': 'lease_obj'})

			# x:291 y:74
			OperatableStateMachine.add('AcquireLease',
										AcquireLease(),
										transitions={'continue': 'PowerON', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'lease_obj': 'lease_obj'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
