#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "turtlesim/msg/pose.hpp"
#include <functional>
#include <chrono>
#include "chapt4_interfaces/srv/patrol.hpp"
#include "rcl_interfaces/msg/set_parameters_result.hpp"

using rcl_interfaces::msg::SetParametersResult;

using chapt4_interfaces::srv::Patrol;

using geometry_msgs::msg::Twist;
using turtlesim::msg::Pose;
using namespace std::chrono_literals;

class TurtleControlNode : public rclcpp::Node
{
private:
    rclcpp::Service<Patrol>::SharedPtr server_;
    rclcpp::Publisher<Twist>::SharedPtr publisher_;
    rclcpp::Subscription<Pose>::SharedPtr subscriber_;
    double target_x_;
    double target_y_;
    double target_z_;
    double k;
    double max_speed;
    OnSetParametersCallbackHandle::SharedPtr parameter_callback_handle;

public:
    TurtleControlNode() : Node("turtle_control_node"), k(1.0), max_speed(3.0), target_x_(3.0), target_y_(3.0), target_z_(0)
    {
        this->declare_parameter("k", 1.0);
        this->declare_parameter("max_speed", 1.0);
        this->get_parameter("k", k);
        this->get_parameter("max_speed", max_speed);
        parameter_callback_handle = this->add_on_set_parameters_callback(
            [&](const std::vector<rclcpp::Parameter> &parameters)
                -> rcl_interfaces::msg::SetParametersResult
            {
                SetParametersResult result;
                result.successful = true;
                for (const auto &param : parameters)
                {
                    if (param.get_name() == "k")
                    {
                        this->k = param.as_double();
                        RCLCPP_INFO(this->get_logger(), "更新参数值:%s=%f", param.get_name().c_str(), param.as_double());
                    }
                    if (param.get_name() == "max_speed")
                    {
                        this->max_speed = param.as_double();
                        RCLCPP_INFO(this->get_logger(), "更新参数值:%s=%f", param.get_name().c_str(), param.as_double());
                    }
                }
                return result;
            });
        publisher_ = this->create_publisher<Twist>("/turtle1/cmd_vel", 10);
        subscriber_ = this->create_subscription<Pose>("/turtle1/pose", 10, std::bind(&TurtleControlNode::on_pose_received, this, std::placeholders::_1));
        server_ = this->create_service<Patrol>("patrol",
                                               [&](const Patrol::Request::SharedPtr request, Patrol::Response::SharedPtr response) -> void
                                               {
                                                   if ((request->target_x >= 0 && request->target_x <= 12) && (request->target_y >= 0 && request->target_y <= 12))
                                                   {
                                                       this->target_x_ = request->target_x;
                                                       this->target_y_ = request->target_y;
                                                       response->result = Patrol::Response::SUCCESS;
                                                   }
                                                   else
                                                   {
                                                       response->result = Patrol::Response::FAIL;
                                                   }

                                                   // 因为C++有指针可以不需要返回response
                                               });
        RCLCPP_INFO(this->get_logger(), "成功启动乌龟启动服务端");
    }
    void on_pose_received(const Pose::SharedPtr pose) // 发布者的这个消息是受到的消息的共享指针
    {
        double cur_x = pose->x;
        double cur_y = pose->y;
        RCLCPP_INFO(this->get_logger(), "当前位置为(%f,%f)", cur_x, cur_y);
        auto distance = std::sqrt(
            (target_x_ - cur_x) * (target_x_ - cur_x) + (target_y_ - cur_y) * (target_y_ - cur_y));
        auto angle = std::atan2(target_y_ - cur_y, target_x_ - cur_x) - pose->theta;
        auto msg = Twist();
        if (distance > 0.1)
        {
            if (fabs(angle) > 0.2)
            {
                msg.angular.z = fabs(angle);
            }
            else
            {
                msg.linear.x = k * distance;
            }
        }
        if (msg.linear.x > max_speed)
        {
            msg.linear.x = max_speed;
        }

        publisher_->publish(msg);
    }
};

int main(int argc, const char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TurtleControlNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}