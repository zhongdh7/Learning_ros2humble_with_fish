#include <QApplication>
#include <QLabel>
#include <QString>
#include "rclcpp/rclcpp.hpp"
#include "status_interfaces/msg/system_status.hpp"

using status_interfaces::msg::SystemStatus;

int main(int argc,char** argv)
{
    QApplication app(argc,argv);
    QLabel* label=new QLabel();
    QString message=QString::fromStdString("Hello Qt");
    label->setText(message);
    label->show();
    app.exec();
    return 0;
}