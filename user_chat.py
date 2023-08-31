import socket
import threading
#접속하고 싶은 ip와 port를 입력받는 클라이언트 코드를 작성해보자.
# 접속하고 싶은 포트를 입력한다.
def handle_receive(client_socket, user):
    while 1:
        try:
            data = client_socket.recv(1024)
        except:
            print("연결 끊김")
            break
        data = data.decode('utf-8')
        if "!@#$" in data:
            print("!@#$")
        else:
            if "---- " in data:
                a = data.split("님")
                for i in range(len(a)):
                    a[i] = a[i].replace("---- ", "")
            else:
                a = data.split(":")
                for i in range(len(a)):
                    a[i] = a[i].strip()
            if not user == a[0]:
                print(data)

def handle_send(client_socket):
    while 1:
        data = input()
        client_socket.send(data.encode('utf-8'))
        if data == "/종료":
            break
    client_socket.close()


def user_chatting(port, user):
    host = '127.0.0.1'
    #IPv4 체계, TCP 타입 소켓 객체를 생성
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 지정한 host와 prot를 통해 서버에 접속합니다.
    client_socket.connect((host, port))


    client_socket.send(user.encode('utf-8'))

    receive_thread = threading.Thread(target=handle_receive, args=(client_socket, user))
    receive_thread.daemon = True
    receive_thread.start()

    send_thread = threading.Thread(target=handle_send, args=(client_socket,))
    send_thread.daemon = True
    send_thread.start()

    send_thread.join()
    receive_thread.join()

port = 8507
user = 'testa'
user_chatting(port, user)