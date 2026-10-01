#include <iostream>
#include <memory>
#include <string>

using namespace std;

int main()
{
    auto p1 = make_shared<string>("This is a str");
    cout << "p1的引用记数为：" << p1.use_count() << "指针内存存放的地址为:" << p1.get() << endl;
    cout << p1 << endl
         << *p1.get() << endl
         << *p1 << endl;

    auto p2 = p1;
    cout << p1.use_count() << endl;
    cout << p1.get() << endl;
    cout << p2.get() << endl;
    cout << p2.use_count() << endl;
    auto str = p1->c_str();
    p1.reset(); // 这个方法让这个p1不再指向这个地址
    cout << "p1的引用记数为：" << p1.use_count() << "指针内存存放的地址为:" << p1.get() << endl;
    cout << p2.use_count() << endl
         << p2.get() << endl;
    return 0;
}