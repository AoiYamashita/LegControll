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
    rviz = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        #arguments=['-d', './abc.rviz']
        )
    return launch.LaunchDescription([web,serial,rviz])