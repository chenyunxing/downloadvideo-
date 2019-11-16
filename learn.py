# coding=utf8
import tools
import subprocess
import time
import re
# 网站链接自己填写
url  = 'https://xxxxx/index.m3u8'

# 第一条命令获取视频相关信息,主要希望获取到视频时长参数
cmd = "ffmpeg -i " + url
process = subprocess.Popen(cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
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
# 正则表达式用于获取时间与对应下载速度
time_pattern = re.compile(r'time=\d+:\d+:\d+.\d+')
speed_pattern = re.compile(r'speed=[ ]*\S+')
# 记录目前下载进度的变量,由于下载中可能网络中断，导致输出不包含已下载时间，因此需要记录到此刻前的下载进度
save_time = 0
while 1:
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
        time = time_pattern.findall(line_str)
        speed = speed_pattern.findall(line_str)
        if time:
            now_time = time[-1].strip()
            now_time = now_time.split('=')[-1].strip()
            now_time = tools.time_to_second(now_time)
            save_time = now_time
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
        break
process.kill()
