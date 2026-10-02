import rclpy 
from rclpy.node import Node
from chapt4_interfaces.srv import FaceDetector
import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory
import os
from cv_bridge import CvBridge
import time


class FaceDetectorClientNode(Node):
    def __init__(self):
        super().__init__("face_detect_client_node")
        self.bridge=CvBridge()
        self.default_image_path=os.path.join(get_package_share_directory("demo_python_service"),
                                                     "resource","test1.jpg")
        self.client=self.create_client(FaceDetector,"face_detect")
        self.get_logger().info("人脸检测客户端启动")
        self.image=cv2.imread(self.default_image_path)

    def send_request(self):
        #先判断服务端是否在线
        while self.client.wait_for_service(timeout_sec=1) is False:#等待一秒时间如果没有上线返回False，1s内上线就返回True
            self.get_logger().info("等待服务上线")
        request=FaceDetector.Request()
        request.image=self.bridge.cv2_to_imgmsg(self.image)

        future=self.client.call_async(request)#发送请求会异步的返回结果
        #发送消息后会立马返回future刚开始的future里面不会包含response,需要等待服务端处理完成才会把结果放到future中

        # while not future.done():
        #     self.get_logger().info("等待服务完成")
        #     time.sleep(1)#这个会导致这个线程休眠导致哪怕有服务端发送来的消息也不会接收到
        rclpy.spin_until_future_complete(self,future)#等待这个future完成
        response: FaceDetector.Response=future.result()
        self.get_logger().info(f"接收到响应,一共有{response.number}张人脸，共耗时{response.use_time}")
        self.show_response(response)

    def show_response(self,response: FaceDetector.Response):
        for i in range(response.number):
            top=response.top[i]
            bottom=response.bottom[i]
            right=response.right[i]
            left=response.left[i]
            cv2.rectangle(self.image,[left,top],[right,bottom],[0,255,0],4)
        cv2.imshow("Face Detect Result",self.image)
        cv2.waitKey(0)

def main():
    rclpy.init()
    node=FaceDetectorClientNode()
    node.send_request()
    # rclpy.spin(node)
    rclpy.shutdown()