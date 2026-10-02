import os

import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory # 获取功能包share目录的绝对路径

def main():
    default_image_path=os.path.join(
        get_package_share_directory("demo_python_service"),"resource","default.jpg")
    print(default_image_path)

    #使用opencv加载图片
    image=cv2.imread(default_image_path)
    if image is None:
        print(f"无法读取图片: {default_image_path}")
        return
    face_location=face_recognition.face_locations(image,number_of_times_to_upsample=1,model="cnn")
    # 绘制人脸框
    for top,right,bottom,left in face_location:
        cv2.rectangle(image,[left,top],[right,bottom],[255,0,0],4)
    # 结果显示
    cv2.imshow("Face Detect Result",image)
    cv2.waitKey(0)