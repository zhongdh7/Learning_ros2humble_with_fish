import os

import launch
import launch_ros
from ament_index_python import get_package_share_directory
def generate_launch_description():
    #包含其他launch
    mutisim_launch_path=os.path.join(
        get_package_share_directory("turtlesim"),"launch","multisim.launch.py"
    )

    action_include_launch=launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            mutisim_launch_path
        )
    )

    action_log_info=launch.actions.LogInfo(msg=mutisim_launch_path)

    #执行一个命令行
    action_topic_list=launch.actions.ExecuteProcess(
        cmd=["ros2","topic","list"]
    )

    action_group=launch.actions.GroupAction([
        launch.actions.TimerAction(period=2.0,actions=[action_include_launch]),
        launch.actions.TimerAction(period=4.0,actions=[action_topic_list])
    ])

    return launch.LaunchDescription([
        action_log_info,
        action_group
    ])