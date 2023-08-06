import os
import subprocess
import logging
import sys

logger = logging.getLogger("lldbtools")
logger.setLevel(logging.DEBUG)
# fh = logging.FileHandler('')
sh = logging.StreamHandler(sys.stdout)

# logger.addHandler(fh)
logger.addHandler(sh)

scriptPath = os.path.split(os.path.realpath(__file__))[0]
LLDB_SERVER = os.path.join(scriptPath, "lldb-server")


def pushLLDBServer():
    commands = [
        "adb",
        "push",
        LLDB_SERVER,
        "/data/local/tmp"
    ]
    try:
        p = subprocess.run(commands, shell=True, check=True)
    except subprocess.CalledProcessError:
        logger.debug("push lldbtools-server error")


def grantPermission():
    p = subprocess.Popen("adb shell ", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    commands = [
        "su",
        "chmod +x /data/local/tmp/lldbtools-server"
    ]
    try:
        out, err = p.communicate(input="\n".join(commands), timeout=4)  # 不设置超时，就会卡在这里如果你知道为什么请告诉我
    except subprocess.TimeoutExpired:
        p.kill()
        logger.debug("chmod +x lld-server error")


def startLLDBServer():
    p = subprocess.Popen("adb shell ", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    commands = [
        "su",
        "cd /data/local/tmp",
        "ls",
        "nohup ./lldbtools-server p --listen 127.0.0.1:9999 --server & 2>&1 lldbtools.log",
    ]
    try:
        out, err = p.communicate(input="\n".join(commands), timeout=4)  # 不设置超时，就会卡在这里如果你知道为什么请告诉我
    except subprocess.TimeoutExpired:
        p.kill()
        logger.debug("if nothing wrong , lldbtools launched successful.\nor u can commit a issue\n")
        # out,err = p.communicate()
    subprocess.run("adb forward tcp:9999 tcp:9999", shell=True, check=True)


# pushLLDBServer()
# grantPermission()
# startLLDBServer()
