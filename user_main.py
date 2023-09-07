import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal
import pymysql
import win32api
import random
import user_port_open
import socket
import threading

SERVER_IP = "127.0.0.1"
port = 0

conn = pymysql.connect(host=SERVER_IP, user="root", password="0000", db="chat_user", charset="utf8")
cur = conn.cursor()
        
def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form_login = resource_path('ui/user_login.ui')
form_loginwindow = uic.loadUiType(form_login)[0]

form_usermain = resource_path('ui/user_main.ui')
form_usermainwindow = uic.loadUiType(form_usermain)[0]

form_makeroom = resource_path('ui/user_room_make.ui')
form_makeroomwindow = uic.loadUiType(form_makeroom)[0]

form_roompasswordcheck = resource_path('ui/room_passwd.ui')
form_roompasswordcheckwindow = uic.loadUiType(form_roompasswordcheck)[0]

form_chatroom = resource_path('ui/chat_room.ui')
form_chatroomwindow = uic.loadUiType(form_chatroom)[0]



class LoginWindow(QMainWindow, form_loginwindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnLogin.clicked.connect(self.btn_login_to_main)
        self.labelPW.setEchoMode(QLineEdit.Password)
        
    def btn_login_to_main(self):   
        
        sql = "select * from user where id = %s and passwd = %s"
        vals = (self.labelID.text(), self.labelPW.text())
        if(cur.execute(sql, vals)):
            global user_id
            user_id = self.labelID.text()
            self.main = Mainwindow()
            self.main.show()
            self.close()
        else:
            win32api.MessageBox(0, "user정보가 없습니다.", "로그인 실패", 16)

class Mainwindow(QMainWindow, form_usermainwindow):

    def __init__(self):
        super().__init__()
        
        self.setupUi(self)
        sql = "SELECT * FROM room"
        cur.execute(sql)
        result = cur.fetchall()
        for i in range(len(result)):
            self.room_list.addItem(result[i][0])
        self.label_userID.setText(user_id + "님")
        self.btnMakeroom.clicked.connect(self.btn_login_to_main)
        self.action_logout.triggered.connect(self.logout)
        self.action_exit.triggered.connect(self.exit_action)
        self.room_list.itemDoubleClicked.connect(self.item_changed)
        self.btn_saero.clicked.connect(self.saerogochim)
        
        
    def btn_login_to_main(self):    
        self.makeroom = Makeroomwindow()
        self.makeroom.show()
        self.close()
        
    def logout(self):
        self.loginwindow = LoginWindow()
        self.loginwindow.show()
        self.close()
    
    def item_changed(self, item):
        global port
        room_name = item.text()
        sql = "select * from room where name = %s"
        vals = (room_name)
        cur.execute(sql, vals)
        result = cur.fetchall()
        if(result[0][5]==result[0][1]):
            win32api.MessageBox(0, "방이 꽉 찼습니다.", "정원초과", 16)
            return 0
        if(result[0][2]):
            self.room_pwcheck = room_password_check()
            self.room_pwcheck.show()
            self.room_pwcheck.exec()
            sql = "select * from room where name = %s and password = %s"
            vals = (room_name, self.room_pwcheck.password)
            if(cur.execute(sql, vals)):
                # 창 바꾸기
                print(result[0][4])
                port = result[0][4]
                sql = "update room set people_count = %s where name = %s"
                vals = (result[0][5]+1, room_name)
                cur.execute(sql, vals)
                conn.commit()
                self.chatroom = Chatroomwindow()
                self.chatroom.show()
                self.close()
            else:
                win32api.MessageBox(0, "비밀번호가 틀립니다.", "비밀번호 오류", 16)
        
        else:
        # sql = "select * from room where name = %s and password = %s"
        # vals = (room_name, temp_pass)
        # if(cur.execute(sql, vals)):
            # 이부분 창 바꾸기
            print(result[0][4])
            port = result[0][4]
            sql = "update room set people_count = %s where name = %s"
            vals = (result[0][5]+1, room_name)
            cur.execute(sql, vals)
            conn.commit()
            self.chatroom = Chatroomwindow()
            self.chatroom.show()
            self.close()
    
    def exit_action(self):
        self.close()
        
    def saerogochim(self):
        self.room_list.clear()
        conn.commit()
        sql = "SELECT * FROM room"
        cur.execute(sql)
        result = cur.fetchall()
        print(result)
        for i in range(len(result)):
            self.room_list.addItem(result[i][0])
                 
        
class Makeroomwindow(QMainWindow,form_makeroomwindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_no.clicked.connect(self.btn_no_click)
        self.edit_passwd.setEchoMode(QLineEdit.Password)
        self.check_passwd.clicked.connect(self.check_push)
        self.edit_passwd.setReadOnly(True)
        self.btn_roomMake.clicked.connect(self.btn_Makeroom)

    def check_push(self):
        if(self.check_passwd.isChecked()):
            self.edit_passwd.setReadOnly(False)
        else:
            self.edit_passwd.setText("")
            self.edit_passwd.setReadOnly(True)
    def btn_no_click(self):
        self.main = Mainwindow()
        self.main.show()
        self.close()
    def btn_Makeroom(self):
        password = None
        if(self.check_passwd.isChecked()):
            password = self.edit_passwd.text()
        global port
        port = random.randrange(8000, 10000)
        sql = "insert into room(name, max_people, password_check, password, port, people_count) values (%s, %s, %s, %s, %s, 1)"
        vals = (self.edit_roomname.text(), self.people_count_num.value(), self.check_passwd.isChecked(), password, port)
        while(1):
            if(cur.execute(sql, vals)):
                conn.commit()
                user_port_open.port_open(port)
                self.chatroom = Chatroomwindow()
                self.chatroom.show()
                self.close()
                break

class room_password_check(QDialog, QWidget, form_roompasswordcheckwindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.btn_ok.clicked.connect(self.ok_click)
    def ok_click(self):
        self.password = self.password_edit.text()
        self.close()
        
class Chatroomwindow(QMainWindow,form_chatroomwindow):
    host = '127.0.0.1'
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.exit_btn.clicked.connect(self.btn_exit)
        self.enter_btn.clicked.connect(self.btn_enter)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, port))
        self.client_socket.send(user_id.encode('utf-8')) 
        self.listWidget.addItem(user_id)
        
        receive_thread = threading.Thread(target=self.handle_receive, args=())
        receive_thread.daemon = True
        receive_thread.start()

        # receive_thread.join()

        
    def btn_exit(self):
        sql = "update room set people_count = (select (people_count-1) where port = %s) where port = %s"
        vals = (port, port)
        cur.execute(sql, vals)
        conn.commit()
        sql = "select people_count from room where port = %s"
        vals = (port)
        cur.execute(sql, vals)
        result = cur.fetchall()
        print(result[0][0])
        if result[0][0] == 0:
            print(1)
            sql = "delete from room where port = %s"
            vals = (port)
            cur.execute(sql, vals)    
            conn.commit()
        self.main = Mainwindow()
        self.main.show()
        self.client_socket.send("/종료".encode('utf-8'))
        self.client_socket.close()
        self.close()
        
    def btn_enter(self):
        if(self.chat_input.text()):
            msg = self.chat_input.text()
            self.client_socket.send(self.chat_input.text().encode('utf-8'))
            self.chat_input.setText("")
            self.add_chat(msg)
    
    def add_chat(self, msg):
        self.chattingchang.appendPlainText(user_id+" : "+msg)
    
    def handle_receive(self):
        while 1:
            try:
                data = self.client_socket.recv(1024)
            except:
                print("연결 끊김")
                break
            data = data.decode('utf-8')
            print(data)
            if "!@#$" in data:
                a = data.split(",")
                print(a)
                self.listWidget.clear()
                for i in range(len(a)):
                    if a[i] != "!@#$":
                        self.listWidget.addItem(a[i].strip())
            elif "----" in data:
                a = data.split("님")
                item = a[0].replace("----", "").strip()
                # self.listWidget.takeItem(item)
            else:
                a = data.split(":")
                for i in range(len(a)):
                    a[i] = a[i].strip()
            if not user_id == a[0]:
                if not a[0] == "!@#$": 
                    self.chattingchang.appendPlainText(data)


            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = LoginWindow()
    myWindow.show()
    app.exec_()
    print("종료")
    conn.close()