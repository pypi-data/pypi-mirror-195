from typing import Dict

import logging as log

logSetting: Dict[str, str] = {
    "format": '%(asctime)s : %(levelname)s : %(name)s : %(message)s',
    "datefmt": '%d-%b-%y %H:%M:%S',
    "level": log.INFO,
}
