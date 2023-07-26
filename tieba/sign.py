import logging
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
    # 我喜欢的贴吧
    TIEBA_LIST = "/i/i/forum?&pn=3"
    MY_LIKE = "/f/like/mylike?v=1690371328754&pn=2"
    HOST = "tieba.baidu.com"

    def __init__(self, bduss=None):
        self.http = Http(f"https://{Tieba.HOST}")
        self.http.session.cookies.set("BDUSS", bduss)
        self._tiebas = []

    def status(self):
        """
        获取签到状态
        """
        endpoint = Tieba.INFO
        data = self.http.make_request(method="GET", endpoint=endpoint)
        forums = data["data"]["like_forum"]
        _LOG.info(f"共关注了{len(forums)}个贴吧")
        for k in data["data"]["like_forum"]:
            _LOG.info(
                f"{k['forum_name']}({k['forum_id']}):{'已签' if k['is_sign'] == 1 else '未签'}"
            )
            if k["is_sign"] == 0:
                self._tiebas.append(k["forum_name"])
        return data

    def onekey_sign(self):
        """
        一键签到
        """
        endpoint = Tieba.ONKEY_SIGN
        payload = {"ie": "utf-8", "tbs": "5c887f8452a9ebec1690371137"}
        data = self.http.make_request(
            method="POST", endpoint=endpoint, data=urlencode(payload)
        )
        # _LOG.info(data)
        if data["no"] == 2280006:
            signed = data["data"]["signedForumAmount"]
            unsigned = data["data"]["unsignedForumAmount"]
            _LOG.info(f"{signed}个贴吧已签到，{unsigned}个贴吧未签到")

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
        # 检查签到的状态，如果还有未签到的贴吧，加入清单
        self.status()
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
        self.headers = {
            "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
        }
        self.session = requests.Session()

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
            self.headers.update(headers)
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
            # no 不为0的都有点问题
            if _json["no"] == 1:
                raise SignFailError(_json["error"])
            if _json["no"] == 1010:
                raise TiebaStatuError(f"贴吧状态异常，{data}")
            return _json
        except ValueError as err:
            _LOG.error(err)


class CaptchaError(Exception):
    ...


class SignFailError(Exception):
    ...


class TiebaStatuError(Exception):
    ...
