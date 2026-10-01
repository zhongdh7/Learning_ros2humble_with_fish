#include <iostream>
#include <algorithm>
#include <string>
#include <functional> // 函数包装器头文件

using namespace std;

void save_with_free_fun(const std::string &file_name)
{
    cout << "自由函数" << file_name << endl;
}

class FileSave
{
public:
    void save_with_member_fun(const string &file_name)
    {
        cout << "成员方法" << file_name << endl;
    }
};

int main()
{
    FileSave file_save;
    auto save_with_lambda = [](const string &file_name) -> void
    { cout << "匿名函数" << file_name << endl; };
    // save_with_free_fun("file.txt");
    // file_save.save_with_member_fun("file.txt");
    // save_with_lambda("file.txt");

    std::function<void(const std::string &)> save1 = save_with_free_fun;
    std::function<void(const std::string &)> save2 = save_with_lambda;
    std::function<void(const std::string &)> save3 = std::bind(&FileSave::save_with_member_fun, &file_save, std::placeholders::_1);

    save1("file.txt");
    save2("file.txt");
    save3("file.txt");

    return 0;
}