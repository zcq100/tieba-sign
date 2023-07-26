import logging
import sys
import argparse
from tieba.sign import Tieba, SignFailError

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(name)s] [%(levelname)s] %(message)s"
)
_LOG = logging.getLogger(__name__)


if __name__ == "tieba":
    parser = argparse.ArgumentParser(description="Baidu Tieba Sign")
    parser.add_argument("bduss", type=str, help="tieba bduss cookie")
    parser.add_argument("-i", type=int, dest="interval", default=5, help="签到间隔时间")
    parser.add_argument("-v", action="store_true", dest="verbose", help="verbose")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger("urllib3.connectionpool").setLevel(logging.DEBUG)
        logging.debug("verbose mode")

    try:
        app = Tieba(args.bduss)
        app.auto_sign()
    except KeyboardInterrupt:
        _LOG.info("Exit..")
        sys.exit()
    except SignFailError as err:
        _LOG.error(f"登录失败,{err}")
        sys.exit(1)
