#include <iostream>
#include "rclcpp/rclcpp.hpp"

int main(int argc, char **argv)
{
    std::cout << "参数的数量" << argc << std::endl;
    std::cout << "程序的名字" << *argv << std::endl;
    // std::cout << "程序还有的参数" << *(argv + 1) << std::endl;

    if (argc >= 2)
    {
        std::string arg1 = *(argv + 1);
        if (arg1 == "--help")
        {
            std::cout << "这个是程序帮助文档" << std::endl;
            std::cout << argv << std::endl;
            std::cout << argv + 1 << std::endl;
            std::cout << sizeof(argv) << std::endl;
            std::cout << sizeof(char *) << std::endl;
        }
    }

    rclcpp::init(argc,argv);
    auto node=std::make_shared<rclcpp::Node>("cpp_node");

    RCLCPP_INFO(node->get_logger(),"你好CPP节点！");
    rclcpp::spin(node);
    rclcpp::shutdown();

    return 0;
}