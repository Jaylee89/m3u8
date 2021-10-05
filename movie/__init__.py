# import requests
# import os
# import time
# from multiprocessing import Pool

# def fetch(url):
#     url = 'https://dapian.video-yongjiu.com/20190917/12948_614ba440/1000k/hls/e6f33517ce300%04d.ts'%i
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
#     }
#     response = requests.get(url, headers = headers,stream=True,timeout=600, verify=False)
#     response.raise_for_status()
#     return response

# def merge(t,cmd):
#     time.sleep(t)
#     res=os.popen(cmd)
#     print(res.read())

# def file_write(response_data, filename):
#     with open(filename,'wb') as f:
#         f.write(response_data)
#         f.close()

# if __name__ == '__main__':
#     # get url list
    
#     # 创建进程池，执行10个任务
#     pool = Pool(10)
#     for i in range(500):
#         pool.apply_async(run, (i,)) #执行任务
#     pool.close()
#     pool.join()
#     #调用合并
#     # merge(5,"copy /b H:\\PyDownload\\*.ts H:\\PyDownload\\new.mp4")
#     print('ok！处理完成')