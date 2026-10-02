import rclpy 
from rclpy.node import Node
from rclpy.parameter import Parameter
from chapt4_interfaces.srv import FaceDetector
from rcl_interfaces.msg import SetParametersResult
import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory
import os
from cv_bridge import CvBridge
import time

class FaceDetectNode(Node):
    def __init__(self):
        super().__init__("face_detect_node")
        
        self.service_=self.create_service(FaceDetector,"face_detect",self.detect_face_callback)
        self.bridge=CvBridge()
        self.declare_parameter("number_of_times_to_unsample",value=1)
        self.declare_parameter("model",value="cnn")
        self.number_of_times_to_unsample=self.get_parameter("number_of_times_to_unsample").value
        self.model=self.get_parameter("model").value
        self.default_image_path=os.path.join(get_package_share_directory("demo_python_service"),
                                             "resource","default.jpg")
        self.get_logger().info("检测服务启动")


        #这个是系统更新parameter的时候调用的回调函数，这边我们在这个里面加入我们自己想要的回调函数内容
        self.add_on_set_parameters_callback(self.parameter_callback)

    def parameter_callback(self,parameters: list[Parameter]):
        for param in parameters:
            self.get_logger().info(f"{param.name}->{param.value}")
            if param.name=="number_of_times_to_unsample":
                self.number_of_times_to_unsample=param.value
            if param.name=="model":
                self.model=param.value
        return SetParametersResult(successful=True)



    def detect_face_callback(self,request: FaceDetector.Request,response: FaceDetector.Response):
        #这里request是请求，response是响应，等会儿需要把response传递回去
        if request.image.data:
            cv_image=self.bridge.imgmsg_to_cv2(request.image)
            self.get_logger().info("加载完成图片，开始识别")
            
        else:
            cv_image=cv2.imread(self.default_image_path)
            self.get_logger().info("传入图像为空使用默认图像")

        #此时cv_image已经是一个opencv格式的了
        start_time=time.time()
        face_locations=face_recognition.face_locations(cv_image,self.number_of_times_to_unsample,self.model)
        end_time=time.time()
        response.use_time=end_time-start_time
        response.number=len(face_locations)#识别的人脸数量
        for top,right,bottom,left in face_locations:
            response.top.append(top)
            response.bottom.append(bottom)
            response.left.append(left)
            response.right.append(right)
        self.get_logger().info(f"检测完成用时{response.use_time}")
        return response

def main():
    rclpy.init()
    node=FaceDetectNode()
    rclpy.spin(node)
    rclpy.shutdown()