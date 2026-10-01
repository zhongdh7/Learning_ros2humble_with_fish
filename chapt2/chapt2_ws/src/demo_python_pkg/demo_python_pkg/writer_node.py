import rclpy
from rclpy.node import Node

from demo_python_pkg.person_node import PersonNode


class WriterNode(PersonNode):
    def __init__(self, name, age,book):
        super().__init__(name, age)
        self.book=book

    def writer(self):
        print(f"{self.name} has written the {self.book}")
def main():
    rclpy.init()
    node=WriterNode("writer",89,"ROS")
    node.eat("鱼香肉丝")
    node.writer()
    node.get_logger().info("继承成功")
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
