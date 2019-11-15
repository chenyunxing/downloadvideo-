# coding=utf8
import winpexpect

cmd = 'ffmpeg -i index.m3u8 file.mp4'
thread = winpexpect.winspawn(cmd)
print("started %s" % cmd)
cpl = thread.compile_pattern_list([
    winpexpect.EOF,
    "frame= *\d+",
    '(.+)'
])
while True:
    i = thread.expect_list(cpl, timeout=None)
    if i == 0: # EOF
        print("the sub process exited")
        break
    elif i == 1:
        frame_number = thread.match.group(0)
        print(frame_number)
        thread.close
    elif i == 2:
        #unknown_line = thread.match.group(0)
        #print unknown_line
        pass
