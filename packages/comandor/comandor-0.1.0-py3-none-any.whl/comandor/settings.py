from pydantic import ValidationError

from comandor.models import Setting
from comandor.log import log

import json
import os


def loadSetting(file: str = ".comandor") -> Setting:
    log.debug("run load setting")

    if not os.path.exists(file):
        raise Exception("Config file not found!")

    setting: Setting = None
    with open(file, "r") as f:
        try:
            log.debug("read .command file from ./")
            log.debug("decode json to dict")
            op = json.load(f)

            log.debug("match setting with models")
            setting = Setting(**op)

        except ValidationError as e:
            log.error(e)
            raise

        except json.JSONDecodeError as e:
            log.error(e)
            raise

    log.debug("load Setting complete, return setting")
    return setting
