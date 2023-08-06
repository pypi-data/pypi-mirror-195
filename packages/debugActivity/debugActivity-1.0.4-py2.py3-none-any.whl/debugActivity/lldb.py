import subprocess
p = subprocess.Popen("adb shell " , shell=True , stdin=subprocess.PIPE , stdout=subprocess.PIPE , text=True)

commands = [
    "su" ,
    "cd /data/local/tmp" ,
    "ls",
    "nohup ./lldbtools-server p --listen 127.0.0.1:9999 --server & " ,
]

try:
    out , err = p.communicate(input="\n".join(commands)  , timeout=4) # 不设置超时，就会卡在这里如果你知道为什么请告诉我
except subprocess.TimeoutExpired:
    p.kill()
    print("if nothing wrong , lldbtools launched successful")
    # out,err = p.communicate()

print(err)
