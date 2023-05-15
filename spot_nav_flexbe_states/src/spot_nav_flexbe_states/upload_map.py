#!/usr/bin/env python
import rospy

from flexbe_core import EventState, Logger
from bosdyn.api.graph_nav import map_pb2
from bosdyn.client.graph_nav import GraphNavClient



class UploadMap(EventState):
    '''
    This state does not require a lease

    -- target_time 	float 	Time which needs to have passed since the behavior started.

    <= continue 			Given time has passed.
    <= failed 				Example for a failure outcome.

    '''

    def __init__(self, path_to_graph):
        # Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
        super(UploadMap, self).__init__(outcomes = ['success', 'failed'])
        self._graph_nav_client = self._robot.ensure_client(GraphNavClient.default_service_name)
        self._map = None
        self._upload_filepath = path_to_graph
        self._current_wp_snapshots = dict()
        self._current_edge_snapshots = dict()



    def execute(self, userdata):
        # This method is called periodically while the state is active.

        # find some way to check if the map already exists
        return 'success'
        

    def on_enter(self, userdata):
        # This method is called when the state becomes active, i.e. a transition from another state to this one is taken.
        # It is primarily used to start actions which are associated with this state.
        with open(self._upload_filepath + "/graph", "rb") as graph_file:
            graph_data = graph_file.read()
            self._map = map_pb2.Graph()
            self._map.ParseFromString(graph_data)
            # print("Loaded graph has {} waypoints and {} edges".format(len(self._current_graph.waypoints), len(self._current_graph.edges)))
            
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
                
        true_if_empty = not len(self._map.anchoring.anchors)
        response = self._graph_nav_client.upload_graph(graph=self._map, generate_new_anchoring=true_if_empty)
        
        for snapshot_id in response.unknown_waypoint_snapshot_ids:
            wp_snapshot = self._current_wp_snapshots[snapshot_id]
            self._graph_nav_client.upload_waypoint_snapshot(wp_snapshot)
            
        for snapshot_id in response.unknown_waypoint_snapshot_ids:
            edge_snapshot = self._current_edge_snapshots[snapshot_id]
            self._graph_nav_client.upload_waypoint_snapshot(edge_snapshot) 
        


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
        
