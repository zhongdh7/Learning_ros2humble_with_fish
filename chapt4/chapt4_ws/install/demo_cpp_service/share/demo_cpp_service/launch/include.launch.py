import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    mutisim_launch_path=os.path.join(get_package_share_directory("turtlesim"),"launch","multisim.launch.py")
    action_include_launch=launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            mutisim_launch_path
        )#这个只能包含Python的launch文件
    )#传入一个完整的launch的路径

    action_launch_arg_rqt=launch.actions.DeclareLaunchArgument("startup_rqt",default_value="False")

    startup_rqt=launch.substitutions.LaunchConfiguration("startup_rqt")

    action_log_info=launch.actions.LogInfo(msg=str(mutisim_launch_path))

    action_topic_list=launch.actions.ExecuteProcess(
        cmd=["ros2","topic","list"]
    )

    action_rqt=launch.actions.ExecuteProcess(
        condition=launch.conditions.IfCondition(startup_rqt),
        cmd=["rqt"]
    )

    #把多个action放在一个组
    action_group=launch.actions.GroupAction([
        # 添加定时发布launch启动时间
        launch.actions.TimerAction(period=2.0,actions=[action_include_launch]),
        launch.actions.TimerAction(period=4.0,actions=[action_topic_list,action_rqt])
    ])

    return launch.LaunchDescription([
        action_log_info,
        action_launch_arg_rqt,
        action_group
    ])