#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "tf2/LinearMath/Quaternion.hpp" //提供tf2::Quaternion类
#include "tf2_geometry_msgs/tf2_geometry_msgs.hpp"
#include "tf2_ros/transform_listener.hpp"
#include "tf2_ros/buffer.hpp"
#include "tf2/utils.hpp"//四元数转换成欧拉角
#include <chrono>

using namespace std::chrono_literals;

using geometry_msgs::msg::TransformStamped;

class TFListener : public rclcpp::Node
{
private:
    std::shared_ptr<tf2_ros::TransformListener> listener_;
    rclcpp::TimerBase::SharedPtr timer_;
    std::shared_ptr<tf2_ros::Buffer> buffer_;

public:
    TFListener() : Node("tf_listener")
    {
        buffer_ = std::make_shared<tf2_ros::Buffer>(this->get_clock());
        listener_ = std::make_shared<tf2_ros::TransformListener>(*buffer_, this);
        timer_ = this->create_wall_timer(100ms, std::bind(&TFListener::get_transform, this));
    }
    void get_transform()
    {
        // 从buffer_里面查询坐标关系
        try
        {
            const auto transform = buffer_->lookupTransform("base_link", "target_point", this->get_clock()->now(), rclcpp::Duration::from_seconds(1.0));
            //获取查询结果
            auto translation=transform.transform.translation;
            auto rotation=transform.transform.rotation;
            double y,p,r;
            tf2::getEulerYPR(rotation,y,p,r);
            RCLCPP_INFO(this->get_logger(),"平移:%.3f,%.3f,%.3f,旋转:%.3f,%.3f,%.3f",translation.x,translation.y,translation.z,r,p,y);
        }
        catch (const std::exception &e)
        {
            std::cerr << e.what() << std::endl;
            RCLCPP_WARN(this->get_logger(),"%s",e.what());
        }
    }
};

int main(int argc, const char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TFListener>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}