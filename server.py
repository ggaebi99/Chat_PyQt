# -*- coding: utf-8 -*-

import socket
import threading
import time

host = "127.0.0.1"
user_list = {}
notice_flag = 0

def msg_func(msg, port):
    print(msg)
    for con in user_list.values():
        if port == int(con.getsockname()[1]):
            try:
                con.send(msg.encode('utf-8'))
            except:
                print("연결이 비 정상적으로 종료된 소켓 발견")
                
def msg_user_list(port):
    msg = "!@#$"
    for i in user_list.keys():
        if port == int(user_list[i].getsockname()[1]):
            msg = msg +","+ i
            print(msg)
    for con in user_list.values():
        if port == int(con.getsockname()[1]):
            # msg = msg + 
            try:
                con.send(msg.encode('utf-8'))
            except:
                print("연결이 비 정상적으로 종료된 소켓 발견")
    
def handle_receive(client_socket, addr, user, port):
    msg = "---- %s님이 들어오셨습니다. ----"%user
    msg_func(msg, port)
    msg_user_list(port)
    while 1:
        data = client_socket.recv(1024)
        string = data.decode('utf-8')

        if "/종료" in string:
            msg = "---- %s님이 나가셨습니다. ----"%user
            #유저 목록에서 방금 종료한 유저의 정보를 삭제
            del user_list[user]
            msg_func(msg, port)
            msg_user_list(port)
            break
        string = "%s : %s"%(user, string)
        msg_func(string, port)
    client_socket.close()

def accept_func(port, num):
    #IPv4 체계, TCP 타입 소켓 객체를 생성
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #포트를 사용 중 일때 에러를 해결하기 위한 구문
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #ip주소와 port번호를 함께 socket에 바인드 한다.
    #포트의 범위는 1-65535 사이의 숫자를 사용할 수 있다.
    server_socket.bind((host, port))

    #서버가 최대 5개의 클라이언트의 접속을 허용한다.
    server_socket.listen(num)

    while 1:
        try:
            #클라이언트 함수가 접속하면 새로운 소켓을 반환한다.
            client_socket, addr = server_socket.accept()
        except KeyboardInterrupt:
            for user, con in user_list:
                con.close()
            server_socket.close()
            print("Keyboard interrupt")
            break
        user = client_socket.recv(1024).decode('utf-8')
        user_list[user] = client_socket
        
        receive_thread = threading.Thread(target=handle_receive, args=(client_socket, addr,user, port))
        receive_thread.daemon = True
        receive_thread.start()

def server_open(port, num):
    accept_func(port, num)
