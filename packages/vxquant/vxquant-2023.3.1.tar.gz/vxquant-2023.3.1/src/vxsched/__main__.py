"""vxsched 主函数"""
import argparse
from vxutils import logger
from vxsched import vxscheduler

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c",
        "--config",
        help="config json file path: etc/config.json",
        default="config.json",
        type=str,
    )
    parser.add_argument(
        "-m", "--mod", help="module directory path : mod/ ", default="mod/", type=str
    )
    parser.add_argument(
        "-v", "--verbose", help="debug 模式", action="store_true", default=False
    )
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel("DEBUG")

    vxscheduler.server_forever(config=args.config, mod=args.mod)
