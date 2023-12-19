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