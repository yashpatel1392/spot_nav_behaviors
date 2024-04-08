#!/usr/bin/env python
import rospy

from flexbe_core import EventState, Logger
from bosdyn.api.graph_nav import map_pb2
from bosdyn.client.graph_nav import GraphNavClient



class UploadMap(EventState):
    '''
    This state is used for verifying if the map is already present, if not it would upload it.
    If should_upload is set to true, it would upload the map regardless of whether a map is there or not.

    -- path_to_graph 	    String 	        path to the map, which would be used for navigation.
    -- should_upload        boolean         true would upload the map to robot, false wouldn't          

    ># graph_nav_client         		GraphNavClient, used for navigation

    #> None

    '''

    def __init__(self, path_to_graph, should_upload):
        # Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
        super(UploadMap, self).__init__(outcomes = ['success', 'failed'],
                                        input_keys = ['graph_nav_client'])
        self._map = None
        self._upload_filepath = path_to_graph
        self._current_wp_snapshots = dict()
        self._current_edge_snapshots = dict()
        self._should_upload = should_upload


    def execute(self, userdata):
        # This method is called periodically while the state is active.
        return 'success'
        

    def on_enter(self, userdata):
        # This method is called when the state becomes active, i.e. a transition from another state to this one is taken.
        # It is primarily used to start actions which are associated with this state.
                
        current_graph = userdata.graph_nav_client.download_graph()
        
        if len(current_graph.waypoints) <= 0 or self._should_upload:
            if len(current_graph.waypoints) <= 0:
                print("no graph is present, uploading the given one to the spot.................\n")
            
            print("clearing previous graph if present.............")
            userdata.graph_nav_client.clear_graph()
            
            print("Uploading the following graph: ")                
            self._upload_filepath = "../" + self._upload_filepath
            print(self._upload_filepath)
            
            with open(self._upload_filepath + "/graph", "rb") as graph_file:
                graph_data = graph_file.read()
                self._map = map_pb2.Graph()
                self._map.ParseFromString(graph_data)
                print("Loaded graph has {} waypoints and {} edges".format(len(self._map.waypoints), len(self._map.edges)))
                
            for waypoint in self._map.waypoints:
                with open(self._upload_filepath + "/waypoint_snapshots/{}".format(waypoint.snapshot_id), "rb") as snapshot_file:
                    wp_snapshot = map_pb2.WaypointSnapshot()
                    wp_snapshot.ParseFromString(snapshot_file.read())
                    self._current_wp_snapshots[wp_snapshot.id] = wp_snapshot
                    
            for edge in self._map.edges:
                if len(edge.snapshot_id) == 0:
                    continue
                
                with open(self._upload_filepath + "/edge_snapshots/{}".format(edge.snapshot_id), "rb") as snapshot_file:
                    edge_snapshot = map_pb2.EdgeSnapshot()
                    edge_snapshot.ParseFromString(snapshot_file.read())
                    self._current_edge_snapshots[edge_snapshot.id] = edge_snapshot
            
            print('Uploading the graph and snapshots to the robot...')            
            true_if_empty = not len(self._map.anchoring.anchors)
            response = userdata.graph_nav_client.upload_graph(graph=self._map, generate_new_anchoring=true_if_empty)
            
            for snapshot_id in response.unknown_waypoint_snapshot_ids:
                wp_snapshot = self._current_wp_snapshots[snapshot_id]
                userdata.graph_nav_client.upload_waypoint_snapshot(wp_snapshot)
                print(f'Uploaded {wp_snapshot.id}')

                
            for snapshot_id in response.unknown_edge_snapshot_ids:
                edge_snapshot = self._current_edge_snapshots[snapshot_id]
                userdata.graph_nav_client.upload_waypoint_snapshot(edge_snapshot) 
                print(f'Uploaded {edge_snapshot.id}')
        else:
            print("graph already present...........\n")
            print("number of waypoints are: ", len(current_graph.waypoints))
        


    def on_exit(self, userdata):
        # This method is called when an outcome is returned and another state gets active.
        # It can be used to stop possibly running processes started by on_enter.

        pass # Nothing to do in this example.


    def on_start(self):
        # This method is called when the behavior is started.
        # If possible, it is generally better to initialize used resources in the constructor
        # because if anything failed, the behavior would not even be started.

        pass


    def on_stop(self):
        # This method is called whenever the behavior stops execution, also if it is cancelled.
        # Use this event to clean up things like claimed resources.

        pass # Nothing to do in this example.
        
