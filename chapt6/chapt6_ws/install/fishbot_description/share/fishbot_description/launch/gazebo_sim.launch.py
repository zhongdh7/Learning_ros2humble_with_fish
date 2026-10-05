#! python3
import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    #获取默认的urdf路径
    fishbot_urdf=os.path.join(get_package_share_directory("fishbot_description"),"urdf","fishbot","fishbot.urdf.xacro")
    # 声明一个urdf目录的参数
    action_declare_arg_model_path=launch.actions.DeclareLaunchArgument(name="model",
                                                                       default_value=str(fishbot_urdf),
                                                                       description="传入的模型的所在的位置的路径")
    
    default_rviz_config_ros=os.path.join(get_package_share_directory("fishbot_description"),"config","fish_robot.rviz")

    default_gazebo_world_path=os.path.join(get_package_share_directory("fishbot_description"),"world","custom_room.world")



    # 通过文件路径获取内容，并且转换成参数值的对象
    substitution_command_result=launch.substitutions.Command(['xacro ',
                                                             launch.substitutions.LaunchConfiguration("model")])
    
    robot_description_value=launch_ros.parameter_descriptions.ParameterValue(substitution_command_result,
                                                                             value_type=str)


    action_robot_state_publisher=launch_ros.actions.Node(
                            package="robot_state_publisher",executable="robot_state_publisher",
                            parameters=[{"robot_description":robot_description_value}])

    # Gazebo 的 diff drive 插件已经在发布轮子 TF，这里再起一个假的 joint_state_publisher
    # 会让同一个轮子 frame 出现两个父坐标系，RViz 解不出来就会把轮子渲染成白色。
    # joint_state_publisher=launch_ros.actions.Node(package="joint_state_publisher",executable="joint_state_publisher")

    rviz_action=launch_ros.actions.Node(package="rviz2",executable="rviz2",arguments=['-d',default_rviz_config_ros])

    gazebo_launch_action=launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("gazebo_ros"),"launch","gazebo.launch.py")
        ),launch_arguments=[("world", default_gazebo_world_path), ("verbose", "true")]
    )

    action_spawn_robot=launch_ros.actions.Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-topic","/robot_description","-entity","fishbot"]
    )
    return launch.LaunchDescription([
        action_declare_arg_model_path,
        action_robot_state_publisher,
        # joint_state_publisher,
        rviz_action,
        gazebo_launch_action,
        # gzserver 加载 custom_room.world 需要时间，spawn_entity 起太早会撞上
        # Gazebo 内部 “entity to appear in simulation” 超时而退出。这里延迟 8s 错开。
        # 注意：TimerAction 只是按时间错开，不代表 Gazebo 真的就绪（见下方说明）。
        launch.actions.TimerAction(period=3.0, actions=[action_spawn_robot])
    ])
