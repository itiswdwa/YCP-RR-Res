# Python3性能分析与尝试优化-研究报告

---

## 目录

* [概述](#abstract)

* [简介](#introduction)

* [Python3性能测试](#py3-p-t-c)

* [性能测试结果分析与评估](#p-t-r-a-c)

* [尝试优化与优化后结果分析](#t-a-r-a)

* [结论](#conclusion)

* [参考文献和附录](#b-m)

---

## 概述<a name='abstract'></a>

    本研究报告讨论了Python3性能分析与优化。经过一些动手实验与操作，我们得到了以下结论：

* 因为Python是一种解释器语言，也因为其GIL锁与动态内存管理机制，Python速度会相当慢

* 在对Python进行优化后，Python速度可以大幅度提高，但速度仍无法与C++等静态编译型语言抗衡

---

## 简介<a name='introduction'></a>

    出于Python丰富的第三方库及其友好的语法，我经常使用Python来制作一些需要的程序。我在进行实际的代码编写与生产环境测试中，我能够明显感受到Python的速度问题——是的，它的速度太慢了！于是，我进行了此次研究，希望能够尝试对Python进行一些优化来加快速度，并投入到生产环境中以进行对服务器系统的升级与节省CPU能耗。

---

## Python3性能测试与对比<a name='py3-p-t-c'></a>

    为了对Python与C++速度对比有一个直观的认识，将对Python与C++进行性能测试

    以下是测试性能机器配置

| 编号  | 语言     | 语言版本                                                             | 运行机器CPU                                 | 架构    | 运行系统                          |
|:---:|:------:|:----------------------------------------------------------------:|:---------------------------------------:|:-----:| ----------------------------- |
| 1   | Python | Python 3.10.5 (main, Dec 17 2023) [GCC 10.2.1 20210110] on linux | Intel Core i3-2120 @ 4x 3.3GHz          | amd64 | Debian(Linux 5.10.0-16-amd64) |
| 2   | C++    | gcc version 10.2.1 20210110 (Debian 10.2.1-6)                    | Intel Core i3-2120 @ 4x 3.3GHz [31.0°C] | amd64 | Debian(Linux 5.10.0-16-amd64) |

    测试将分为三个方面：循环（连加）、递归（斐波那契数列）、网络流（爬虫）

> 注意：
> 
>     爬虫方面由于C++语言的“特性”需要从头写起，代码极其繁杂，因此将不会提供爬虫方面的C++代码，而只提供Python的代码使其与改进后相比较。

    每次测试将运行5次指定程序，程序最终结果取这五次的平均值。

> 第一次测试：循环。
> 
>         测试代码请在[这里](#code-loop-1) 查看，或访问[这里](https://github.com/itiswdwa/)下载

    

    在上述机器上的执行结果：

| 语言     | 第一次测试      | 第二次测试        | 第三次测试       | 第四次测试        | 第五次测试       | 最终结果       |
|:------:|:----------:|:------------:|:-----------:|:------------:|:-----------:|:----------:|
| C++    | 0.2386891  | 0.24193172   | 0.24163818  | 0.24416895   | 0.24655456  | 0.24259651 |
| Python | 11.0492892 | 10.021233797 | 9.972793102 | 10.979090452 | 9.986224174 | 10.401726  |

> 第二轮测试：递归
> 
>         测试代码请在[这里](#code-fib-1) 查看，或访问[这里](https://github.com/itiswdwa/)下载

        

        在上述机器上的执行结果：

| 语言     | 第一次测试       | 第二次测试       | 第三次测试       | 第四次测试      | 第五次测试       | 最终结果       |
|:------:|:-----------:|:-----------:|:-----------:|:----------:|:-----------:|:----------:|
| C++    | 1.11744184  | 1.10839218  | 1.117330127 | 1.1115380  | 1.11115593  | 1.1115366  |
| Python | 40.22082686 | 39.63060235 | 38.64069986 | 41.0531318 | 38.43628692 | 39.5963095 |

> 第三轮测试：网络流
> 
>         测试代码请在[这里](#code-crawler-1) 查看，或访问[这里](https://github.com/itiswdwa/)下载
> 
>         注意：本次测试使用了C-S模式。服务器使用golang编写。

    

> 注：本次测试使用了外部文件b.txt，目的是为了加强负载。b.txt文件由随机数构成，大小为5098KB，可以在本项目Github上下载。

        在上述机器上的执行结果：

| 语言     | 第一次测试       | 第二次测试       | 第三次测试       | 第四次测试      | 第五次测试     | 最终结果      |
|:------:|:-----------:|:-----------:|:-----------:|:----------:|:---------:|:---------:|
| Python | 42.09808230 | 45.37146854 | 53.03924727 | 32.2660923 | 32.001096 | 40.955197 |

> 注意：这次的测试结果由于网络的不稳定性，摘除了过分不正常的数据，同时在局域网内完成，降低不确定性。

---

## 性能测试结果分析与评估<a name='p-t-r-a-c'></a>

    在上一个部分的测试中，我们分别得到了Python与C++在累加、递归以及网络流（C++没有！太麻烦！）的表现情况。数据是不出意料的，C++在性能方面大大超过了Python。现在分析一下原因：

* 在运行两种语言编写的代码是，命令是不一样的。C++使用`g++ *.cpp -o ***`来编译，并用`***`来运行该程序。而Python则使用`python3 ***.py`直接运行。这是两种语言最大的不同：运行机制。Python是解释型语言，由解释器一行一行读代码执行；C++由编译器编译为二进制文件，然后直接执行。处于这两种机制，Python便是“生来”落后于C++的。

* 上网查阅资料，我了解到出于Python的GIL（全局解释器锁）特性，即在任意时刻有且只有一个线程(thread)占据着CPU，这样虽然可以提高内存安全性，但也会导致Python的速度被永远锁死

因此，综合上述分析，我们提出以下优化思路：

1. 通过对部分Python代码进行一些改进，使用JIT技术即时编译为二进制数据，可以增强大量重复的函数的速度，这可以提高第一轮测试循环的速度

2. 通过部分提前编译为机器码，减少解释器运行的任务，提高第一轮测试循环的速度

3. 查阅资料，了解了“备忘机制”，这可以提高第二轮测试递归速度

4. 使用异步技术，通过对一个进程的多分配方式利用，用“协程”的方式提高第三轮测试网络流速度

将在下一部分进行优化尝试。

## 尝试优化与优化后结果分析<a name='t-a-r-a'></a>

> 第一轮优化测试：循环递加
> 
>         测试代码请在[这里](#code-loop-2) 查看，或访问[这里](https://github.com/itiswdwa/)下载

        python代码（使用思路1）：



        使用上述机器后运行结果：

| 语言         | 第一次测试      | 第二次测试      | 第三次测试       | 第四次测试       | 第五次测试      | 最终结果      |
| ---------- | ---------- | ---------- | ----------- | ----------- | ---------- | --------- |
| Python3.10 | 0.22415876 | 0.22443890 | 0.223468780 | 0.222794294 | 0.22235202 | 0.2234425 |

> 第二轮优化测试：递归
> 
>         测试代码请在[这里](#code-fib-2) 查看，或访问[这里](https://github.com/itiswdwa/)下载

        Python代码（使用思路3）：



        使用上述机器运行结果：

| 语言     | 第一次测试     | 第二次测试      | 第三次测试    | 第四次测试      | 第五次测试      | 最终结果       |
| ------ | --------- | ---------- | -------- | ---------- | ---------- | ---------- |
| Python | 0.0000703 | 0.00008034 | 0.000062 | 0.00006389 | 0.00006723 | 0.00006895 |

> 第三轮优化测试
> 
>         测试代码请在[这里](#code-crawler-2) 查看，或访问[这里](https://github.com/itiswdwa/)下载

        Python代码（使用思路4）



| 语言     | 第一次测试      | 第二次测试     | 第三次测试      | 第四次测试     | 第五次测试     | 最终结果       |
|:------:|:----------:|:---------:|:----------:|:---------:|:---------:|:----------:|
| Python | 23.1568026 | 22.291598 | 22.3281288 | 22.317199 | 22.471568 | 22.5130596 |

> 第四轮优化测试
> 
>         测试代码请在[这里](#code-loop-4) 查看，或访问[这里](https://github.com/itiswdwa/)下载
> 
> 使用上述机器运行结果如下

| 语言     | 第一次测试     | 第二次测试      | 第三次测试      | 第四次测试      | 第五次测试      | 最终结果       |
| ------ | --------- | ---------- | ---------- | ---------- | ---------- | ---------- |
| Python | 0.7305562 | 0.73211151 | 0.72743855 | 0.73526983 | 0.73600063 | 0.73227535 |

---

## 结论<a name='conclusion'></a>

        通过以上实验与探究，我们得到了制约Python性能的几个最重要的因素以及应对它的方法。

1. Python是一门解释型语言，这从根本上制约了Python的性能；而对于Python的解释机制而言，既可以使用JIT即时编译为机器码，也可以使用CPython自带工具对Python进行到C的转换，两种方法提速都很显著；
2. 对于递归来说，可以使用备忘机制来加速Python性能；
3. Python具有GIL锁（全局解释器锁），这一特性使Python在运行时的任意时刻只有一个进程运行；对于此项，我们可以选择删除GIL锁，但其副作用将也是巨大的，推荐使用异步async库，在Python一个进程中用多个协程的方式最大化使用CPU资源。

---

## 参考文献和附录<a name='b-m'></a>

> #### 参考文献

1. Python官方网站：www.python.org               -->Python应用程序的下载

2. Python官方文档：docs.python.org               -->大部分Python语法

3. CSDN博客:             blog.csdn.net                    -->编写过程中发生的问题

4. PEP：                      peps.python.org              -->PEP 703；PEP 693；PEP443；PEP 8

> #### 附录
> 
>         Python与C++代码在这里。

#### 对于第一轮测试（循环）<a name='code-loop-1'></a>

C++代码：

```cpp
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
```

Python代码：

```python
# -*- Coding : utf-8 -*-
# 原版Python测试：循环累加
# 累加到一亿次，计算时间
# 代码开始

import time                 # 调包：计时器

def b():
    p = 0
    # 获取起始时间
    print("Started.")
    t0 = float(time.time())
    # 进行计算
    while(p < 100000000):
        p = p + 1
    # 获取结束时间
    t1 = float(time.time())
    # 输出，代码结束
    print("Completed.\nUsed %s seconds."%(float(t1 - t0)))
```

#### 对于第二轮测试（递归）：<a name='code-fib-1'></a>

C++代码：

```cpp
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
```

Python代码：

```python
# -*- Coding : utf-8 -*-
# 原版Python测试：Fibonacci数列前40项

# 使用递归方式写的Fibonacci数列
# 代码开始

import time                 # 调包：计时器

def Fibonacci(n):
    if n < 2:
        # 临界条件：n < 2
        return n
    else:
        # 前两项相加
        return Fibonacci(n - 1) + Fibonacci(n - 2)

# 递归函数编写结束
# 开始调用
if __name__  == '__main__':
    # 获取起始时间
    print("Started.")
    t0 = float(time.time())
    # 进行计算
    print("Answer is :",Fibonacci(40))
    # 获取结束时间
    t1 = float(time.time())
    # 输出，代码结束
    print("Used %s seconds."%(float(t1 - t0)))
```

#### 对于第三轮测试：网络流<a name='code-crawler-1'></a>

Go代码：

```go
package main

import (
        "log"
        "net/http"
)

func main() {
        file := http.FileServer(http.Dir("public"))
        http.Handle("/static/", http.StripPrefix("/static/", file))
        err := http.ListenAndServe(":5999", nil)
        if err != nil {
                log.Println(err)
        }
}

```

Python代码：

```python
# -*- Coding : utf-8 -*-
# 原版Python测试：Python爬虫与文件IO

# 使用普通流写的Python爬虫与文件IO。
# 代码开始

import requests             
# 调包：爬虫
import time                 
# 调包：计时器
cnt = 5                  
# 计数器
print("Started.")
t0 = float(time.time())
while (cnt > 0):            
    # 计数器--：循环50次
    response = requests.get("http://192.168.0.102:5999/static/b%d.txt"%cnt)
    if response:            
        # 解析返回数据
        content = response.content
        file = open("b%d.txt"%cnt,'ab+')
        file.write(content)
        file.close()
        # 读取内容，写入文件
        cnt -= 1
    else:
        print("ERR!Connection empty.")
# 获取结束时间
t1 = float(time.time())
# 输出，代码结束
print("Used %s seconds."%(float(t1 - t0)))
```

#### 对于第一轮优化（循环）<a name='code-loop-2'></a>

Python代码：

```python
# -*- Coding : utf-8 -*-
# 改版Python测试：循环累加
# 累加到一亿次，计算时间
# 代码开始

import time                 # 调包：计时器
import numba                # 调包：JIT

p = 0

@numba.jit(nopython=True)
def add():
    p = 0
    while(p < 100000000):
        p = p + 1

if __name__  == '__main__':
    # 获取起始时间
    print("Started.")
    t0 = float(time.time())
    # 进行计算
    add()
    # 获取结束时间
    t1 = float(time.time())
    # 输出，代码结束
    print("Completed.\nUsed %s seconds."%(float(t1 - t0)))
```

### 对于第二轮优化（递归）<a name='code-fib-2'></a>

Python代码：

```python
    # -*- Coding : utf-8 -*-
    # 改版Python测试：Fibonacci数列前40项

    # 使用递归方式写的Fibonacci数列
    # 代码开始

    import time                 # 调包：计时器
    import functools
    # 备忘机制启动
    @functools.lru_cache()
    def Fibonacci(n):
        if n < 2:
            # 临界条件：n < 2
            return n
        else:
            # 前两项相加
            return Fibonacci(n - 1) + Fibonacci(n - 2)

    # 递归函数编写结束
    # 开始调用
    if __name__  == '__main__':
        # 获取起始时间
        print("Started.")
        t0 = float(time.time())
        # 进行计算
        print("Answer is :",Fibonacci(40))
        # 获取结束时间
        t1 = float(time.time())
        # 输出，代码结束
        print("Used %s seconds."%(float(t1 - t0)))
```

### 对于第三轮优化（网络流）<a name='code-crawler-2'></a>

Python代码

```python


    # -*- Coding : utf-8 -*-
    # 改版Python测试：Python爬虫与文件IO

    # 使用异步流写的Python爬虫与文件IO。
    # 代码开始
    import asyncio      # 调包：异步库
    import aiohttp      # 调包：网络异步库
    import time         # 调包：计时器
    import random       # 调包：随机数

    # 下载函数
    async def fetch(session,url):
        async with session.get(url, verify_ssl=False) as response:
             with open('b' + str(random.randint(1,9999)) + '.txt','ab+') as f:
                # 注意：这里不用全局变量是怕冲突
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)

    # 调用函数
    async def main(urlList):
        async with aiohttp.ClientSession() as session:
            task = [ asyncio.create_task( fetch(session,url)) for url in urlList ]
            done,pending = await asyncio.wait(task)

    if __name__ == '__main__':
        # 设置异步任务数
        numbers_of_async = 50
        urlList = []
        for i in range(1,50):
            urlList.append("http://192.168.1.6:6000/files/b%d.txt"%i)
        t0 = time.time()
        # 启动计数器
        numbers_of_times = int(len(urlList)/numbers_of_async) if not len(urlList)%numbers_of_async else int(len(urlList)/numbers_of_async) + 1
        for number in range(numbers_of_times):
            asyncio.run(main(urlList[number*numbers_of_async:number*numbers_of_async+numbers_of_async]))
        print("Time Used: %.14f seconds"%(time.time() - t0))


    # 代码结束
```

#### 对于第四轮优化：循环-2<a name='code-loop-3'></a>

> 由于需要命令行参与，不提供此次优化的代码
