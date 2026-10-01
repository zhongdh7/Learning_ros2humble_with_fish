import espeakng
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from queue import Queue
import threading
import time

class NovelSubNode(Node):
    def __init__(self,node_name):
        super().__init__(node_name)
        self.get_logger().info(f"{node_name},启动")
        self.novel_queue_=Queue() 
        self.novel_sub_=self.create_subscription(msg_type=String,qos_profile=10,topic="novel",callback=self.novel_callback)
        #这个最后的回调函数是指处理接收到的消息的函数,一旦接收到消息就回调这个函数，也是回调函数的一个

        self.speech_thread_=threading.Thread(target=self.speak_thread)#创建一个阅读的线程和这个ros节点的线程分开执行
        self.speech_thread_.start()#启动这个线程

    def novel_callback(self,msg: String):
        self.novel_queue_.put(msg.data)

    def speak_thread(self):
        speaker=espeakng.Speaker()
        speaker.voice='zh'

        while rclpy.ok():#只要这个节点没有shutdown那么就返回True
            if self.novel_queue_.qsize()>0:
                text=self.novel_queue_.get()
                self.get_logger().info(f"收到数据:{text}")
                speaker.say(text)
                speaker.wait()#等他说完
            else:
                # 避免CPU功耗太高
                time.sleep(1)

def main():
    rclpy.init()
    node=NovelSubNode("novel_sub")
    rclpy.spin(node)
    rclpy.shutdown()