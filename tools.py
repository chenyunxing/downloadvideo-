import chardet
# 无论传入bytes还是str返回str
def change_str(s):
    arg_type = type(s)
    if arg_type == type('s'):
        return s
    elif arg_type == type(b's'):
        s_info = chardet.detect(s)
        if s_info['encoding']:
            return s.decode(s_info['encoding'])
        else:
            return "error,can't know encode"
    else:
        print(arg_type)
        return "error,arg not str or bytes"
# 无论传入bytes还是str返回bytes
def change_bytes(s):
    arg_type = type(s)
    if arg_type == type(b's'):
        return s
    elif arg_type == type('s'):
        return s.encode('utf-8')
    else:
        return "error,arg not str or bytes"
# 定义一个由字符串类型时间转化为描述的函数
def time_to_second(time):
    '''
        如传入00:12:06
        将会转化为12*60+6即726
    '''
    time = time.strip()
    time = time.split(':')
    second = 0
    for i in range(len(time)):
        second = second + float(time[len(time) - i - 1]) * (60**i)
    return second
