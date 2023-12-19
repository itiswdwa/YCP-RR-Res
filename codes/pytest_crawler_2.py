import asyncio
import aiohttp
import time
import random

# 下载函数
async def fetch(session,url):
    async with session.get(url, verify_ssl=False) as response:
         with open('b' + str(random.randint(1,9999)) + '.txt','ab+') as f:
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
    numbers_of_async = 5

    # 启动计数器
    urlList = [
        "http://192.168.0.102:5999/static/b5.txt",
        "http://192.168.0.102:5999/static/b1.txt",
        "http://192.168.0.102:5999/static/b2.txt",
        "http://192.168.0.102:5999/static/b3.txt",
        "http://192.168.0.102:5999/static/b4.txt"
    ]
    t0 = time.time()
    numbers_of_times = int(len(urlList)/numbers_of_async) if not len(urlList)%numbers_of_async else int(len(urlList)/numbers_of_async) + 1
    for number in range(numbers_of_times):
        asyncio.run(main(urlList[number*numbers_of_async:number*numbers_of_async+numbers_of_async]))
    print("Time Used: %.14f seconds"%(time.time() - t0))

