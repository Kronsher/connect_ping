import yaml

import pythonping.executor
from pythonping import ping

with open("device.yml") as f:
    devices = yaml.safe_load(f)

for dev in devices:
    ping_test = ping(dev['host'],  count=3).rtt_avg_ms
    if ping_test < 500:
        show_res ='ONLINE'
    elif ping_test <= 1500:
         show_res ='FREZEE'
    else:
        show_res = 'OFFLINE'

    print(show_res + '-'*10 + dev['host'])