from socket import *
from time import *
from select import *

host = '10.255.1.230'       #服务器ip，根据需要改写
port = 8765
addr=(host,8765)    #地址
inputs=[]    #套接字列表
names={}     #用户昵称列表


def who_in_room(w):  #返回当前聊天室成员名单
    name_list=[]
    for i in w:
        name_list.append(w[i])
    return name_list
def connect():
    print("runing...")
    s=socket()
    s.bind(addr)
    s.listen(5)
    return s

def new(s): #新连接客户端处理
    client,addr=s.accept()
    print('a user try to connect')
    client.send('please input your password:'.encode("utf-8"))
    password=client.recv(1024).decode("utf-8")#接收密码
    if password !='123':
        client.send('sys:password error'.encode("utf-8"))
        print('%s connect falied!' %(str(addr)))
        time.sleep(1)
        client.close()
    else:
        print('%s connect successed!' %str(addr))
        client.send("please input your nick:".encode("utf-8"))
        nick=client.recv(1024).decode("utf-8")
        inputs.append(client)
        names[client]=nick
        nameList=('%d people in talking room,these are %s'%(len(names),who_in_room(names)))
        print(nameList)
        client.send(nameList.encode("utf-8"))
        for other in inputs:
            if other!=s and other!=client:
                other.send(("welcome!  "+
                strftime('%Y-%m-%d %H:%M:%S',localtime())).encode("utf-8"))

def server_run():
    s=connect()
    inputs.append(s)
    while(1):
        r,w,e=select(inputs,[],[])
        for temp in r:
            if temp == s:
                new(s)
            else:
                disconnect=False
                try:
                    data=temp.recv(1024).decode("utf-8")
                    if data.strip()=='show list':
                        nameList="%d people in talking room,these are %s"%(len(names),who_in_room(names))
                        temp.send(nameList.encode("utf-8"))
                        break
                    data=names[temp]+' say:'+data
                except error:
                    data=names[temp]+' say:'+'leave the room'
                    disconnect=True
                if(disconnect):
                    inputs.remove(temp)
                    print(data)
                    for other in inputs:
                        if other!=s:
                            other.send(data.encode("utf-8"))
                    del names[temp]
                else:
                    print(data)
                    for other in inputs:
                        if other!=s:
                            other.send(data.encode("utf-8"))



server_run()     #程序入口
