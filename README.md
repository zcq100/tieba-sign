# 百度贴吧 自动签到

## 如何安装

``` shell
pip install --user tieba-sign
```

## 使用说明

``` shell
#查看帮助
usage: -m [-h] [-i INTERVAL] [-v] bduss

Baidu Tieba Sign

positional arguments:
  bduss        tieba bduss cookie

options:
  -h, --help   show this help message and exit
  -i INTERVAL  签到间隔时间
  -v           verbose
```

首先登录百度，然后打开浏览器调试工具(按F12)，在网络，请求头找到cookie,然后拷贝BDUSS段的值过来。

``` shell
python -m tieba "RsNlNwbUpKdGtjeS1zaFZxcHJMQVZzM3BE"
```

## 代码中使用

``` python
from tieba import Tieba

app=Tieba("RsNlNwbUpKdGtj....aFZxcHJMQVZzM3BE")
#查看签到状态
app.status()
# 单独签到
app.sign("python")
#批量签到
app.auto_sign()
# 2023-07-26 21:51:49,320 - tieba.sign - INFO - 共关注了136个贴吧
# 2023-07-26 21:51:49,320 - tieba.sign - DEBUG - 3d打印(2206871):已签
# 2023-07-26 21:51:49,320 - tieba.sign - DEBUG - 4k(463046):已签
# 2023-07-26 21:51:49,320 - tieba.sign - DEBUG - archlinux(1695944):已签
# 2023-07-26 21:51:49,320 - tieba.sign - DEBUG - arduino(2712373):已签
# 2023-07-26 21:51:49,320 - tieba.sign - DEBUG - blender(972857):已签
# ...
```
