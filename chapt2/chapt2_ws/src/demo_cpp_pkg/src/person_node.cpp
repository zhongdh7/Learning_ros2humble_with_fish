#include "rclcpp/rclcpp.hpp"

class PersonNode : public rclcpp::Node
{
public:
    PersonNode();
    PersonNode(const std::string &name, int age);
    void eat(const std::string &food_name);

private:
    std::string name_;
    int age_;
};

PersonNode::PersonNode() : Node("cpp_node")
{
    this->name_ = "cpp_node";
    this->age_ = 0;
}

PersonNode::PersonNode(const std::string &name, int age) : Node(name), name_(name), age_(age) 
{
    RCLCPP_INFO(this->get_logger(),"你好CPP");
}

void PersonNode::eat(const std::string &food_name)
{
    RCLCPP_INFO(this->get_logger(), "我是%s,今年%d岁了，喜欢吃%s", this->name_.c_str(), this->age_, food_name.c_str());
}

int main(int argc, const char **argv)
{
    rclcpp::init(argc, argv);
    std::string name = "zhangsan";
    int age = 18;
    std::shared_ptr<PersonNode> node = std::make_shared<PersonNode>(name, age);

    node->eat("鱼香肉丝");
    rclcpp::spin(node);

    rclcpp::shutdown();
    return 0;
}