import launch
import launch.actions
import launch.substitutions
import launch_ros.actions

def generate_launch_description():
    serial = launch_ros.actions.Node(
            package = 'test_controll',
            executable = 'serial',
            output = 'screen',
            )
    web = launch_ros.actions.Node(
            package = 'rosbridge_server',
            executable = 'rosbridge_websocket.py',
            parameters=[{'port': 9092}],
            output = 'screen',
            )
    lidar = launch_ros.actions.Node(
            package = 'urg_node2',
            executable = 'urg_node2.launch.py',
            output = 'screen',
            )
    return launch.LaunchDescription([web,serial,lidar])