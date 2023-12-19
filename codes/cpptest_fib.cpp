// CppTest_Fib.cpp: 此文件包含 "main" 函数。程序执行将在此处开始并结束。
// 斐波那契数列：前40项

// 代码开始
#include<iostream>
#include<chrono>
#pragma warning (disable:4819)

using namespace std;

int Fibonacci(int n)
{
    if (n < 2) 
    {
        // 临界条件
        return n;
    }
    else
    {
        // 前两项相加
        return Fibonacci(n - 1) + Fibonacci(n - 2);
    }
}

int main()
{
    printf("Started.\n");
    // 创建一个计时器
    auto begin = std::chrono::high_resolution_clock::now();
    // 计算斐波那契数列
    printf("Answer is : %ld\n", Fibonacci(40));
    // 结束计时
    auto end = std::chrono::high_resolution_clock::now();
    // 计算时间差（计算运行时间Δt）
    auto elapsed = std::chrono::duration_cast<std::chrono::nanoseconds>(end - begin);
    printf("Used %.14lf seconds.\n", elapsed.count() * 1e-9);
    return 0;
}