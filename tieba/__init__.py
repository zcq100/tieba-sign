import logging
import sys
import argparse
from tieba.sign import Tieba

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
_LOG = logging.getLogger(__name__)


if __name__ == "tieba":
    parser = argparse.ArgumentParser(description="Baidu Tieba Sign")
    parser.add_argument("bduss", type=str, help="tieba bduss cookie")
    parser.add_argument("-i", type=int, dest="interval",default=5, help="签到间隔时间")
    parser.add_argument("-v", action="store_true", dest="dbg", help="verbose")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    
    if args.dbg:
        logging.getLogger("urllib3.connectionpool").setLevel(logging.DEBUG)
        logging.debug("verbose mode")

    if args.bduss is None:
        parser.print_help()

    try:
        app = Tieba(args.bduss)
        app.auto_sign()
    except KeyboardInterrupt:
        _LOG.info("Exit..")
        sys.exit()
