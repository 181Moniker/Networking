#the current issue is that the outputs are disorganized

#This following program was copied from TechWithTim on YouTube
import socket, threading
from enum import Enum
import random as r
import os

class ServerInfo(Enum):
    HEADER = 64
    FORMAT = 'utf-8'
    PORT = 5050
    SERVER = socket.gethostbyname('192.168.0.212')
    ADDRESS = (SERVER, PORT)
    DISCONNECT_MSG = 'bye bye'
#The header will be 64 bytes. Within those bytes will be
#a number that signifies how many bytes the acutal msg
#with it will be

'''
port = 5050
server = "192.168.0.120"
#The below does the same as the above: it's just automated
server = socekt.gethostbyname(socket.gethostname())
'''
si = ServerInfo
#The INET family is the type of address we'll be looking for
serversoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversoc.bind(si.ADDRESS.value)

'''
The below keeps track of all clients and the leader's command log
when status is "[self]" then each client acts on their own
when status is "[follower]" then each client follows the leader's
messag log

when clusters are formed this will be adpated to account for that
'''

#Variables
message_log, clients, file_message_log = [], [], []
exp_cli, chain_num, status, actives = 0, 0, 0, 0
leader, chained = [], []
fulfilled = False

#Methods
'''Client services'''
def set_client_status(lead, clis, refine=False): #lead = leader, clis = clients
    if refine == False:
        for i in range(len(clis)):
            for j in range(len(clis[i])): #Go inside the nested list
                #print(f"OUTSIDE TEST: {clis[i]}")
                for key in clis[i][j]: #within this layer of the list lies groups of dictionaries
                    sub = clis[i][j][key]
                    #print(f"TEST: {sub}")
                    #The "len(sub) == 4" resets the list to 3 elements as to rid of its old status
                    if lead == "": #if there is no leader then make everyone act on their own
                        if len(sub) == 4: sub.pop()
                        sub.append("self") #add the status of "self"
                    else: #if there is a leader then...
                        if len(sub) == 4: sub.pop()  #remove any previous status

                        for k in range(len(lead)):
                            for l in range(len(lead[k])):
                                #print(f"{lead[k]} and {lead[k][l]} and {lead[k][0]} for {leader} vs {sub}")
                                if lead[k][l] in sub: #if an element in the "leader" list matches with an element in "sub", add the title of "leade>
                                    if "follower" in sub: sub.remove("follower")
                                    sub.append("leader")
                                else: #if an element in the "leader" list doesn't match with an element in "sub", add the title of "follower" to sub
                                    if len(sub) != 4: sub.append("follower")
    else:
        for i in range(len(clis)):
            for j in range(len(clis[i])):
                for key in clis[i][j]:
                    sub = clis[i][j][key]
                    if "self" not in sub:
                        if "follower" or "leader" not in sub:
                            sub.append("follower")
                        if "follower" and "leader" in sub:
                            sub.remove("follower")
    return clis

def rand_leader(clis): #chose random leader per chain
    lead = [] #make list for chosen leads
    cands = [] #make list for candidates

    for i in range(len(clis)):
        cands = clis[i] #candidates are those within the list within the list
        lead.append([cands[r.randrange(0, len(cands))]])
        #The above randomly chooses the index of the leader within this list before move on to the other

    for i in range(len(lead)): #This process grabs the first value in accordance to its key from the chosen index above
        for j in range(len(lead[i])):
            for key in lead[i][j]: #do this to grab the value per key
                sub = lead[i][j][key]
                lead[i][j] = sub[0] #refine the leader to the first element in the list rather than the whole dict
    return lead #return the list of leaders per chain


def activate_chain(chains): #split the clients into however many groups the user asked for
    #print("This is 'activate_chain'") #For testing purposes
    sections = [] #This is the list that will hold each sect of individuals
    #print(f"len of clients: {len(clients)} || chains: {chains}") #for testing purposes
    cli_per_chain = len(clients) // chains
    #The number of people per chain is equal to the quotient of the # of clients and how many chains there will be
    #print(f"People per chain: {cli_per_chain}") #For testing purposes

    if chains > 1: #If there's more than one requested chain...
        new_chain = []; dup_clients = clients
        #'new_chain' serves as a list for each respective chain
        #dup_clients equates to a malleable version of clients

        while len(dup_clients) != 0: #For as long as 'dup_clients' has elements...
            for i in range(cli_per_chain): #for as long as the number of clients per chain hasn't been met...
                rand_indie = dup_clients[r.randrange(0, len(dup_clients))] #randomly choose a client from dup_clients
                dup_clients.remove(rand_indie) #the chosen client will be removed from 'dup_clients' as to prevent duplicate clients
                new_chain.append(rand_indie) #the chosen client will be added into the current 'new chain'
            sections.append(new_chain); new_chain = []
            #add the finished 'new_chain' to 'sections' before clearing it

    else: #If there's one requested chain...
        sections.append(clients) #The only section will consist of the number of clients the server currently has
        if [] in sections: sections.remove([])

    print("Chains:") #showcase how many chains there are
    for i in range(len(sections)): print(f"{i+1}) {sections[i]}")
    return sections

def fix_client(cli):
    print("THIS IS 'FIX_CLIENT'")
    #print(f"MESSAGES LOG: {message_log}")
    global chained
    for key in cli:
        for i in range(len(message_log)):
            for key2 in message_log[i]:
                print(f"INSIDE: {message_log[i][key2]} and {cli[key][0]} vs {key2}")
                if str(cli[key][0]) == str(key2) and ('diagnostic' in message_log[i][key2]):
                        marker = message_log[i][key2].split(":")[3]
                        if marker not in cli[key]:
                            cli[key].insert(1, marker)

