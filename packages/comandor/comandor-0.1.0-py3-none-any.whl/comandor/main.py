from tqdm.contrib.logging import logging_redirect_tqdm
from tqdm import tqdm


from comandor.settings import loadSetting, Setting
from comandor.log import log, logSetting
from comandor.models import Action

from typing import Tuple, List

import subprocess as sp
import argparse


def read_args() -> Tuple[str]:
    parser = argparse.ArgumentParser()

    parser.add_argument('-l', "--logfile", type=str,
                        default="", help='where save logfile')
    parser.add_argument('-c', "--config", type=str, default=".comandor",
                        help='where you have config file')
    parser.add_argument('-d', "--debug", action='store_true',
                        required=False, help='run debug mod')

    args = parser.parse_args()
    return (args.logfile, args.config, args.debug)


def newConfig() -> Setting:
    logfile, config, debug = read_args()

    if debug:
        logSetting["level"] = log.DEBUG

    if logfile:
        logSetting["filemode"] = "w"
        logSetting["filename"] = logfile

    log.basicConfig(**logSetting)
    log.info("logger configure!")

    return loadSetting(config)


def errorHandel(func):
    def wrapper(*a, **kw):
        try:
            return func(*a, **kw)

        except sp.CalledProcessError as err:
            log.error(
                f"Status : FAIL Code: {err.returncode} OutPut: {err.output}")
            return 1

        except Exception as e:
            log.error(e)
            return 1

    return wrapper


@errorHandel
def runActions(actions: List[Action]) -> int:
    for action in tqdm(actions):
        log.info(f"Processing {action.action_name}")

        command = f"cd {action.path} && " + \
            " && ".join(action.commands)

        log.debug(f"run this command: {command}")
        outstr = sp.check_output(command, shell=True, stderr=sp.STDOUT,
                                 timeout=action.timeout)
        log.info(outstr.decode())
        log.info(f"Done Process {action.action_name}")

    log.info("Done All Task!")
    return 0


def main() -> int:
    setting: Setting = newConfig()

    log.info(f"start commander -> {setting.name}")

    with logging_redirect_tqdm():
        return runActions(setting.actions)


if __name__ == "__main__":
    exit(main())
