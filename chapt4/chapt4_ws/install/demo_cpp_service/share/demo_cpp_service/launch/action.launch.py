import launch 
import launch_ros

def generate_launch_description():

    #先声明launch参数，然后把launch参数传入节点
    #注意：default_value 必须是字符串，写 150（int）会报 'int' object is not iterable
    action_declare_arg_bg=launch.actions.DeclareLaunchArgument("launch_arg_bg",default_value="255",description="修改小海龟的节点的背景g")

    #注意:这里必须写 "3.0" 而不是 "3"。launch 会把参数写成 YAML 文件传给节点,
    #YAML 会做类型推断:"3.0"->double,"3"->integer,而节点声明的 max_speed 是 double,
    #类型不匹配节点会抛 InvalidParameterTypeException 直接崩掉。
    action_declare_arg_max_speed=launch.actions.DeclareLaunchArgument("launch_arg_max_speed",default_value="3.0",description="小乌龟运动的最大速度")
    action_node_turtlesim=launch_ros.actions.Node(
        package="turtlesim",
        executable="turtlesim_node",
        #用 LaunchConfiguration 拿到 launch 参数，再用 ParameterValue(value_type=int) 转成 int
        #可以在Node里面的parameters里面传入参数这个修改的是该节点修改的参数
        parameters=[{"background_r":255,
                     "background_g":launch.substitutions.LaunchConfiguration("launch_arg_bg")}],#launch替换
        #Node 没有 log 参数，输出位置用 output
        output="screen")
    action_node_partol_client=launch_ros.actions.Node(
        package="demo_cpp_service",
        executable="patrol_client",
        output="both"
    )

    action_node_turtle_control=launch_ros.actions.Node(
        package="demo_cpp_service",
        executable="turtle_control",
        output="log",
        parameters=[{"max_speed":launch.substitutions.LaunchConfiguration("launch_arg_max_speed")}]
    )
    return launch.LaunchDescription([
        action_declare_arg_bg,
        action_declare_arg_max_speed,
        action_node_turtlesim,
        action_node_turtle_control,
        action_node_partol_client,
    ])