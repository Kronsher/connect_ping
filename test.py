import telnetlib
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor

ip = ("172.21.0.66", "172.21.0.75")

def connect(ip):
    try:
        with telnetlib.Telnet(ip, timeout=20) as telnet:
            login = ""
            login += str(telnet.read_until(b'UserName:'))
            print(login)
            telnet.write(b'username\n')
            telnet.write(b'password\n')
            login += str(telnet.read_until(b'#'))
            print(login)
            telnet.write(b'show boot_file\n')
            telnet.write(b'a\n')
            time.sleep(5)
            device = telnet.read_very_eager().decode("ascii")
            print(device)
            return device
    except:
        pass


#connect("172.21.0.66")
with ThreadPoolExecutor(max_workers=3) as executor:
    device = executor.map(connect, ip, timeout=10)
    #print(device)

