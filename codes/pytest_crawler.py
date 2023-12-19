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