
#!/usr/bin/env python

from flexbe_core import EventState
from flexbe_core.proxy import ProxySubscriberCached, ProxyPublisher
from std_msgs.msg import String
import time, json

class PauseState(EventState):
    """
    This state continues running until a "continue" message is published to the 
    topic, whose name is passed as an input parameter. This state is also similar
    to the get_arm_data.py as this state can also be used to get each of the arm joint values.

    -- topic            string          name to topic, which has to be subscibed.

	># state_client             		StateClient

    #> None


    """

    def __init__(self, topic):
        # Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.

        super(PauseState, self).__init__(outcomes=['success'],
                                         input_keys = ['state_client'])
        self._topic = topic
        self._sub = ProxySubscriberCached({self._topic: String})
        self._pub = ProxyPublisher({self._topic: String})


    def parse_arm_joints_data(self, data):
        splitted_data = data.strip().split('\n')
        counter = 0
        joint_values = {}
        
        for i in range(len(splitted_data)):
            if counter >= 6: # no need to iterate the list after all 6 joint values have been recorded
                break
            
            if splitted_data[i].strip().startswith('joint_states'):
                if (i+3 < len(splitted_data)):
                    joint_name = splitted_data[i+1].strip().split(':')[1].strip().replace('"', '')

                    if joint_name == 'arm0.hr0' or joint_name == 'arm0.f1x':
                        continue
                    
                    if joint_name.startswith('arm'):
                        arm_joint_name = joint_name.split('.')[1]
                        arm_joint_position = float(splitted_data[i+3].strip().split(':')[1].strip())

                        print(arm_joint_name, ": ", arm_joint_position)
                        
                        joint_values[arm_joint_name] = arm_joint_position
                        
                        counter += 1
                    
        # returns a dict where key is the joint name while the values are the corresponding values
        return joint_values

    def execute(self, userdata):
        # This method is called periodically while the state is active.
        # Main purpose is to check state conditions and trigger a corresponding outcome.
        # If no outcome is returned, the state will stay active.

        print("\n\n**************************************************************")
        
        if self._topic:
            if self._sub.has_msg(self._topic):
                self._data = self._sub.get_last_msg(self._topic)
                if self._data.data == "continue":
                    return 'success'
            else:
                user_input = input("Hit enter to print current arm position or type save to current arm position:  ")
                print()
                
                state_data = userdata.state_client.get_robot_state()
                arm_joint_data = self.parse_arm_joints_data(str(state_data))
                                     
                if user_input == 'save':
                    position_name = input("For saving the arm position, provide a unique name: ")
                    
                    try:
                        with open('../spot-arm-positions/arm_data.json', 'r') as file:
                            current_data = json.load(file)
                    except (FileNotFoundError, json.decoder.JSONDecodeError):
                        current_data = {}
                 
                    if position_name in current_data:
                        print("An arm position with this name already exists: ")
                        print(current_data[position_name])
                        print()
                        
                        user_input = input("Type r to rename the current position, or Press Enter to update the existing position:  ")
                        if user_input == 'r':
                            position_name = input("Enter the new unique name for this arm position:  ")
                    
                
                    updated_data = {position_name: arm_joint_data}
                    current_data.update(updated_data)
                
                    with open('../spot-arm-positions/arm_data.json', 'w') as file:
                        json.dump(current_data, file, indent=4)
                

    def on_enter(self, userdata):
        # This method is called when the state becomes active, i.e. a transition from another state to this one is taken.
        pass # Nothing to do here


    def on_exit(self, userdata):
        # This method is called when an outcome is returned and another state gets active.

        pause_msg = String()
        pause_msg.data = "pause"
        self._pub.publish(self._topic, pause_msg)
        pass


    def on_stop(self):
        # This method is called whenever the behavior stops execution, also if it is cancelled.

        pause_msg = String()
        pause_msg.data = "pause"
        self._pub.publish(self._topic, pause_msg)
        pass
