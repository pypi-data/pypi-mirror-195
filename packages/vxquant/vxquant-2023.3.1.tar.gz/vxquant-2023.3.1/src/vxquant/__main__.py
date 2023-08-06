"""配置文件"""

import json
import argparse
from typing import Union
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor as Executor
from vxsched import vxContext
from vxsched.core import vxscheduler
from vxutils import vxLRUCache, logger, DiskCacheUnit
from vxquant.apis import vxMdAPI, vxTdAPI


_cache_path = Path.home().joinpath(".vxcache").absolute()

_default_config = {
    "params": {},
    "providers": {
        "mdapi": {},
        "tdapi": {},
    },
    "settings": {"modules": [], "cache_dir": _cache_path},
}


def run_quant(
    config_file: Union[str, Path] = "etc/config.json",
    mod_path: Union[str, Path] = "mod",
):
    try:
        with open(config_file, "r") as fp:
            kwargs = json.load(fp)
    except OSError:
        kwargs = {}
    logger.debug(f"加载配置文件: {kwargs},默认值: {_default_config}")
    context = vxContext(_default_config, **kwargs)

    context.memcache = vxLRUCache()
    logger.info(f"初始化内存缓存完成: {context.memcache}")

    cache_dir = context.settings.get("cache_dir", _cache_path)
    DiskCacheUnit.set_cache_params(cache_dir)
    context.settings["cache_dir"] = cache_dir

    try:
        mdapi_settings = context.providers.mdapi.to_dict()
    except AttributeError:
        mdapi_settings = {}
    context.mdapi = vxMdAPI(**mdapi_settings)

    logger.info(f"初始化mdapi 完成.{context.mdapi}")

    try:
        tdapi_settings = context.providers.tdapi.to_dict()
    except AttributeError:
        tdapi_settings = {}
    context.tdapi = vxTdAPI(**tdapi_settings)
    logger.info(f"初始化tdapi 完成{context.tdapi}")
    logger.info(f"通过{config_file}初始化context完成.")

    for mod in context.settings.modules:
        vxscheduler.load_modules(mod)

    vxscheduler.load_modules(mod_path)

    try:
        vxscheduler.start(
            context, executor=Executor(thread_name_prefix="vxquant"), blocking=True
        )
    finally:
        _context = vxContext(_default_config)
        for key in ["params", "settings", "providers"]:
            _context[key] = context[key]

        # _context.save_json(config_file)
        logger.info(f"保存配置文件: {config_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        help="config json file path: etc/config.json",
        default="etc/config.json",
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

    run_quant(config_file=args.config, mod_path=args.mod)
