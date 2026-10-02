#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "turtlesim/msg/pose.hpp"
#include <functional>
#include <chrono>

using geometry_msgs::msg::Twist;
using turtlesim::msg::Pose;
using namespace std::chrono_literals;

class TurtleControlNode:public rclcpp::Node
{
private:
    rclcpp::Publisher<Twist>::SharedPtr publisher_;
    rclcpp::Subscription<Pose>::SharedPtr subscriber_;
    double target_x_;
    double target_y_;
    double target_z_;
    double k;
    double max_speed;
public:
    TurtleControlNode():Node("turtle_control_node"),target_x_(1),target_y_(1.0),target_z_(1.0),k(1.0),max_speed(3.0)
    {
        publisher_=this->create_publisher<Twist>("/turtle1/cmd_vel",10);
        subscriber_=this->create_subscription<Pose>("/turtle1/pose",10,std::bind(&TurtleControlNode::on_pose_received,this,std::placeholders::_1));
    }
    void on_pose_received(const Pose::SharedPtr pose)//发布者的这个消息是受到的消息的共享指针
    {
        double cur_x=pose->x;
        double cur_y=pose->y;
        RCLCPP_INFO(this->get_logger(),"当前位置为(%f,%f)",cur_x,cur_y);
        auto distance=std::sqrt(
            (target_x_-cur_x)*(target_x_-cur_x)+(target_y_-cur_y)*(target_y_-cur_y)
        );
        auto angle=std::atan2(target_y_-cur_y,target_x_-cur_x)-pose->theta;
        auto msg=Twist();
        if(distance>0.1)
        {
            if(fabs(angle)>0.2)
            {
                msg.angular.z=fabs(angle);
            }
            else{
                msg.linear.x=k*distance;
            }
        }
        if(msg.linear.x>max_speed)
        {
            msg.linear.x=max_speed;
        }

        publisher_->publish(msg);

        
    }
};

int main(int argc,const char** argv)
{
    rclcpp::init(argc,argv);
    auto node=std::make_shared<TurtleControlNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}