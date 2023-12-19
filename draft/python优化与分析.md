# Python3性能分析与尝试优化--调查报告-大纲

* 标题：Python3性能分析与尝试优化

* 目录：

* * 概述（Abstract）
  
  * 简介
  
  * Python3性能测试（Python3 Performance Test）
  
  * 性能测试结果分析与评估（Performance Result Analysis and Assessment）
  
  * 尝试优化与优化后结果分析（The Analysis of the Result After Trying Optimizations）
  
  * 结论（Conclusions）
  
  * 参考文献和附录（References and Appendices）

* 概述：
  
  * 这一段大概说一下，本次调查研究的所有重要方面，略提一下结论，100-150字。

* 简介：
  
  * 大概就是：自己在实际使用中经常能够感受到Python与其它语言的性能差异，于是进行了此次研究，目的是对Python性能做出分析与优化以投入生产环境。200字。

* Python3性能测试：
  
  * 列出一下表格：（OS版本：Debian GNU/Linux 14（Kali））
  
  * | 编号  | 语言&版本      | 运行机器CPU           | 架构    | 运行项目        | 运行结果（5次平均值） |
    |:---:|:----------:|:-----------------:|:-----:|:-----------:|:-----------:|
    | 1   | Python3.10 | AMD® Ryzen™ 5500U | amd64 | Fibonacci   | xxx         |
    | 2   | Python3.10 | AMD® Ryzen™ 5500U | amd64 | loop-python | xxx         |
    | 3   | Python3.10 | AMD® Ryzen™ 5500U | amd64 | Crawler     | xxx         |
    | 4   | C++17      | AMD® Ryzen™ 5500U | amd64 | Fibonacci   | xxx         |
    | 5   | C++17      | AMD® Ryzen™ 5500U | amd64 | loop-cpp    | xxx         |
    | 6   | C++17      | AMD® Ryzen™ 5500U | amd64 | Crawler     | xxx         |
  
  * 运行代码整理

* 性能测试结果分析与评估
  
  1. 分析Python与C++速度差异-图表
  
  2. 查阅资料与Python源码分析
  
  3. 全局解释器锁GIL
  
  4. 动态内存管理机制

* 尝试优化与优化后结果分析
  
  1. 利用ctypes对接C的API关掉全局解释器锁
  
  2. 利用asyncio异步方式
  
  3. 利用缓存备忘机制functools
  
  4. 进行优化后实验（同性能测试表格）

* 结论
  
  * Python的解释机制与其GIL的限制使其速度缓慢
  
  * 可以利用关掉解释器锁的方法提高速度，但是不安全
  
  * 可以使用异步或缓存备忘机制，但是较为繁琐
  
  * 可以转换Python原始代码为CPython代码，但兼容性较差

* 参考文献和附录
  
  * 。。。
