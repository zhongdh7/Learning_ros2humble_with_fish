#动态坐标变换发布到/tf话题下面
import rclpy
from rclpy.node import Node
from tf2_ros import TransformListener,Buffer #坐标监听
from tf_transformations import euler_from_quaternion #从四元素转换

# import math

class TFBroadcast(Node):
    def __init__(self):
        super().__init__("tf_listener")
        self.buffer_=Buffer()
        self.listener_=TransformListener(self.buffer_,self)
        self.timer_=self.create_timer(1,self.get_transform)


    def get_transform(self):
        try:
            result=self.buffer_.lookup_transform("base_link","bottle_link",
                                                rclpy.time.Time(seconds=0),rclpy.time.Duration(seconds=1.0))#这两个是指frame_id和child_id
            transform_=result.transform
            self.get_logger().info(f"平移:{transform_.translation},旋转{euler_from_quaternion([transform_.rotation.x,transform_.rotation.y,transform_.rotation.z,transform_.rotation.w])}")
        except Exception as e:
            self.get_logger().warn(f"{str(e)}")
            
     
def main():
    rclpy.init()
    node=TFBroadcast()
    rclpy.spin(node)
    rclpy.shutdown()