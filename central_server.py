######server IP on line 10 and Port On Line 11
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import thread
addresses = {}
clientAdd_to_data = {}
clients=[]

#HOST = ''
HOST = '10.3.3.10' #ip of the server hosting 
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)
def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
    	print("in while")
        clientsoc, client_address = SERVER.accept()
        print("request acceptedd")
        print("%s:%s has connected." % client_address)
        clientsoc.send("Greetings from Server!! What is Your Name?")
        print(clientsoc)
        curr_data = clientsoc.recv(BUFSIZ)
        print(curr_data)
        for key in clientAdd_to_data.keys():
        	print("sending user info")
        	clientsoc.send("ADD"+str(clientAdd_to_data[key]))
        clientAdd_to_data[client_address]=str(curr_data)
        clients.append(clientsoc)
        for socs in clients:
        	print("sending user info")
        	socs.send("ADD"+str(curr_data))
        thread.start_new_thread(handleClient, (clientsoc, client_address))
        		
def handleClient(clientsoc, clientaddr):
	print("in handle client")
	while 1:
		try:
			print("trying to get message")
			data = clientsoc.recv(BUFSIZ)
			print(data)
			if not data:
			    print("no data break")
			    break
		except:
			break
	print("discon: "+str(clientaddr))
	index_to_remove=clients.index(clientsoc)
	del clients[index_to_remove]
	for socs in clients:
		print("sending closing info")
		socs.send("DEL"+str(index_to_remove)+"-"+str(clientAdd_to_data[clientaddr]))
	del clientAdd_to_data[clientaddr]
	clientsoc.close()


if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.daemon = True
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
SERVER.close()