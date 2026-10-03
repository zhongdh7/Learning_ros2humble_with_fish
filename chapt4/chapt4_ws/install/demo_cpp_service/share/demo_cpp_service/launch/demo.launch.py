import launch
import launch_ros

def generate_launch_description():
    #这个函数名字是写死的，产生launch描述
    action_node_turtlesim_node=launch_ros.actions.Node(
        package="turtlesim",#功能包的名字
        executable="turtlesim_node",#可执行文件的名字
        output="screen"#日志打印的位置
    )

    action_node_partol_client=launch_ros.actions.Node(
        package="demo_cpp_service",
        executable="patrol_client",
        output="both"
    )

    action_node_turtle_control=launch_ros.actions.Node(
        package="demo_cpp_service",
        executable="turtle_control",
        output="log"
    )
    return launch.LaunchDescription([
        #action动作
        action_node_turtlesim_node,
        action_node_partol_client,
        action_node_turtle_control
    ])