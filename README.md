# 百度贴吧 自动签到

## 如何安装

``` shell
pip install --user tieba-sign
```

## 使用说明

``` shell
#查看帮助
C:\Users\>tieba-sign -h
```

首先登录百度，然后打开浏览器调试工具(按F12)，在网络，请求头找到cookie,然后拷贝BDUSS段的值过来。

``` shell
tieba-sign -c "RsNlNwbUpKdGtjeS1zaFZxcHJMQVZzM3BE;"
```

## 代码中使用

``` python
from tieba import Tieba

app=Tieba("RsNlNwbUpKdGtjeS1zaFZxcHJMQVZzM3BE;")
#查看签到状态
app.status()
#批量签到
app.auto_sign()
# 2021-05-21 17:16:34,982 贴吧签到: 获取到了120个贴吧信息
# 2021-05-21 17:16:34,982 贴吧签到: 3d打印已经签过了
# 2021-05-21 17:16:34,983 贴吧签到: 4k已经签过了
```
