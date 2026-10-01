#include "rclcpp/rclcpp.hpp"

int main(int argc, const char **argv)
{
    rclcpp::init(argc, argv);
    rclcpp::Node::SharedPtr node = std::make_shared<rclcpp::Node>("cpp_node");
    RCLCPP_INFO(node->get_logger(), "你好CPP");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}