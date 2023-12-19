# -*- Coding : utf-8 -*-
# 改版Python测试：Fibonacci数列前40项

# 使用递归方式写的Fibonacci数列
# 代码开始

import time                 # 调包：计时器
import functools

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
    print("Answer is :",Fibonacci(496))
    # 获取结束时间
    t1 = float(time.time())
    # 输出，代码结束
    print("Used %s seconds."%(float(t1 - t0)))