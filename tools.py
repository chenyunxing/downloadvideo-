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
