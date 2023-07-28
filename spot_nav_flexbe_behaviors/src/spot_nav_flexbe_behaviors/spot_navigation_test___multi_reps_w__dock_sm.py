#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from spot_nav_flexbe_states.counter import CounterState
from spot_nav_flexbe_states.dock import Dock
from spot_nav_flexbe_states.localize import Localize
from spot_nav_flexbe_states.navigate import NavigateTo
from spot_nav_flexbe_states.return_lease import ReturnLease
from spot_nav_flexbe_states.setup_spot import SetupSpot
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon July 20 2023
@author: Yash P
'''
class SpotNavigationTestMultiRepswDockSM(Behavior):
	'''
	Spot Navigation Test Dock
	'''


	def __init__(self):
		super(SpotNavigationTestMultiRepswDockSM, self).__init__()
		self.name = 'Spot Navigation Test - Multi Reps w/ Dock'

		# parameters of this behavior
		self.add_parameter('init_waypoint_id', 'healed-bobcat-T1nIxvFP55eD3JyB4K4R2A==')
		self.add_parameter('goal_waypoint_id', 'famous-seal-FL7nlT7iMBqWH0dVVFpFeg==')
		self.add_parameter('true', True)
		self.add_parameter('false', False)
		self.add_parameter('reps', 1)
		self.add_parameter('dock_id', 520)

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:752 y:399, x:441 y:272
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.num_reps_IN = self.reps

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:58 y:425, x:548 y:183
		_sm_container_0 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['state_client', 'graph_nav_client', 'lease', 'power_client', 'robot_command_client', 'num_reps_IN'])

		with _sm_container_0:
			# x:153 y:74
			OperatableStateMachine.add('CounterCheck',
										CounterState(decrement=self.false),
										transitions={'success': 'NavigateToDest', 'failed': 'failed', 'end': 'finished'},
										autonomy={'success': Autonomy.Off, 'failed': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'num_reps': 'num_reps_IN', 'num_reps_remaining': 'num_reps_OUT'})

			# x:478 y:357
			OperatableStateMachine.add('DecrementCounter',
										CounterState(decrement=self.true),
										transitions={'success': 'CounterCheck', 'failed': 'failed', 'end': 'finished'},
										autonomy={'success': Autonomy.Off, 'failed': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'num_reps': 'num_reps_OUT', 'num_reps_remaining': 'num_reps_IN'})

			# x:501 y:40
			OperatableStateMachine.add('NavigateToDest',
										NavigateTo(destination_waypoint=self.goal_waypoint_id),
										transitions={'continue': 'NavigateToStartPos', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client', 'lease': 'lease', 'power_client': 'power_client', 'robot_command_client': 'robot_command_client'})

			# x:842 y:205
			OperatableStateMachine.add('NavigateToStartPos',
										NavigateTo(destination_waypoint=self.init_waypoint_id),
										transitions={'continue': 'DecrementCounter', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client', 'lease': 'lease', 'power_client': 'power_client', 'robot_command_client': 'robot_command_client'})



		with _state_machine:
			# x:86 y:55
			OperatableStateMachine.add('SetupSpot',
										SetupSpot(),
										transitions={'continue': 'Undock', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client', 'lease': 'lease', 'power_client': 'power_client', 'robot_command_client': 'robot_command_client', 'license_client': 'license_client', 'robot': 'robot', 'lease_obj': 'lease_obj'})

			# x:1144 y:141
			OperatableStateMachine.add('Dock',
										Dock(should_dock=self.true, dock_id=self.dock_id),
										transitions={'continue': 'ReturnLease', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'robot_command_client': 'robot_command_client', 'license_client': 'license_client', 'robot': 'robot'})

			# x:710 y:6
			OperatableStateMachine.add('Localize',
										Localize(initial_waypoint=self.init_waypoint_id),
										transitions={'continue': 'Container', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client'})

			# x:924 y:268
			OperatableStateMachine.add('ReturnLease',
										ReturnLease(),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'lease_obj': 'lease_obj'})

			# x:319 y:20
			OperatableStateMachine.add('Undock',
										Dock(should_dock=self.false, dock_id=self.dock_id),
										transitions={'continue': 'Localize', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'lease': 'lease', 'robot_command_client': 'robot_command_client', 'license_client': 'license_client', 'robot': 'robot'})

			# x:960 y:27
			OperatableStateMachine.add('Container',
										_sm_container_0,
										transitions={'finished': 'Dock', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'state_client': 'state_client', 'graph_nav_client': 'graph_nav_client', 'lease': 'lease', 'power_client': 'power_client', 'robot_command_client': 'robot_command_client', 'num_reps_IN': 'num_reps_IN'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
