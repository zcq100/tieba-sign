import os
import sys
import logging
import unittest
from unittest.mock import MagicMock
from tieba.sign import Tieba
from dotenv import load_dotenv

logging.getLogger().setLevel(logging.DEBUG)

class TestTieba(unittest.TestCase):
    def setUp(self):
        load_dotenv(".env")
        BDUSS = os.environ.get("BDUSS")
        self.tieba = Tieba(BDUSS)
        # self.tieba.http.session.proxies = {
        #     "http": "http://10.0.1.115:8888",
        #     "https": "https://10.0.1.115:8888"
        # }
        # self.tieba.http = MagicMock()

    def test_get_status(self):
        # self.tieba.http.make_request.return_value = {"status": "ok"}
        self.tieba.status()

    def test_onekey_sign(self):
        self.tieba.onekey_sign()

    def test_sign(self):
        self.tieba.sign("阿尔比恩")

    def test_auto_sign(self):
        self.tieba.auto_sign()

    def test_file_path(self):
        # 测试Windows平台下的情况
        os.environ["APPDATA"] = "test_APPDATA"
        sys.platform = "win32"
        self.assertEqual(self.tieba.http.file_path(), "test_APPDATA/tieba-sign")

        # 测试Linux平台下的情况
        os.environ["HOME"] = "test_HOME"
        sys.platform = "linux"
        self.assertEqual(self.tieba.http.file_path(), "test_HOME/.config/tieba-sign")

        # 测试macOS平台下的情况
        sys.platform = "darwin"
        self.assertEqual(self.tieba.http.file_path(), "test_HOME/.config/tieba-sign")

        # 测试其他平台下的情况
        sys.platform = "other"
        self.assertEqual(self.tieba.http.file_path(), "tieba-sign")
        
    def test_cookie_dump(self):
        self.tieba.http.dump_cookie(b"test")
        with open(self.tieba.http.file_path() + "/cookie", "rb") as f:
            self.assertEqual(f.read(), b"test")
