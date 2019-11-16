# coding=utf8
import tools
import subprocess
import time
url  = 'https://xxxxxx/index.m3u8'
filename = str(time.time()) + '.mp4'
# 第一条命令获取视频相关信息,主要希望获取到视频时长参数
# cmd = "ffmpeg -i " + url
cmd = "ffmpeg -i " + url + ' ' + filename
# Duration: 00:01:02.49, start: 0.000000, bitrate: 865 kb/s
process = subprocess.Popen(cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
# process.wait()
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
    with open('log.txt','ab') as f:
        f.write(line)
    # line2 = tools.change_str(line2)
    if line != '' and process.poll() is None:
        print(line_str)
        print('********************************')
        # print(line2)
    else:
        break
# out = process.stderr.read()
# out = tools.change_str(out)
# out = out.split('\r\n')
# print(out)
# for i in out:
#     print(i)
# temp = process.communicate(b'q')
# sleep(2)
process.kill()
