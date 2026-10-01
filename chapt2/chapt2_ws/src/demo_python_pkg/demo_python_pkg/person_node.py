import rclpy
from rclpy.node import Node

class PersonNode(Node):
    def __init__(self,name:str,age:int):
        print("这个是初始化__init__的方法")
        super().__init__(name)
        self.name=name
        self.age=age

    def eat(self,food:str):
        print(f"{self.name}今年{self.age}，正在吃{food}")

def main():
    rclpy.init()
    node=PersonNode("zhangsan",18)
    node.eat("鱼香肉丝")
    node.get_logger().info("张三来了")
    rclpy.spin(node)
    node.get_logger().info("张三走了")

    rclpy.shutdown()

if __name__=="__main__":
    main()
        