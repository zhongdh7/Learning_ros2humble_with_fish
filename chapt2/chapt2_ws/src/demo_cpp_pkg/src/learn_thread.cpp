#include <iostream>
#include <thread>
#include <chrono>       //和时间相关的头文件
#include <functional>   //函数封装器
#include "cpp-httplib/httplib.h"    //下载相关的头文件 

using namespace std;

class Download
{
public: 
    void download(const string& host,const string& path,
        const std::function<void(const std::string&,const std::string&)> callback_word_count)
        {
            cout<<"线程"<<this_thread::get_id()<<endl;
            httplib::Client client(host);
            auto response=client.Get(path);
            if(response && response->status==200)
            {
                callback_word_count(path,response->body);
            }
        }
    void start_download(const string& host,const string& path,
        const std::function<void(const std::string&,const std::string&)> callback_word_count)
        {
            thread thread(std::bind(&Download::download,this,placeholders::_1,placeholders::_2,placeholders::_3),host,path,callback_word_count);
            thread.detach();
        }
};

int main()
{
    Download d;
    auto word_count=[](const string&path,const string&result)->void{
        cout<<"下载完成"<<path<<result.length()<<result.substr(0,5)<<endl;
    };
    string host="http://0.0.0.0:8000";
    d.start_download(host,"/novel1.txt",word_count);
    d.start_download(host,"/novel2.txt",word_count);
    d.start_download(host,"/novel3.txt",word_count);

    std::this_thread::sleep_for(std::chrono::milliseconds(1000*5));
    return 0;
}