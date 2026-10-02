#include <QApplication>
#include <QLabel>
#include <QString>
#include "rclcpp/rclcpp.hpp"
#include "status_interfaces/msg/system_status.hpp"

using status_interfaces::msg::SystemStatus;

class SystemStatusDisplay : public rclcpp::Node
{
private:
    rclcpp::Subscription<SystemStatus>::SharedPtr subscriber_;
    std::shared_ptr<QLabel> label_;

public:
    SystemStatusDisplay() : Node("sys_status_display")
    {
        label_ = std::make_shared<QLabel>();
        label_->setText(get_qstr_from_msg(std::make_shared<SystemStatus>()));
        RCLCPP_INFO(this->get_logger(), "展示数据节点已创建");
        subscriber_ = this->create_subscription<SystemStatus>("sys_status",
                                                              10,
                                                              std::bind(&SystemStatusDisplay::subscriber_callback, this, std::placeholders::_1));
        label_->show();
    }

    QString get_qstr_from_msg(const SystemStatus::SharedPtr msg)
    {
        std::stringstream show_str;
        show_str<<"===================系统状态可视化显示工具===================\n"
                <<"数据时间：\t"<<msg->stamp.sec<<"\ts\n"
                <<"主机名字：\t"<<msg->host_name<<"\n"
                <<"CPU使用率: \t"<<msg->cpu_percent<<"\t%\n"
                <<"内存使用率: \t"<<msg->memory_percent<<"\t%\n"
                <<"内存总大小: \t"<<msg->memory_total<<"\n"
                <<"可用内存大小: \t"<<msg->memory_available<<"\n"
                <<"网络发送数据总量: \t"<<msg->net_sent<<"\n"
                <<"网络接受总量: \t"<<msg->net_recv<<"\n";
        return QString::fromStdString(show_str.str());
    }

    void subscriber_callback(const SystemStatus::SharedPtr msg)
    {
        label_->setText(get_qstr_from_msg(msg));
    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    QApplication app(argc, argv);  // 必须先于任何 QWidget（含节点里的 QLabel）
    auto node=std::make_shared<SystemStatusDisplay>();
    std::thread spin_thread([&]()->void{
        rclcpp::spin(node);
    });
    spin_thread.detach();
    app.exec();
    rclcpp::shutdown();
    return 0;
}