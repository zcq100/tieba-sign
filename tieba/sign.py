import argparse
import re
import requests
import logging
import time
from urllib.parse import quote

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
}

# REG_1=r'f\?kw=([\d\w\%]*)"|tbs="([\d\w]*)"'
REG_1 = r'<tr>.*?f\?kw=([\d\w\%]*)" title="(.*?)".*?balvid="(\d*)".*?<\/tr>'
REG_TOTAL = r'&pn=(\d+)">尾页'
URL_FAV = "http://tieba.baidu.com/f/like/mylike?pn="
URL_SIGN = "https://tieba.baidu.com/sign/add"


class Tieba:
    def __init__(self, cookie=None, filename=None):
        self.filename = filename
        self.bars = []
        if cookie is not None:
            headers["Cookie"] = cookie

    def get_bars(self):
        """
        获取关注的贴吧列表
        """
        num = 1
        i = 1
        while i <= num:
            url = URL_FAV+str(num)
            resp = requests.get(url, headers=headers)
            i += 1
            if resp.status_code == 200:
                # 获取最大页数
                if num == 1:
                    matchs2 = re.search(REG_TOTAL, resp.text, re.MULTILINE)
                    if matchs2 is not None:
                        num = int(matchs2.group(1))
                        logging.debug(f"total:{num}")

                # 匹配关注的贴吧
                matchs = re.finditer(REG_1, resp.text, re.MULTILINE)
                for m in matchs:
                    b = [m.group(1).strip(), m.group(
                        2).strip(), m.group(3).strip()]
                    self.bars.append(b)
                    logging.debug(f"{b}")

            else:
                logging.debug("请求失败")
        logging.info(f"获取到关注贴吧:{len(self.bars)}个")

    def dumps(self, file_name="list.txt"):
        """
        把贴吧列表保存到文件
        - file_name 文件名
        """
        _list = ""
        with open(file_name, "w", encoding="utf-8") as f:
            for i in self.bars:
                f.writelines(f"{i[1]},{i[2]},{i[0]}\n")
                _list += f"{i[1]},"
            logging.info(f"贴吧列表保存到{file_name}..")
        return _list

    def sign(self, name=None, tbs=None, encode_name=None):
        """
        贴吧签到
        - name 吧名
        - tbs 贴吧编号
        - encode_name urlencode后的名称
        """
        if encode_name is None:
            if name is None:
                raise ValueError("贴吧名称不能为空")
            encode_name = quote(name)
        headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        data = {
            "ie": "utf-8", "kw": encode_name, "tbs": tbs}
        logging.debug(f"----------\n{data}")
        resp = requests.post(URL_SIGN, headers=headers, data=data)
        logging.debug(resp.text)
        if resp.status_code == 200:
            j = resp.json()
            code = j.get("no")
            error = j.get("error")
            if code == 0:
                logging.info(f"{name},{encode_name},{tbs}:签到成功..")
            else:
                logging.info(f"{name},{encode_name},{tbs}:{error}")

    def batch_sign(self, _time=0):
        """
        批量签到
        - _time 签到间隔时间，默认为0
        """
        for i in self.bars:
            self.sign(name=i[1], encode_name=i[0], tbs=i[2])
            time.sleep(_time)


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cookie", help="Cookies")
    parser.add_argument("-f", "--file", help="cookies file")
    parser.add_argument("-t", "--time", help="sleep time")
    parser.add_argument("-d", "--dump", action="store_true",
                        help="dump list to file")
    parser.add_argument("-v",dest="verbose",action="store_true",help="verbose mode")
    args = parser.parse_args()
    if args.cookie is None and args.file is None:
        parser.print_usage()
        return 
    
    if args.cookie:
        cookie = args.cookie

    if args.file:
        with open(args.files, "r", encoding="utf-8") as f:
            cookie = f.read()
            
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
        
    tieba = Tieba(cookie)
    tieba.get_bars()
    if args.dump:
        tieba.dumps()
    _time = 1
    if args.time:
        _time = args.time
    tieba.batch_sign(_time)


if __name__ == "__main__":
    main()
