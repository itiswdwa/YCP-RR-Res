// CppTest_Loop.cpp: 此文件包含 "main" 函数。程序执行将在此处开始并结束。
// C++对比测试：循环累加
// 加到一亿次，测时间

// 代码开始
#include<iostream>
#include<chrono>
using namespace std;

int main()
{
    long long c = 0;                                                                     
    // 计算元归零
    printf("Started.\n");
    auto begin = std::chrono::high_resolution_clock::now();                              
    // 启动计时器
    while (c < 100000000)
    {
        c = c + 1;                                                                       
        //累加
    }
    auto end = std::chrono::high_resolution_clock::now();                                
    // 计时器结束
    auto elapsed = std::chrono::duration_cast<std::chrono::nanoseconds>(end - begin);
    printf("Completed.\nUsed %.14lf seconds.", elapsed.count() * 1e-9);
    // 输出，代码结束
    return 0;
}