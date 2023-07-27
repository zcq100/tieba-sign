# 百度贴吧 自动签到

## Action 自动签到

使用GitHub提供的CI任务，可以实现定时自动签到。

步骤：
1. Fork 本项目
2. 浏览器打开贴吧网站，按F12打开调试工具，在应用，Cookie，里面找到BDUSS，拷贝值到第三步。
3. 打开项目设置，在`Secrets and Variables`，点 New repository secret，添加变量名`BDUSS`，并填入上面获取到的值。
4. 保存后就可去Action里面触发任务。

## 如何安装

``` shell
pip install --user tieba-sign
```

## 使用说明

``` shell
#查看帮助
$ python -m tieba -h

usage: -m [-h] [-i INTERVAL] [-q | -v] [bduss]

百度贴吧批量签到

positional arguments:
  bduss        贴吧bduss的cookie值

options:
  -h, --help   show this help message and exit
  -i INTERVAL  签到间隔时间，批量签到避免弹验证码，默认5秒
  -q           安静模式，不显示运行信息
  -v           详细模式，显示更多运行信息
```

首先登录百度，然后打开浏览器调试工具(按F12)，在网络，请求头找到cookie,然后拷贝BDUSS段的值过来。

``` shell
python -m tieba "RsNlNwbUpKdGtj....aFZxcHJMQVZzM3BE"
```

```
2023-07-27 08:35:17,960 [tieba.sign] [INFO] 共关注了136个贴吧
2023-07-27 08:35:17,960 [tieba.sign] [INFO] 3d打印(2206871):已签
2023-07-27 08:35:17,960 [tieba.sign] [INFO] 4k(463046):已签
2023-07-27 08:35:17,960 [tieba.sign] [INFO] archlinux(1695944):已签
2023-07-27 08:35:17,960 [tieba.sign] [INFO] arduino(2712373):已签
2023-07-27 08:35:17,960 [tieba.sign] [INFO] blender(972857):已签
2023-07-27 08:35:17,960 [tieba.sign] [INFO] cemu(21343135):已签
2023-07-27 08:35:17,960 [tieba.sign] [INFO] centos(471894):已签
2023-07-27 08:35:17,960 [tieba.sign] [INFO] cheatengine(3338054):已签
...
2023-07-27 08:35:29,415 [tieba.sign] [INFO] 58个贴吧已签到，78个贴吧未签到
2023-07-27 08:35:29,475 [tieba.sign] [ERROR] 贴吧状态异常，ie=utf-8&kw=gta5
2023-07-27 08:35:29,715 [tieba] [INFO] 退出..
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
```

