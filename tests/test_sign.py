import os
import unittest
from unittest.mock import MagicMock
from tieba.sign import Tieba
from dotenv import load_dotenv


class TestTieba(unittest.TestCase):
    def setUp(self):
        load_dotenv(".env")
        BDUSS = os.environ.get("BDUSS")
        self.tieba = Tieba(BDUSS)
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
