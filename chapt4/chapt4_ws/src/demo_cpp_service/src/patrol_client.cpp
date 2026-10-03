#include "rclcpp/rclcpp.hpp"
#include <ctime> //产生随机数
#include "chapt4_interfaces/srv/patrol.hpp"
#include <chrono>
#include "rcl_interfaces/msg/parameter.hpp"
#include "rcl_interfaces/msg/parameter_value.hpp"
#include "rcl_interfaces/msg/parameter_type.hpp"
#include "rcl_interfaces/srv/set_parameters.hpp"

using SetP = rcl_interfaces::srv::SetParameters;

using namespace std::chrono_literals;

using chapt4_interfaces::srv::Patrol;

class PatrolClientNode : public rclcpp::Node
{
private:
    rclcpp::Client<Patrol>::SharedPtr client_;
    rclcpp::TimerBase::SharedPtr timer_;

public:
    PatrolClientNode() : Node("patrol_client_node")
    {
        srand(time(NULL));
        client_ = this->create_client<Patrol>("patrol");
        timer_ = this->create_wall_timer(10s, std::bind(&PatrolClientNode::send_request_callback, this));
        RCLCPP_INFO(this->get_logger(), "完成节点初始化");
    }
    void send_request_callback()
    {
        auto request = std::make_shared<Patrol::Request>();
        while (!this->client_->wait_for_service(10s)) // 服务上线则为1
        {
            if (rclcpp::ok())
            {
                RCLCPP_INFO(this->get_logger(), "等待服务上线");
            }
            else
            {
                RCLCPP_ERROR(rclcpp::get_logger("rclcpp"), "ros已经被终止了");
            }
        }

        // 服务上线
        request->target_x = rand() % 15;
        request->target_y = rand() % 15;
        RCLCPP_INFO(this->get_logger(), "目标点准备好:(%d,%d)", (int)request->target_x, (int)request->target_y);

        // 发送请求
        // 这里的回调函数的位置是当这个请求被响应完成之后会自动调用的回调函数，而且会传入这个result_future给这个回调函数
        auto future = this->client_->async_send_request(request,
                                                        [&](rclcpp::Client<Patrol>::SharedFuture result_future) -> void
                                                        {
                                                            auto response = result_future.get();
                                                            if (response->result == Patrol::Response::SUCCESS)
                                                            {
                                                                RCLCPP_INFO(this->get_logger(), "请求目标点成功");
                                                            }
                                                            else
                                                            {
                                                                RCLCPP_INFO(this->get_logger(), "请求失败");
                                                            }
                                                        });
    }

    SetP::Response::SharedPtr call_set_parameters(const rcl_interfaces::msg::Parameter &param)
    {
        auto client = this->create_client<SetP>("/turtle_control_node/set_parameters");
        while (!client->wait_for_service(1s))
        {
            if (!rclcpp::ok())
            {
                RCLCPP_ERROR(this->get_logger(), "ros已经被终止了");
                return nullptr;
            }
            RCLCPP_INFO(this->get_logger(), "等待服务上线");
        }
        auto request = std::make_shared<SetP::Request>();
        request->parameters.push_back(param);
        auto future = client->async_send_request(request);
        rclcpp::spin_until_future_complete(this->get_node_base_interface(), future);
        auto response = future.get();
        return response;
    }

    // 更新参数k
    void update_server_param_k(double k)
    {
        auto param = rcl_interfaces::msg::Parameter();
        param.name = "k";
        auto param_value = rcl_interfaces::msg::ParameterValue();
        param_value.type = rcl_interfaces::msg::ParameterType::PARAMETER_DOUBLE;
        param_value.double_value = k;
        param.value = param_value;
        auto response = this->call_set_parameters(param);
        if (response == NULL)
        {
            RCLCPP_INFO(this->get_logger(), "参数更新失败");
            return;
        }

        for (auto result : response->results)
        {
            if (result.successful == false)
            {
                RCLCPP_INFO(this->get_logger(), "参数更新失败，原因:%s", result.reason.c_str());
            }
            else
            {
                RCLCPP_INFO(this->get_logger(), "参数更新成功");
            }
        }
    }
};

int main(int argc, const char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<PatrolClientNode>();
    node->update_server_param_k(4.0);
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}