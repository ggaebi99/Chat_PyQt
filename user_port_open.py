import socket

port = 4000


def port_open(open_port):
    host = "127.0.0.1"
    #IPv4 체계, TCP 타입 소켓 객체를 생성
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 지정한 host와 prot를 통해 서버에 접속합니다.
    client_socket.connect((host, port))
    data = "%s,10"%open_port
    print(data)

    client_socket.send(data.encode('utf-8'))
    
    
    