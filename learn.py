import tools
import subprocess

cmd = "ffmpeg1 -i 2.mkv"
process = subprocess.Popen(cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
# process.wait()
out = process.stderr.read()
out = tools.change_str(out)
out = out.split('\r\n')
# print(out)
for i in out:
    print(i)
# temp = process.communicate(b'q')
# sleep(2)
process.kill()
