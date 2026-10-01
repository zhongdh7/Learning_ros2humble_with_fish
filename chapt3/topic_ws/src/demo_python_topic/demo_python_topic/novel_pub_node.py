import rclpy
from rclpy.node import Node
import requests
from example_interfaces.msg import String
from queue import Queue


class NovelPubNode(Node):
    

    def __init__(self,node_name):
        super().__init__(node_name)
        self.get_logger().info(f"{node_name},启动")
        self.novel_queue_=Queue() #创建队列
        self.novel_publisher_=self.create_publisher(msg_type=String,topic="novel",qos_profile=10)#最后一个是队列的大小
        self.create_timer(timer_period_sec=5,callback=self.timer_callback)#这个地方的callback函数是隔一段时间会回调的函数


    def timer_callback(self):
        if self.novel_queue_.qsize()>0:
            line=self.novel_queue_.get()
            msg=String()
            msg.data=line
            self.novel_publisher_.publish(msg)
            self.get_logger().info(f"发布了{msg}")
            
    

    def download(self,url):
        response=requests.get(url)
        response.encoding="utf-8"
        self.get_logger().info(f"下载{url},{len(response.text)},type:{type(response.text)}")
        for line in response.text.splitlines():
            self.novel_queue_.put(line)


def main():
    rclpy.init()

    novel_pub_node=NovelPubNode("novel_pub_node")
    novel_pub_node.download("http://0.0.0.0:8000/novel1.txt")
    rclpy.spin(novel_pub_node)#会自动调用回调函数

    rclpy.shutdown()