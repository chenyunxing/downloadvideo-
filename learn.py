# coding=utf8
import tools
import subprocess
import time
url  = 'index.m3u8'
filename = str(time.time()) + '.mp4'
# 第一条命令获取视频相关信息,主要希望获取到视频时长参数
# cmd = "ffmpeg -i " + url
cmd = "ffmpeg -i " + url + ' ' + filename
# Duration: 00:01:02.49, start: 0.000000, bitrate: 865 kb/s
process = subprocess.Popen(cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
# process.wait()
while 1:
    line = process.stdout.readline()
    # line2 = process.stdin.readline()
    line = tools.change_str(line)
    # line2 = tools.change_str(line2)
    if line != '' and process.poll() is None:
        print(line)
        print('--------------------------------')
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
