import logging
import time
import sys
import argparse
import requests

# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s 贴吧签到: %(message)s')


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

    def __init__(self, bduss=None, ua=None, log=None):
        """
        BDUSS 是你的cookie里面的登录凭证，用浏览器登录，然后找到登录的cookie，复制BDUSS的值
        """
        self.token = bduss
        self._forums = []
        self.session = Tieba.Net("https://%s" % Tieba.HOST, ua)
        self.session.headers["Cookie"] = f"BDUSS={bduss}"
        self.log = log or logging.getLogger()

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
            c = len(self._forums)
            self.log.info(f"获取到了{c}个贴吧信息")
            return c
        else:
            self.log.error(f"获取贴吧列表失败，请检查百度令牌")

    def status(self):
        """
        获取签到状态
        """
        self.get_tiebas()
        self.log.info("#签到状态:")
        count = 0
        for tb in self._forums:
            self.log.info(f"{tb.name}")
            if tb.isSign == 1:
                count += 1
        self.log.info(f"#其中{count}个已经签过了:")

    def sign(self, name, delay=0):
        """
        签到一个贴吧
        """
        if name is None:
            raise ValueError("贴吧名不能为空")

        forum = self._get_forum(name)
        if forum is not None and forum.isSign == 1:
            self.log.info(f"{name}已经签过了")
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
                self.log.info(f"{name}签到成功")
            elif j["no"] == 2150040:
                raise CaptchaException(f"!!!贴吧:{name}", j)
            else:
                raise SignFailException(f"{name}签到失败", j['error'])

    def auto_sign(self, delay=3):
        """
        批量签到
        delay 签到间隙时间
        """
        if not self.get_tiebas():
            return
        for forum in self._forums:
            try:
                self.sign(forum.name, delay)
            except CaptchaException as e:
                self.log.info(e)
                # TODO(zcq100): 需要处理验证码的问题
                # 暂时休眠3分钟
                self.log.info("验证码暂时没有处理，建议停三分钟以上再试")
                return

            except Exception as e:
                self.log.error(e)
        return True

    def _get_forum(self, name):
        for f in self._forums:
            if f.name == name:
                return f

    class Net:
        headers = {
            'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
            'Host': "tieba.baidu.com",
#            'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
#            'x-requested-with': "XMLHttpRequest"
        }

        def __init__(self, host, ua=None):
            if isinstance(ua, str) and len(ua):
                self.headers['User-Agent'] = ua
            self.host = host
            self.session = requests.Session()
            self.session.headers = self.headers

        def get(self, path):
            url = self.host+path
            return self.session.get(url)

        def post(self, path, payload):
            url = self.host+path
            return self.session.post(url, data=payload.encode("utf-8"))


class CaptchaException(Exception):
    ...


class SignFailException(Exception):
    ...


def main():
    parser = argparse.ArgumentParser(description="Baidu Tieba Sign")
    parser.add_argument("bduss", type=str, help="tieba bduss cookie")
    parser.add_argument("-v", action="store_true",
                        dest="dbg", help="verbose")
    args = parser.parse_args()
    if args.dbg:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("verbose mode")

    if args.bduss is None:
        parser.print_help()
    else:
        try:
            logging.info("BDUSS=%s"%args.bduss)
            app = Tieba(args.bduss)
            app.auto_sign()
        except KeyboardInterrupt:
            logging.info("Exit..")
            sys.exit()


if __name__ == '__main__':
    main()
