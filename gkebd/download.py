from vlermv import cache

@cache('~/.gkebd-https')
def https(domain):
    command = ['openssl', 's_client', '-connect', domain + ':443']
    p = subprocess.Popen(command, stdin = subprocess.PIPE,
                         stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    return p.communicate()

