#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include <chrono>
#include <functional>

// std::function<void ()>
using namespace std::chrono_literals; // 这个命令之后可以自动把这个输入的时间转换成chrono里面的数据
using geometry_msgs::msg::Twist;

class TurtleCircleNode : public rclcpp::Node
{
private:
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<Twist>::SharedPtr publisher_;

public:
    TurtleCircleNode(const std::string &node_name = "turtle_circle_node") : Node(node_name)
    {
        this->publisher_ = this->create_publisher<Twist>("/turtle1/cmd_vel", 10);
        timer_ = this->create_wall_timer(1000ms, std::bind(&TurtleCircleNode::timer_callback, this)); // 传入回调函数需要绑定
    }

    void timer_callback()
    {
        Twist msg;
        msg.linear.x = 1.0;
        msg.angular.z = 1.57;
        this->publisher_->publish(msg);
    }
};

int main(int argc, const char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TurtleCircleNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}