# coding=utf8
# 此文件是为了实现断点续传等功能进行的
# 初步思路是，自我解析m3u8文件，随后打开文件，查看里面的ts连接
# 如果不是m3u8格式，那么就算了，直接默认下载，通过时间重新下载后合并
# 需要做到的是，中断后算是正常退出，会把原视频保存
# 如果是ts文件列表，那么可以考虑，直接重新下载ts文件（在ts文件小于多少秒或者多大是考虑
# 或者从ts文件的时间断点重新下载开始）
# ffmpeg -ss 183 -accurate_seek -i https://qxxx/index.m3u8 test.mp4
# ffmpeg -ss 120 -t 15 -accurate_seek -i https://qxxx/index.m3u8 test.mp4

# 此文件中进行函数化，后期考虑转类
# 首先第一步，想从learn。py复制下载逻辑，随后增加下载中可以进行输入的功能，输出的也写到一个页面里
# coding=utf8
import tools
import subprocess
import time
import re
import threading
def cmd(command):
    process = subprocess.Popen(command, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    return process
def print_info(process):
    old_time = time.time()
    # 正则表达式用于获取时间与对应下载速度
    time_pattern = re.compile(r'time=\d+:\d+:\d+.\d+')
    speed_pattern = re.compile(r'speed=[ ]*\S+')
    # 记录目前下载进度的变量,由于下载中可能网络中断，导致输出不包含已下载时间，因此需要记录到此刻前的下载进度
    save_time = 0
    while 1:
        if time.time() - old_time < 1:
            continue
        else:
            old_time = time.time()
        line = process.stderr.readline()
        # 这里发生十分奇怪的事情，如果把这里的byte类型字符进行decode()，原本输出的关于下载进度的信息就会删除，就是最后一行的下载信息，会被清除
        # 两者之间输出的对比就是
        '''
        b"frame=  317 fps= 43 q=28.0 size=    2304kB time=00:00:12.84 bitrate=1469.9kbits/s dup=1 drop=0 speed=1.76x    \rframe=  336 fps= 43 q=28.0 size=    2560kB time=00:00:13.51 bitrate=1551.9kbits/s dup=1 drop=0 speed=1.73x    \rframe=  359 fps= 43 q=28.0 size=    2560kB time=00:00:14.48 bitrate=1447.4kbits/s dup=1 drop=0 speed=1.72x    \rframe=  377 fps= 42 q=28.0 size=    3072kB time=00:00:15.16 bitrate=1659.8kbits/s dup=1 drop=0 speed= 1.7x    \rframe=  395 fps= 42 q=28.0 size=    3072kB time=00:00:15.81 bitrate=1591.5kbits/s dup=1 drop=0 speed=1.68x    \rframe=  415 fps= 42 q=25.0 size=    3328kB time=00:00:16.83 bitrate=1619.5kbits/s dup=1 drop=0 speed=1.68x    \r[https @ 0000015681969c40] Opening 'https://xxxxxx/747a49ee167000005.ts' for reading\r\n"
        --------------------------------
        [https @ 0000015681969c40] Opening 'https://xxxxxx/747a49ee167000005.ts' for reading
        '''
        # 因此这里采用之间str的方法，然后删除b'这种符号,然后重新进行解码
        line_str = str(line)
        line_str = line_str[2:-1]
        # line2 = tools.change_str(line2)
        if line != '' and process.poll() is None:
            video_time = time_pattern.findall(line_str)
            speed = speed_pattern.findall(line_str)
            if video_time:
                now_time = video_time[-1].strip()
                now_time = now_time.split('=')[-1].strip()
                now_time = tools.time_to_second(now_time)
                save_time = now_time
            if save_time <= all_time:
                # 进度
                percentage = save_time/all_time
                print("进度：%.2f%%"%(percentage*100))
                # 剩余时间
                if speed:
                    speed = speed[-1].strip()
                    speed = speed.split('=')[-1].strip()[0:-1]
                    speed = float(speed)
                    remaining_time = (all_time - save_time)/speed
                    print("还需%.2f秒下载"%remaining_time)
            else:
                print("下载时长超过获取的总时长，剩余下载时间不明！")
        else:
            break
    process.kill()
# 把需要输出的函数人到这里，目前这里设置为多线程输出,主线程只负责输入
def output(process):
    t = threading.Thread(target=print_info ,args=(process,))
    t.start()
# 网站链接自己填写
url  = 'https://xxxx.m3u8'
# 第一条命令获取视频相关信息,主要希望获取到视频时长参数
cmd_str = "ffmpeg -i " + url
process = cmd(cmd_str)

return_str =process.stderr.read()
return_str = return_str.decode()
# 获取视频时长
all_time_pattern = re.compile(r'Duration:[ ]*\d+:\d+:\d+.\d+')
temp = all_time_pattern.findall(return_str)
temp = temp[0].split(':')
temp.pop(0)
temp = ':'.join(temp).strip()
all_time = tools.time_to_second(temp) # 视频总时间的变量
print("视频总时长：%.2f秒"%all_time)
# 下载区
filename = str(time.time()) + '.mp4'
cmd = "ffmpeg -i " + url + ' ' +filename
process = subprocess.Popen(cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
output(process)
while 1:
    get_cmd = input()
    if get_cmd == 'exit':
        break
    else:
        print(get_cmd)