def inform_clients(): #inform the clients of their chain and the role they play within it
    global chained
    for i in range(len(chained)):
        for j in range(len(chained[i])):
            for key in chained[i][j]:
                if 'leader' and 'follower' in chained[i][j][key]: chained[i][j][key].remove("follower")
                if len(chained[i][j][key]) != 4: fix_client(chained[i][j])

    chained = set_client_status("", chained, True)
    print("This is 'Inform Clients'")
    print(f"CHAINED: {chained}")
    for i in range(len(chained)):
        print(f"Chain {i+1} Stats:")
        for j in range(len(chained[i])):
            for key in chained[i][j]:
                sub = chained[i][j] #[key]
                print(f"I will message '{key}' for {chained[i]}")
                key.send(f"YOUR CHAIN: {chained[i]}".encode(si.FORMAT.value))
                print("SENT!!!")
                if 'leader' in sub[key]:
                    key.send("CHECK:k_cluster.py".encode(si.FORMAT.value))
                print("CHECK SENT TO LEADER!!!") #; key.close()
                #once again, "key" by itself serves as the connection for "sub[0]" or the simulated IP address
        print()


def client_convo(conn, addr): #set the socket up to listen
    global chained, chain_num
    try:
        print(f"***NEW CONNECTION*** {addr}")
        connected = True
        while connected == True:
            try:
                #The below will decode the msg from bytes to str
                msg_len = conn.recv(si.HEADER.value).decode(si.FORMAT.value)
                if msg_len != None:
                    #print(f"len: {msg_len} | type: {type(msg_len)}")
                    msg_len = int(msg_len)
                    #try:
                    msg = conn.recv(msg_len).decode(si.FORMAT.value)
                    if msg == si.DISCONNECT_MSG.value:
                        connected = False
                    print(f"{addr} says: {msg}")
                    if {addr[0]:msg} not in message_log:
                        message_log.append({addr[0]:msg})

                    if "diagnostic" in msg:
                        #print("adding...")
                        dia_parts = msg.split(":")
                        for i in range(len(clients)):
                            for key in clients[i]:
                                if clients[i][key][0] == dia_parts[1]:
                                    clients[i][key].append(dia_parts[2])
                                    clients[i][key].append(dia_parts[3])
                        print(f"CLIENTS: {clients}")

                    if "CHECKED:" in msg:
                        #print("part 1 pass")
                        file_check = msg.split(":")
                        if file_check[2] == "SUCCESS": pass
                        if file_check[2] == "FAIL":
                            if os.path.isfile(file_check[1]): #replace 'file_check[1]' with own file
                                BUFFER_SIZE = 4096
                                conn.send(f"{file_check[1]}".encode(si.FORMAT.value)) #replace 'si.FORMAT.value' with utf-8
                                with open(file_check[1],"rb") as f: #replace 'file_check[1]' with own file
                                    while True:
                                        bytes_read = f.read(BUFFER_SIZE) #read bytes from file
                                        if not bytes_read: break #break if no more to read
                                        conn.sendall(bytes_read) #send everything #conn is a socket connection
                        print("FILE SENT!!!")
            except OSError: print("DISCONNECTING"); break  #conn.send("TEST CONFIRMATION".encode(si.FORMAT.value))
        conn.close()
    except ValueError: pass

'''Server initialization'''
def init():
    global exp_cli, chain_num
    exp_cli = int(input("# of expected clients: "))
    chain_num = int(input("# of chains (1 at min): "))
    status = 0

def start(): #start the socket server
    global status, actives, exp_cli, chain_num, chained, fulfilled
    serversoc.listen()
    is_on = True
    #print(f"***SERVER LISTENING ON '{si.SERVER.value}'***")
    while True:
        while is_on == True:
            #print(f"actives{actives} and {exp_cli}")

            if actives == exp_cli:
                if status == 0:
                    #fulfilled = True
                    print(flush = True)
                    chained = activate_chain(chain_num)
                    #print(f"MESSAGES: {message_log}")
                    update_client_status(chained)
                    status += 1

            #if status == 2: is_on = False

            #conn is a socket obj and addr is its info
            conn, addr = serversoc.accept()
            clients.append({conn:[addr[0]]})
            #start new thread to handle specific clients
            thread = threading.Thread(target=client_convo, args=(conn, addr))
            #when new conn occurs pass info to "client_convo"
            thread.start(); actives = threading.active_count() - 1
            '''
            if actives == exp_cli:
                if status == 1:
                    chained = activate_chain(chain_num)
                    print(f"TEST ACTIVATION: {chained}")
                    update_client_status(chained)
                    status += 1
                status += 1
            '''
        if is_on == False:
            chained = activate_chain(chain_num)
            update_client_status(chained)
            is_on = True

'''Extra'''
def print_chains(): #print how many chains there are
    print("Chains:")
    for i in range(len(chained)):
        print(f"{i+1}) {chained[i]}")

def update_client_status(chained): #update every client's status
    check_one, check_two = True, True
    update = None
    while check_one == True:
        update = str(input("Update client role? y or n: "))
        if update in ["y", "n", "Y", "N"]: check_one = False
        else: print("***PLEASE ENTER VALID INPUT***")

    while check_two == True:
        if update == "y":
            role = input("leader dynamic (l) || self dynamic (s): ")
            print("Updating client status....")
            if role == "s":
                chained = set_client_status("", chained); inform_clients()
                check_two = False
            elif role == "l":
                leader = rand_leader(chained)
                chained = set_client_status(leader, chained); inform_clients()
                check_two = False
            else: print("***PLEASE ENTER VALID INPUT***")

print("***STARTING SERVER***")
init(); start()
