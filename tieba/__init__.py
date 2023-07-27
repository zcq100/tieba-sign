import logging
import sys
import argparse

from tieba.sign import Tieba, SignFailError

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(name)s] [%(levelname)s] %(message)s"
)
_LOG = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="百度贴吧批量签到")
    parser.add_argument("bduss", type=str, nargs="?", help="贴吧bduss的cookie值")
    parser.add_argument(
        "-i", type=int, dest="interval", default=5, help="签到间隔时间，批量签到避免弹验证码，默认5秒"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", action="store_true", dest="verbose", help="详细模式，显示更多运行信息")
    group.add_argument("-q", action="store_true", dest="quiet", help="安静模式，不显示运行信息")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger(__name__).setLevel(logging.DEBUG)
        logging.getLogger("urllib3.connectionpool").setLevel(logging.DEBUG)
        logging.debug("详细模式..")
    
    if args.quiet:
        logging.getLogger().setLevel(logging.CRITICAL)

    try:
        app = Tieba(args.bduss)
        app.auto_sign(args.interval)
    except KeyboardInterrupt:
        _LOG.info("退出..")
        sys.exit()
    except SignFailError as err:
        _LOG.critical(f"登录失败,{err}")
        sys.exit(1)


if __name__ == "tieba":
    main()
    sys.exit()
