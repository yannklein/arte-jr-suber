import time

def ftime():
    return f"[{time.strftime('%y-%m-%d %H:%M:%S', time.gmtime())}]"