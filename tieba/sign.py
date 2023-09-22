import base64
import json
import logging
import os
import sys
import time
from urllib.parse import urlencode

import requests

_LOG = logging.getLogger(__name__)


class Tieba:
    # 用户贴吧状态
    INFO = "/mo/q/newmoindex"
    # 单独签到的接口
    SIGN_PATH = "/sign/add"
    # 一键签到
    ONKEY_SIGN = "/tbmall/onekeySignin1"

    HOST = "tieba.baidu.com"

    def __init__(self, bduss=None):
        self.http = Http(f"https://{Tieba.HOST}")
        self.http.session.cookies.set("BDUSS", bduss)
        self._tiebas = []
        self.tbs = ""

    def status(self):
        """
        获取签到状态
        """
        endpoint = Tieba.INFO
        data = self.http.make_request(method="GET", endpoint=endpoint)
        forums = data["data"]["like_forum"]
        _LOG.info(f"共关注了{len(forums)}个贴吧")
        for k in forums:
            _LOG.info(
                f"{k['forum_name']}({k['forum_id']}):{'已签' if k['is_sign'] == 1 else '未签'}"
            )
            if k["is_sign"] == 0:
                self._tiebas.append(k["forum_name"])
        self.tbs = data["data"]["itb_tbs"]
        return data

    def onekey_sign(self):
        """
        一键签到
        """
        self.status()
        endpoint = Tieba.ONKEY_SIGN
        payload = {"ie": "utf-8", "tbs": self.tbs}
        data = self.http.make_request(
            method="POST", endpoint=endpoint, data=urlencode(payload)
        )
        # _LOG.info(data)
        if data["no"] == 2280006:
            signed = data["data"]["signedForumAmount"]
            unsigned = data["data"]["unsignedForumAmount"]
            _LOG.info(f"{signed}个贴吧已签到，{unsigned}个贴吧未签到")
        else:
            _LOG.error(data["error"])

    def sign(self, name):
        """
        签到单个贴吧

        name 贴吧的名字
        """
        endpoint = Tieba.SIGN_PATH
        payload = {"ie": "utf-8", "kw": name}
        data = self.http.make_request(
            method="POST", endpoint=endpoint, data=urlencode(payload)
        )
        # _LOG.info(data)
        if data["no"] == 0:
            _LOG.info(f"{name}吧签到成功")
        else:
            _LOG.error(data["error"])

    def auto_sign(self, interval=5):
        # 先调用贴吧的一键签到，可以签到一部分
        self.onekey_sign()
        # 逐一处理未签到的贴吧
        for name in self._tiebas:
            try:
                self.sign(name)
            except Exception as err:
                _LOG.error(err)
            # 慢点来
            time.sleep(interval)

        # 再检查一次签到状态
        self.status()


class Http:
    def __init__(self, base_url=None):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/95.0.4638.54 Safari/537.36",
        }
        self.load_cookie()
        self.cookie_saved = False

    def make_request(
        self,
        method,
        endpoint,
        headers=None,
        params=None,
        cookies=None,
        data=None,
        verify=True,
        **kwargs,
    ) -> dict:
        if headers:
            self.session.headers.update(headers)
        if cookies:
            self.session.cookies.update(cookies)

        url = self.base_url + endpoint
        resp = self.session.request(
            method,
            url=url,
            params=params,
            data=data,
            verify=verify,
            **kwargs,
        )
        resp.raise_for_status()
        try:
            _json = resp.json()
            # 请求成功，保存cookie，下次直接从文件读取
            if _json["no"] == 0:
                if not self.cookie_saved:
                    d = self.session.cookies.get_dict()
                    self.dump_cookie(base64.b64encode(json.dumps(d).encode()))
                    self.cookie_saved = True
            # no 不为0的都有点问题
            if _json["no"] == 1:
                raise SignFailError(_json["error"])
            if _json["no"] == 1010:
                raise TiebaStatuError(f"贴吧状态异常，{data}")
            if _json["no"] == 2150040:
                raise CaptchaError(f"需要验证码,{_json['data']}")
            return _json
        except ValueError as err:
            _LOG.error(err)

    def file_path(self) -> str:
        """
        获取cookie保存的目录
        """
        if sys.platform == "win32":
            base_path = os.environ.get("APPDATA")
        elif sys.platform == "linux":
            base_path = os.path.join(os.environ.get("HOME", "."), ".config")
        elif sys.platform == "darwin":
            base_path = os.path.join(os.environ.get("HOME", "."), ".config")
        else:
            base_path = ""
        path = os.path.join(base_path, "tieba-sign")
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def dump_cookie(self, cookie):
        """
        保存cookie到文件
        """
        file_path = os.path.join(self.file_path(), "cookie")
        with open(file_path, "wb") as f:
            f.write(cookie)
            f.close()
            _LOG.debug(cookie)
            _LOG.debug("写入凭证到%s", file_path)

    def load_cookie(self, file=None):
        """
        从文件中加载cookie
        """
        if not file:
            file = os.path.join(self.file_path(), "cookie")
        if os.path.exists(file):
            with open(file, "rb") as f:
                cookie = f.read()
                f.close()
                try:
                    _cookie = json.loads(base64.b64decode(cookie))
                    _LOG.debug("[+]找到凭证")
                    _LOG.debug("[+]从%s加载凭证", file)
                    _LOG.debug(_cookie)
                    self.session.cookies.update(_cookie)
                except Exception as err:
                    _LOG.error(err)


class CaptchaError(Exception):
    ...


class SignFailError(Exception):
    ...


class TiebaStatuError(Exception):
    ...
