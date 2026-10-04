import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    #获取默认的urdf路径
    first_robot_urdf=os.path.join(get_package_share_directory("fishbot_description"),"urdf","first_robot.urdf")
    # 声明一个urdf目录的参数
    action_declare_arg_model_path=launch.actions.DeclareLaunchArgument(name="model",default_value=str(first_robot_urdf),description="传入的模型的所在的位置的路径")

    # 通过文件路径获取内容，并且转换成参数值的对象
    substitution_command_result=launch.substitutions.Command('cat',launch.substitutions.LaunchConfiguration("model"))
    robot_description_value=aunch_ros.parameter_descriptions.ParameterValue(substitution_command_result,value_type=str)

    action_robot_state_publisher=launch_ros.actions.Node(
                            package="robot_state_publisher",executable="robot_state_publisher",
                            parameters=[{"robot_description":robot_description_value}])


    return launch.LaunchDescription([
        action_declare_arg_model_path,
        action_robot_state_publisher

    ])