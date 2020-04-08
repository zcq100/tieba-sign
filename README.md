## 百度贴吧自动签到

### 安装
```
pip install --user tieba-sign
```

### 使用说明
```
C:\Users\>tieba-sign -h
usage: tieba-sign [-h] [-c COOKIE] [-f FILE] [-t TIME] [-d] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -c COOKIE, --cookie COOKIE
                        Cookies
  -f FILE, --file FILE  cookies file
  -t TIME, --time TIME  sleep time
  -d, --dump            dump list to file
  -v                    verbose mode
```

首先登录百度，然后打开浏览器调试工具(按F12)，在网络，请求头找到cookie,然后拷贝过来。
```
C:\Users\>tieba-sign -c "Cookie:hUb3NkcVBMfk1NV1Y3bGtjdHBnNzVFYktRbjBCVmVvWS03YzZ"
```

###  代码中使用
```
from tieba import Tieba

tieba=Tieba("Your Cookie")
tieba.get_bars()
tieba.batch_sign(1)
```