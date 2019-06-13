#server address for friend list in function handleSetServer line 238
from Tkinter import *
import socket
import thread

class ChatClient(Frame):
  
    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.initUI()
        self.addr_server_curr_listning_on=None #contains ip and socket as tuple
        self.serverSoc = None
        self.Name=None
        self.serveraddr=None
        self.serverStatus = 0
        self.buffsize = 1024
        self.allClients = {}
        self.ip_to_chatframe = {}
        self.ip_to_chatlabel = {}
        self.frame_to_ip = {}
        self.soc_to_frame = {}
        self.frame_to_soc = {}
        self.frame_status = [0]*4
        self.counter = 0
        self.chatcount = 0
  
    def initUI(self):
        # menubar = Menu(self.root)
        # filemenu = Menu(menubar, tearoff=0)
        # filemenu.add_command(label="New", command=self.donothing)
        # filemenu.add_command(label="Open", command=self.donothing)
        # filemenu.add_command(label="Save", command=self.donothing)
        # filemenu.add_command(label="Save as...", command=self.donothing)
        # filemenu.add_command(label="Close", command=self.donothing)
        # filemenu.add_separator()
        # filemenu.add_command(label="Exit", command=self.root.quit)
        # menubar.add_cascade(label="File", menu=filemenu)
        # self.root.config(menu=menubar)
        self.root.title("Simple P2P Chat Client")
        ScreenSizeX = self.root.winfo_screenwidth()
        ScreenSizeY = self.root.winfo_screenheight()
        self.FrameSizeX  = 1050
        self.FrameSizeY  = 670
        FramePosX   = (ScreenSizeX - self.FrameSizeX)/2
        FramePosY   = (ScreenSizeY - self.FrameSizeY)/2
        self.root.geometry("%sx%s+%s+%s" % (self.FrameSizeX,self.FrameSizeY,FramePosX,FramePosY))
        self.root.resizable(width=False, height=False)

        padX = 10
        padY = 10
        parentFrame = Frame(self.root)
        parentFrame.grid(padx=padX, pady=padY, stick=E+W+N+S)

        ipGroup = Frame(parentFrame)
        setServer=Frame(ipGroup)
        serverLabel = Label(setServer, text="Set Your Server ")
        serverLabel.grid(row=0, column=0)
        serverInput=Frame(setServer)
        nameLabel=Label(serverInput, text="UserName:")
        self.userName = StringVar()
        self.userName.set("Anurag")
        userNameField = Entry(serverInput, width=15, textvariable=self.userName)
        self.nameVar = StringVar()
        self.nameVar.set("SDH")
        nameField = Entry(serverInput, width=10, textvariable=self.nameVar)
        ipLabel=Label(serverInput, text="IP:")
        self.serverIPVar = StringVar()
        self.serverIPVar.set("127.0.0.1")
        serverIPField = Entry(serverInput, width=15, textvariable=self.serverIPVar)
        portLabel=Label(serverInput, text="Port:")
        self.serverPortVar = StringVar()
        self.serverPortVar.set("8090")
        serverPortField = Entry(serverInput, width=5, textvariable=self.serverPortVar)
        serverSetButton = Button(serverInput, text="Set", width=8, command=self.handleSetServer)
        nameLabel.grid(row=0,column=0)
        userNameField.grid(row=0,column=1,padx=5)
        ipLabel.grid(row=0,column=2,padx=5)
        serverIPField.grid(row=0, column=3)
        portLabel.grid(row=0,column=4,padx=5)
        serverPortField.grid(row=0, column=5)
        serverSetButton.grid(row=0, column=6, padx=10)
        # nameField.grid(row=0, column=7)
        serverInput.grid(row=1,column=0)
        setServer.grid(row=0,column=1)

        gap=Frame(ipGroup,width=130)
        gap.grid(row=0,column=2)

        addFriend=Frame(ipGroup)
        addClientLabel = Label(addFriend, text="Add Your Friend")
        addClientLabel.grid(row=0, column=0)
        clientInput=Frame(addFriend)
        clientIpLabel=Label(clientInput, text="IP:")
        self.clientIPVar = StringVar()
        self.clientIPVar.set("127.0.0.1")
        clientIPField = Entry(clientInput, width=15, textvariable=self.clientIPVar)
        clientPortLabel=Label(clientInput, text="Port:")
        self.clientPortVar = StringVar()
        self.clientPortVar.set("8091")
        clientPortField = Entry(clientInput, width=5, textvariable=self.clientPortVar)
        clientSetButton = Button(clientInput, text="Add", width=8, command=self.handleAddClient)
        clientIpLabel.grid(row=0,column=0)
        clientIPField.grid(row=0, column=1,padx=5)
        clientPortLabel.grid(row=0,column=2)
        clientPortField.grid(row=0, column=3,padx=5)
        clientSetButton.grid(row=0, column=4,padx=5)
        clientInput.grid(row=1,column=0)
        addFriend.grid(row=0,column=3)
        ipGroup.grid(row=0, column=0,sticky=E+W+N+S)

        middleframe=Frame(parentFrame)
        readChatGroup = Frame(middleframe)

        self.chatframe1=Frame(readChatGroup,highlightbackground="Black", highlightcolor="Black", highlightthickness=2,bd=0)
        self.chattop1=Frame(self.chatframe1)
        self.chatLabel1 = Label(self.chattop1,width=35)
        self.chatLabel1.grid(row=0,column=1)
        closeChatButton1 = Button(self.chattop1, text="X", width=5,command=self.closeChat1)
        closeChatButton1.grid(row=0,column=2)
        self.chattop1.grid(row=0,column=1)
        scrollbar1 = Scrollbar(self.chatframe1) 
        self.messageread1 =Text(self.chatframe1,width=50,height=15,yscrollcommand=scrollbar1.set, bg ="red", borderwidth=2,state=DISABLED)
        scrollbar1.config(command=self.messageread1.yview)
        self.messageread1.grid(row=1,column=1)
        scrollbar1.grid(row=1,column=2,sticky=(N, S, E, W))
        messagesend1=Frame(self.chatframe1)
        self.chatVar1 = StringVar()
        self.chatField1 = Entry(messagesend1,width=35, textvariable=self.chatVar1)
        self.chatField1.grid(row=0,column=1)
        sendChatButton1 = Button(messagesend1, text="Send", width=5,command=self.handleSendChat1)
        sendChatButton1.grid(row=0,column=2)
        messagesend1.grid(row=2,column=1)
        self.chatframe1.grid(row=0,column=1)

        self.chatframe2=Frame(readChatGroup,highlightbackground="Black", highlightcolor="Black", highlightthickness=2,bd=0)
        self.chattop2=Frame(self.chatframe2)
        self.chatLabel2 = Label(self.chattop2,width=35)
        self.chatLabel2.grid(row=0,column=1)
        closeChatButton2 = Button(self.chattop2, text="X", width=5,command=self.closeChat2)
        closeChatButton2.grid(row=0,column=2)
        self.chattop2.grid(row=0,column=1)
        scrollbar2 = Scrollbar(self.chatframe2) 
        self.messageread2 =Text(self.chatframe2,width=50,height=15,yscrollcommand=scrollbar2.set, bg = "RED", borderwidth=2,state=DISABLED)
        scrollbar2.config(command=self.messageread2.yview)
        self.messageread2.grid(row=1,column=1)
        scrollbar2.grid(row=1,column=2,sticky=(N, S, E, W))
        messagesend2=Frame(self.chatframe2)
        self.chatVar2 = StringVar()
        self.chatField2 = Entry(messagesend2,width=35, textvariable=self.chatVar2)
        self.chatField2.grid(row=0,column=1)
        sendChatButton2 = Button(messagesend2, text="Send", width=5,command=self.handleSendChat2)
        sendChatButton2.grid(row=0,column=2)
        messagesend2.grid(row=2,column=1)
        self.chatframe2.grid(row=0,column=2)

        self.chatframe3=Frame(readChatGroup,highlightbackground="Black", highlightcolor="Black", highlightthickness=2,bd=0)
        self.chattop3=Frame(self.chatframe3)
        self.chatLabel3 = Label(self.chattop3,width=35)
        self.chatLabel3.grid(row=0,column=1)
        closeChatButton3 = Button(self.chattop3, text="X", width=5,command=self.closeChat3)
        closeChatButton3.grid(row=0,column=2)
        self.chattop3.grid(row=0,column=1)
        scrollbar3 = Scrollbar(self.chatframe3) 
        self.messageread3 =Text(self.chatframe3,width=50,height=15,yscrollcommand=scrollbar3.set, bg = "RED", borderwidth=2,state=DISABLED)
        scrollbar3.config(command=self.messageread3.yview)
        self.messageread3.grid(row=1,column=1)
        scrollbar3.grid(row=1,column=2,sticky=(N, S, E, W))
        messagesend3=Frame(self.chatframe3)
        self.chatVar3 = StringVar()
        self.chatField3 = Entry(messagesend3,width=35, textvariable=self.chatVar3)
        self.chatField3.grid(row=0,column=1)
        sendChatButton3 = Button(messagesend3, text="Send", width=5,command=self.handleSendChat3)
        sendChatButton3.grid(row=0,column=2)
        messagesend3.grid(row=2,column=1)
        self.chatframe3.grid(row=1,column=1)

        self.chatframe4=Frame(readChatGroup,highlightbackground="Black", highlightcolor="Black", highlightthickness=2,bd=0)
        self.chattop4=Frame(self.chatframe4)
        self.chatLabel4 = Label(self.chattop4,width=35)
        self.chatLabel4.grid(row=0,column=1)
        closeChatButton4 = Button(self.chattop4, text="X", width=5,command=self.closeChat4)
        closeChatButton4.grid(row=0,column=2)
        self.chattop4.grid(row=0,column=1)
        scrollbar4 = Scrollbar(self.chatframe4) 
        self.messageread4 =Text(self.chatframe4,width=50,height=15,yscrollcommand=scrollbar4.set, bg = "RED", borderwidth=2,state=DISABLED)
        scrollbar4.config(command=self.messageread4.yview)
        self.messageread4.grid(row=1,column=1)
        scrollbar4.grid(row=1,column=2,sticky=(N, S, E, W))
        messagesend4=Frame(self.chatframe4)
        self.chatVar4 = StringVar()
        self.chatField4 = Entry(messagesend4,width=35, textvariable=self.chatVar4)
        self.chatField4.grid(row=0,column=1)
        sendChatButton4 = Button(messagesend4, text="Send", width=5,command=self.handleSendChat4)
        sendChatButton4.grid(row=0,column=2)
        messagesend4.grid(row=2,column=1)
        self.chatframe4.grid(row=1,column=2)

        readChatGroup.grid(row=0, column=1)
        friend_list=Frame(middleframe,highlightbackground="Black", highlightcolor="Black", highlightthickness=2,bd=0)
        self.avaiblity_label = Label(friend_list,width=33,text="Your Server is not Up",highlightbackground="Black", highlightcolor="Black", highlightthickness=2,bd=0)
        self.avaiblity_label.grid(row=0,column=1)
        self.friends = Listbox(friend_list, bg="white", width=33, height=35)
        self.friends.grid(row=1, column=1)
        friend_list.grid(row=0,column=2,padx=10)
        middleframe.grid(row=1,column=0)


        self.statusLabel = Label(parentFrame)

        bottomLabel = Label(parentFrame, text="Created by @raaaaaam")

        self.statusLabel.grid(row=3, column=0)
        bottomLabel.grid(row=4, column=0, pady=10)
    
    def handleSetServer(self):
        print("in handle set server")
        if self.serverSoc != None:
            self.serverSoc.close()
            self.serverSoc = None
            self.serverStatus = 0
            self.Name=None
        serveraddr = (self.serverIPVar.get().replace(' ',''), int(self.serverPortVar.get().replace(' ','')))
        self.addr_server_curr_listning_on=serveraddr
        try:
            self.serverSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serveraddr=serveraddr
            self.serverSoc.bind(serveraddr)
            self.serverSoc.listen(5)
            self.Name=self.userName.get()
            self.setStatus("Server listening on %s:%s" % serveraddr)
            thread.start_new_thread(self.listenClients,())
            self.serverStatus = 1
            self.name = self.nameVar.get().replace(' ','')
            if self.name == '':
                self.name = "%s:%s" % serveraddr               
            try:
                self.friend_list_socket = socket.socket()   
                addre=('10.3.3.10', 33000)       
                self.friend_list_socket.connect(addre) 
                data = self.friend_list_socket.recv(self.buffsize)
                print(data)
                self.friend_list_socket.send(str(serveraddr)+" : "+self.Name)
                self.avaiblity_label.config(text="Connected To server providing List")
                thread.start_new_thread(self.recive_active_users,(self.friend_list_socket,addre))
            except:
                self.avaiblity_label.config(text="Not Connected To server providing List")
                print("server not ava")

     
        except:
            self.setStatus("Error setting up server (Try on some other socket)")
            try:
                self.closeChat1()
            except:
                print("already Closed")    
            try:
                self.closeChat2()
            except:
                print("already Closed")
            try:
                self.closeChat3()
            except:
                print("already Closed")
            try:
                self.closeChat4()
            except:
                print("already Closed")
            self.avaiblity_label.config(text="Your Server is not Up")
            self.friend_list_socket.close()
        
    def listenClients(self):
        print("in listen client")
        while 1:
          clientsoc, clientaddr = self.serverSoc.accept()
          self.setStatus("Client connected from %s:%s" % clientaddr)
          print("server function addClient")
          self.addClient(clientsoc, clientaddr)
          print("server start tread")
          thread.start_new_thread(self.handleClientMessages, (clientsoc, clientaddr))
        self.serverSoc.close()
        print("out listen client")
    def recive_active_users(self,clientsoc,clientaddr):
        print("in recive_active_users")
        while 1:
            try:
                print("trying to get message users")
                data = clientsoc.recv(self.buffsize)
                print(data)
                if not data:
                    print("no data break")
                    break    
                if data[:3]=="ADD":
                    self.friends.insert(END,data[3:])
                if data[:3]=="DEL":
                    index_to_delete=""
                    for s in data[3:]:
                        if s=="-":
                            break
                        else:
                            index_to_delete=index_to_delete+s
                    print(index_to_delete)            
                    self.friends.delete(int(index_to_delete))
            except:
                print("except")
                break
        print("out recive_active_users")          
    def handleAddClient(self):
        print("in handel add client")
        if self.serverStatus == 0:
          self.setStatus("Set server address first")
          return
        if self.chatcount >=4:
          self.setStatus("Cann't Chat with more than 4 peoples simultaneously")
          return
        clientaddr = (self.clientIPVar.get().replace(' ',''), int(self.clientPortVar.get().replace(' ','')))
        if clientaddr==self.addr_server_curr_listning_on:
            self.setStatus("self connection not allowed")
            return     
        if clientaddr in self.ip_to_chatframe.keys() :
            print("already added")
            return
        try:
            clientsoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("going for connection")
            clientsoc.connect(clientaddr)
            print(clientsoc)
            self.setStatus("Connected to client on %s:%s" % clientaddr)
            print("function addClient")
            self.addClient(clientsoc, clientaddr)
            print("starting thread")
            thread.start_new_thread(self.handleClientMessages, (clientsoc, clientaddr))
        except:
            self.setStatus("Error connecting to client")
        print("out handel add client")    

    def handleClientMessages(self, clientsoc, clientaddr):
        print("in handle client message")
        while 1:
          try:
            print("trying to get message")
            data = clientsoc.recv(self.buffsize)
            print(data)
            if not data:
                print("no data break")
                break
            if data=="%!=!^%close":
                break    
            self.addChat(clientaddr, data)
          except:
              break
        self.removeClient(clientsoc, clientaddr)
        clientsoc.close()
        self.setStatus("Client disconnected from %s:%s" % clientaddr)
        print("out handle client message")
    def handleSendChat1(self):
        print("in handle send chat1")
        self.check_msg_and_send(self.messageread1,self.chatField1,0)
    def handleSendChat2(self):
        print("in handle send chat2")
        self.check_msg_and_send(self.messageread2,self.chatField2,1)
    def handleSendChat3(self):
        print("in handle send chat3")
        self.check_msg_and_send(self.messageread3,self.chatField3,2)
    def handleSendChat4(self):
        print("in handle send chat4")
        self.check_msg_and_send(self.messageread4,self.chatField4,3)  
    def addChat(self, client, msg):
        print("in addChat")
        if msg[:12]=="##e!m!a!n@@:":
            print("in if")
            self.ip_to_chatlabel[client].config(text=msg[12:])
        else:
            self.ip_to_chatframe[client].config(state=NORMAL)
            self.ip_to_chatframe[client].insert("end",msg+"\n")
            self.ip_to_chatframe[client].see("end")
            self.ip_to_chatframe[client].config(state=DISABLED) 
    def check_msg_and_send(self,frame,chatbox,soc_index):
        if self.serverStatus == 0:
          self.setStatus("Set server address first")
          return
        print(self.frame_status)  
        if self.frame_status[soc_index] ==0:
            self.setStatus("No client added in this chat frame")
            return 
        msg = chatbox.get()
        chatbox.delete(0, 'end')
        if msg == '':
            return
        frame.config(state=NORMAL)
        frame.insert("end","Me"+": "+msg+"\n")
        frame.see("end")
        frame.config(state=DISABLED)
        self.frame_to_soc[soc_index].send(self.Name+": "+msg)
    def addClient(self, clientsoc, clientaddr):
        print("in add client")
        if clientaddr in self.ip_to_chatframe.keys() :
            return
        self.allClients[clientsoc]=self.counter
        self.counter += 1
        self.assignframe(clientaddr,clientsoc)
        #self.friends.insert(self.counter,"%s:%s" % clientaddr)
    def closeChat1(self):
        # self.messageread1.config(state=NORMAL)
        # self.messageread1.insert("end","msgAnumsgAnumsgAnurafrafrafmsgAnurafmsgAnurafmsgAnurafmsgAnurafmsgAnurafmsgAnurafmsgAnuraf"+"\n")
        # self.messageread1.see("end")
        # self.messageread1.config(state=DISABLED) 
        #self.messageread1.config(bg="Black")
        print("in closeChat1") 
        if self.frame_status[0]==0:
            return   
        clientaddr=self.frame_to_ip[0]
        clientsoc=self.frame_to_soc[0]
        clientsoc.send("%!=!^%close")
        self.setStatus("Client disconnected from me")
        self.removeClient(clientsoc,clientaddr)
        print("out closeChat1")
    def closeChat2(self):
        print("in closeChat2") 
        if self.frame_status[1]==0:
            return   
        clientaddr=self.frame_to_ip[1]
        clientsoc=self.frame_to_soc[1]
        clientsoc.send("%!=!^%close")
        self.setStatus("Client disconnected from me")
        self.removeClient(clientsoc,clientaddr)
        print("out closeChat2")    
    def closeChat3(self):
        print("in closeChat3") 
        if self.frame_status[2]==0:
            return   
        clientaddr=self.frame_to_ip[2]
        clientsoc=self.frame_to_soc[2]
        clientsoc.send("%!=!^%close")
        self.setStatus("Client disconnected from me")
        self.removeClient(clientsoc,clientaddr)
        print("out closeChat3")
    def closeChat4(self):
        print("in closeChat4") 
        if self.frame_status[3]==0:
            return   
        clientaddr=self.frame_to_ip[3]
        clientsoc=self.frame_to_soc[3]
        clientsoc.send("%!=!^%close")
        self.setStatus("Client disconnected from me")
        self.removeClient(clientsoc,clientaddr)
        print("out closeChat4")    
    def removeClient(self, clientsoc, clientaddr):
        print("in removeClient ")
        try:
            clientsoc.close()
            label=self.ip_to_chatlabel[clientaddr]
            frame=self.ip_to_chatframe[clientaddr]
            label.config(text="")
            frame.config(state=NORMAL)
            frame.delete('1.0', END)
            frame.config(state=DISABLED)
            del self.ip_to_chatframe[clientaddr]
            del self.ip_to_chatlabel[clientaddr]
            frame=self.soc_to_frame[clientsoc]
            del self.soc_to_frame[clientsoc]
            del self.frame_to_soc[frame]
            del self.frame_to_ip[frame]
            self.frame_status[frame]=0  
            print(self.allClients)
            del self.allClients[clientsoc]
            print(self.allClients)
            print("out removeClient ")
        except:
            return

    def setStatus(self, msg):
        self.statusLabel.config(text=msg)
        print(msg)
      
    def assignframe(self,clientaddr,clientsoc):
        print("in assign frame")
        print(clientaddr)
        if self.chatcount>=4:
            return 
        i=0
        for i in range(0,len(self.frame_status)):
            if self.frame_status[i]==0:
                break
        self.chatcount += 1
        self.frame_status[i]=1
        self.frame_to_soc[i]=clientsoc
        self.soc_to_frame[clientsoc]=i
        print(i)
        frame_to_assign=self.messageread1 #any random intial value should change to correct value after if 
        label_to_assign=self.chatLabel1
        print(frame_to_assign)
        if i==0:
            frame_to_assign=self.messageread1
            label_to_assign=self.chatLabel1
        if i==1:
            frame_to_assign=self.messageread2
            label_to_assign=self.chatLabel2
        if i==2:
            frame_to_assign=self.messageread3
            label_to_assign=self.chatLabel3
        if i==3:
            frame_to_assign=self.messageread4        
            label_to_assign=self.chatLabel4
        self.ip_to_chatframe[clientaddr]=frame_to_assign
        self.frame_to_ip[i]=clientaddr
        self.ip_to_chatlabel[clientaddr]=label_to_assign
        clientsoc.send("##e!m!a!n@@:"+self.Name+"( "+str(clientaddr[0])+" )")
        print("our assign frame")

def main():  
  root = Tk()
  app = ChatClient(root)
  root.mainloop()  

if __name__ == '__main__':
	main() 
