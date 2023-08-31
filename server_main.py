# -*- coding: utf-8 -*-

import socket
import threading
import time
import server
import pymysql

host = "127.0.0.1"
port = 4000
conn = pymysql.connect(host=host, user="root", password="0000", db="chat_user", charset="utf8")
cur = conn.cursor()

def handle_receive(client_socket, addr, port, num):
    server.server_open(port, num)
    client_socket.close()

def accept_func():
    #IPv4 체계, TCP 타입 소켓 객체를 생성
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #포트를 사용 중 일때 에러를 해결하기 위한 구문
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #ip주소와 port번호를 함께 socket에 바인드 한다.
    #포트의 범위는 1-65535 사이의 숫자를 사용할 수 있다.
    server_socket.bind((host, port))

    #서버가 최대 5개의 클라이언트의 접속을 허용한다.
    server_socket.listen(1024)
    while 1:
        try:
            #클라이언트 함수가 접속하면 새로운 소켓을 반환한다.
            client_socket, addr = server_socket.accept()
            
        except KeyboardInterrupt:
            server_socket.close()
            print("Keyboard interrupt")
            break
        
        data = client_socket.recv(1024)
        data = data.decode('utf-8')
        port_, num_ = data.split(",")
        receive_thread = threading.Thread(target=handle_receive, args=(client_socket, addr,int(port_), int(num_)))
        receive_thread.daemon = True
        receive_thread.start()
        
    receive_thread.join()

def server_open():
    accept_func()


sql = "delete from room"
cur.execute(sql)
conn.commit()
server_open()