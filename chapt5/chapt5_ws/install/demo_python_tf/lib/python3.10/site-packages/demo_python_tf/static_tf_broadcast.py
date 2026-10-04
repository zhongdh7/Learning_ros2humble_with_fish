import rclpy
from rclpy.node import Node
from tf2_ros import StaticTransformBroadcaster #静态坐标广播器
from geometry_msgs.msg import TransformStamped #消息接口
from tf_transformations import quaternion_from_euler #从欧拉角转换
import math

class StaticTFBroadcast(Node):
    def __init__(self):
        super().__init__("static_tf_broadcaster")
        self.static_broadcaster_=StaticTransformBroadcaster(self)
        self.publish_static_tf()

    def publish_static_tf(self):
        #发布静态TF从base_link到camera_link之间的坐标关系
        transform=TransformStamped()
        transform.header.frame_id="base_link"
        transform.header.stamp=self.get_clock().now().to_msg()
        transform.child_frame_id="camera_link"

        transform.transform.translation.x=0.5
        transform.transform.translation.y=0.3
        transform.transform.translation.z=0.6

        q=quaternion_from_euler(math.radians(180),0,0)
        transform.transform.rotation.x=q[0]
        transform.transform.rotation.y=q[1]
        transform.transform.rotation.z=q[2]
        transform.transform.rotation.w=q[3]

        self.static_broadcaster_.sendTransform(transform)
        self.get_logger().info(f"发布静态TF：{transform}")

def main():
    rclpy.init()
    node=StaticTFBroadcast()
    rclpy.spin(node)
    rclpy.shutdown()