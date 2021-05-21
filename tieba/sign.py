import logging
import time
import requests

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s 贴吧签到: %(message)s')


class Forum(object):

    def __init__(self, id, name, level, exp, isSign):
        self.id = id
        self.name = name
        self.level = level
        self.exp = exp
        self.isSign = isSign


class Tieba():
    TIEBA_LIKE = "/mo/q/newmoindex"
    SIGN_PATH = "/sign/add"
    HOST = "tieba.baidu.com"

    def __init__(self, bduss=None):
        """
        BDUSS 是你的cookie里面的登录凭证，用浏览器登录，然后找到登录的cookie，复制BDUSS的值
        """
        self.token = bduss
        self._forums = []
        self.session = Tieba.Net("https://%s" % Tieba.HOST)
        self.session.headers["cookie"] = f"BDUSS={bduss}"

    def get_tiebas(self):
        """
        获取所有关注的贴吧名称
        """
        if len(self._forums) > 0:
            return
        resp = self.session.get(Tieba.TIEBA_LIKE)
        _data = resp.json()
        if _data["error"] == "success":
            for tb in _data["data"]["like_forum"]:
                forum = Forum(id=tb["forum_id"], name=tb["forum_name"],
                              exp=tb["user_exp"], level=tb["user_level"], isSign=tb["is_sign"])
                self._forums.append(forum)
            logging.info(f"获取到了{len(self._forums)}个贴吧信息")

    def status(self):
        """
        获取签到状态
        """
        self.get_tiebas()
        logging.info("#签到状态:")
        count = 0
        for tb in self._forums:
            logging.info(f"{tb.name}")
            if tb.isSign == 1:
                count += 1
        logging.info(f"#其中{count}个已经签过了:")

    def sign(self, name, delay=0):
        """
        签到一个贴吧
        """
        if name is None:
            logging.info("贴吧名不能为空")
            return

        forum = self._get_forum(name)
        if forum is not None and forum.isSign == 1:
            logging.info(f"{name}已经签过了")
            return

        time.sleep(delay)

        payload = f"ie=utf-8&kw={name}"
        resp = self.session.post(Tieba.SIGN_PATH, payload)
        # logging.debug(resp.json())
        if resp.status_code == 200:
            j = resp.json()
            if j["no"] == 0:
                for tb in self._forums:
                    if tb.name == name:
                        tb.isSign = 1
                logging.info(f"{name}签到成功")
            elif j["no"] == 2150040:
                raise CaptchaException(f"!!!贴吧:{name}", j)
            else:
                raise SignFailException(f"{name}签到失败", j['error'])

    def auto_sign(self, delay=3):
        """
        批量签到
        delay 签到间隙时间
        """
        self.get_tiebas()
        sleepTime = delay
        for forum in self._forums:
            try:
                self.sign(forum.name, delay=sleepTime)
                sleepTime = delay
            except CaptchaException as e:
                logging.info(e)
                # TODO(zcq100): 需要处理验证码的问题
                # 暂时休眠3分钟
                sleepTime += 10
                logging.info(f"{sleepTime}秒后再试..")

            except Exception as e:
                logging.info(e)

    def _get_forum(self, name):
        for f in self._forums:
            if f.name == name:
                return f

    class Net:
        headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
            'host': "tieba.baidu.com",
            'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
            'x-requested-with': "XMLHttpRequest"
        }

        def __init__(self, host):
            self.host = host

        def get(self, path):
            url = self.host+path
            return requests.get(url, headers=self.headers)

        def post(self, path, payload):
            url = self.host+path
            return requests.post(url, headers=self.headers, data=payload.encode("utf-8"))


class CaptchaException(Exception):
    ...


class SignFailException(Exception):
    ...


def main(bduss):
    app = Tieba(bduss)
    # app.sign("看门狗")
    app.status()
    app.auto_sign()


if __name__ == '__main__':
    main("RsNlNwbUpKdGtjeS1zaFZxcHJMQVZzM3BEUkl5dGpURGFDSVJoRTJOeTRTczFnRVFBQUFBJCQAAAAAAAAAAAEAAACtK9sBemNxMTAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALi9pWC4vaVgdz")
