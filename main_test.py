import datetime
import telnetlib
import time
import os
import yaml
import socket
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat

# Функция для форматирования строки и перевод ее в байтовую
def to_bytes(line):
    return f"{line}\n".encode("utf-8")

# Изменение цвета
def out_green(text):
    print("\033[32m {}" .format(text))
    print("\033[0m")

def out_red(text1):
    print("\033[31m {}" .format(text1))
    print("\033[0m")

def out_blue(text2):
    print("\033[34m {}" .format(text2))
    print("\033[0m")



# Подключение к устройству и отправка команды
def connect_and_set_command(device, command):
    ip = device["host"]
    name = device["device"]
    try:
        with telnetlib.Telnet(ip, timeout=20) as telnet:
            login = ""
            telnet.read_until(b'UserName:')
            # login += str(telnet.read_until(b'UserName:'))
            # print(login)
            telnet.write(b'username\n')
            telnet.write(b'password\n')
            telnet.read_until(b'#')
            # login += str(telnet.read_until(b'#'))
            # print(login)
            telnet.write(to_bytes(command))
            telnet.write(b'a\n')
            time.sleep(40)
            info = telnet.read_very_eager().decode('ascii')
            #print(info)
            telnet.close()
            return info

    except socket.timeout:
        print(out_red(f"Timeout при подключении к {name} {ip}"))



def make_folder():
    date_1 = datetime.datetime.now()
    date = str(date_1).split()[0]
    if not os.path.isdir(f"logs/{date}/"):
        os.mkdir(f"logs/{date}")
    return date

folder = make_folder()


# def write_config(device, info):
#     global folder
#     with open(f'logs/{folder}/{device["host"]}.txt', 'w', encoding="UTF-8") as f:
#         data = datetime.datetime.now()
#         f.writelines(f"{info}\n{data}")






if __name__ == "__main__":
    make_folder()
    with open("device.yml") as f:
         devices = yaml.safe_load(f)



    with ThreadPoolExecutor(max_workers=10) as executor:
        result = executor.map(connect_and_set_command, devices, repeat("show config current_config\n"))
        for dev, output in zip(devices, result):
            # write_config(devices, output)
            with open(f'logs/{folder}/{dev["host"]}.txt', 'w', encoding="UTF-8") as f:
                data = datetime.datetime.now()
                f.writelines(f"{output}\n{data}")

