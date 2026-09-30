#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

def main():
    rclpy.init() # 初始化工作，准备通信为通信初始化资源

    node=Node(node_name="python_node") #创建一个节点要求传入一个节点的名字

    # 打印日志
    node.get_logger().info("这个是python节点")
    node.get_logger().error("你好python")
    node.get_logger().warn("你好 python !")
    rclpy.spin(node)#运行这个节点，然后阻塞这节点，节点会一直运行
    rclpy.shutdown()# 主动退出会清理的

if __name__=="__main__":
    main()