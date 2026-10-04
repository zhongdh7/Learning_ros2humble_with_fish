import launch 
import launch_ros

def generate_launch_description():
    action_node_turtle_control=launch_ros.actions.Node(
        package="demo_cpp_service",
        executable="turtle_control",
        output="log"
    )
    action_node_turtlesim=launch_ros.actions.Node(
        package="turtlesim",
        executable="turtlesim_node",
        output="screen"
    )
    action_node_patrol=launch_ros.actions.Node(
        package="demo_cpp_service",
        executable="patrol_client",
        output="both"
    )


    return launch.LaunchDescription([
        action_node_turtle_control,
        action_node_turtlesim,
        action_node_patrol
    ])