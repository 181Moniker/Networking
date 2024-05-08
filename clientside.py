'''
Things to note for positioning:
the yellow swaure in the middle is two by two meters long. Convert to feet 
to get x and y coords and send to thread
iotcar4 at 192.168.0.244
iotcar5 at 192.168.0.240
iotcar6 at 192.168.0.161
'''
import socket
from enum import Enum
from subprocess import check_output
import os
import main_drive, check_messages

class ClientConnInfo(Enum):
    HEADER = 64
    PORT = 5050
    SERVER = socket.gethostbyname('192.168.0.212')
    FORMAT = 'utf-8'
    DISCONNECT_MSG = 'bye bye'
    ADDRESS = (SERVER, PORT)
    FILE_BUFF_SIZE = 4096
    SELF_USER = os.popen("whoami").read().strip("\n")

    def find_self():
        self = str(check_output(['hostname','-I']))
        self = self.split("'")[1]; self = self.split(" ")[0]
        return self

cci = ClientConnInfo
clientsoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsoc.connect(cci.ADDRESS.value)
chain_dct = {}
file_msg = ""
escape = False
is_leader = False
ssh_list = []

def send(msg):
    global file_msg, escape, chain_dct
    mess = msg.encode(cci.FORMAT.value)
    msg_len = len(mess)
    send_len = str(msg_len).encode(cci.FORMAT.value)
    send_len += b' ' * (cci.HEADER.value - len(send_len))
    clientsoc.send(send_len); clientsoc.send(mess)
    if escape == False:
        recved_msg = clientsoc.recv(2048).decode(cci.FORMAT.value)
        print("RECEIVED MESSAGE | ", recved_msg)
        if "CHAIN" in recved_msg:
            chain_str = recved_msg
            chain_lst = chain_str.split("{")
            chain = {}
            for i in range(len(chain_lst)):
                chain_lst[i] = chain_lst[i].split("}")[0]; key_split = chain_lst[i].split(": ")[0]
                back_split = chain_lst[i].split(": ")[1].strip("[").strip("]").split(", '")

                if len(back_split) > 1:
                    back_split = [back_split[j].strip("'") for j in range(len(back_split))]
                    chain[key_split]=back_split
            print("REV CHAIN:")
            for key, value in chain.items():
                print(f"{key} for {value}\n")
            chain_dct = chain

        if "CHECK" in recved_msg:
            file_msg = recved_msg.split(":")[1]
            if os.path.isfile(f'../Desktop/{file_msg}'):
                send(f"CHECKED:{file_msg}:SUCCESS")
            else: send(f"CHECKED:{file_msg}:FAIL")

        if recved_msg == file_msg and file_msg != "":
            with open(file_msg, 'wb') as f:
                while True:
                    bytes_read = clientsoc.recv(cci.FILE_BUFF_SIZE.value)
                    if not bytes_read:break
                    f.write(bytes_read)
        escape = True

def send_cmd_to_followers(lttr, spec_ip=""):
    for i in range(len(ssh_list)):
        if spec_ip != "" and spec_ip == ssh_list[i]:
            ssh_list[i].run(f'cd Desktop; touch simp_mess.txt; echo {lttr} > simp_mess.txt')
        else:
            ssh_list[i].run(f'cd Desktop; touch simp_mess.txt; echo {lttr} > simp_mess.txt')


send(f"diagnostic:{cci.find_self()}:{cci.SELF_USER.value}:R3")
send("Hello there from 159!")
print("CHAIN:", chain_dct)

for key, value in chain_dct.items():
    if value[0] == cci.find_self() and value[3] == "leader": is_leader = True

if is_leader == True:
    for key, value in chain_dct.items():
        ip = value[0]; user = value[1]
        if ip != cci.find_self():
            ssh_list.append((ip, user))

    print("SSH LIST:", ssh_list)

#ssh_list = [('192.168.0.120', 'iotcar'), ('192.168.0.168', 'iotcar2'), ('192.168.0.159', 'iotcar3')]
counter = 0
#read its status and position so it can update clustering and send info to sink
'''
SIM:
ip1:active:(x,y):follow
ip2:inactive:(x,y):self
ip3:inactive:(x,y):self
ip4:active:(x,y):self:found 'best_path'
'''
positions = []
while True:
    if is_leader == True:
        if counter == 0:
            main_drive.run_drive(ssh_list)
            counter+=1
        if counter == 1:
            room_message = ""
            send_cmd_to_followers("self")
            with open("room.txt", "r") as f:
                room_message = f.read().split(":")
                positions.append(room_message[2])
                if room_message[1] == "done":
                    counter+=1
        #break
    else:
        check_messages.check_noti()
    #have something that checks the outside conditions of things to 
    #see if you need to switch operations up or end them altogether

while True:
    esacape = False
    ipt = input("USER: ")
    if ipt != "q":
        send(ipt)
    else:
        send(cci.DISCONNNECT_MSG.value)
    print(">>", ipt,"\n")
