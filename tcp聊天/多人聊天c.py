from socket import *
from select import *
from threading import *
from sys import *
from os import *

host = "10.255.1.230"
port = 8765

addr=(host,port)

def connect():  #创建套接字 连接服务器
    s=socket()
    s.connect(addr)
    return s

def lis(s):
    while(1):
        try:
            data=s.recv(2048)
            print(data)
            if data.strip()=='sys:password error':
                print('you have no root!')
                exit(1)
        except error:
            print('socket is disconnected')
            exit(1)

def talk(s):
    while(1):
        try:
            info = input()
            if info.strip() == 'sys.exit':
                s.close()
                print('you have exit\n')
                return
        except Exception as e:
            print('can not input')
            exit()
        try:
            s.send(info.encode("utf-8"))
        except Exception as e:
            print('socket is disconnected...')
            exit()

def main():
    s=connect()
    t1=Thread(target=lis,args=(s,))
    t1.start()
    t2=Thread(target=talk,args=(s,))
    t2.start()


main()



