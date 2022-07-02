# -----------------------------------------------------------
# Класс предназначен для работы работы клиента с сервером
#
# Класс реализует:
# - проверку подключения к серверу
# - передачу данных на сервер
# - прием данных с сервера
#
# (C) 2022 Kuznetsov Konstantin
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------

from PySide2 import QtWidgets, QtGui, QtCore
import socket
import json

KEY = '@v&#XST3kH-t9fZad69eN'
IP = '127.0.0.1'

class Client(QtWidgets.QWidget):
    def __init__(self, key = KEY):
        super().__init__()
        self.key = key

    def __recvall(self, sock):
        """Функция приема сообщения целиком"""
        BUFF_SIZE = 256  # 4 KiB
        data = b''
        while True:
            part = sock.recv(BUFF_SIZE)
            data += part
            if len(part) == 0:
                break
        return data

    def check_key(self):
        try:
            server_call = 0
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((IP, 8888))
            str_json =  json.dumps((server_call, self.key))
            sock.send(bytes(str_json, encoding='utf-8'))
            res = self.__recvall(sock)
        except ConnectionRefusedError:
            res = 'error'
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Подключение к серверу отсутсвует!")
            msg.exec()
        if res != 'error':
            return bool(res)
        else:
            return False

    def server_get_lenght(self, data: list) -> float:
        try:
            server_call = 1
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((IP, 8888))
            str_json =  json.dumps((server_call, data))
            sock.send(bytes(str_json, encoding='utf-8'))
            res = self.__recvall(sock)
        except ConnectionRefusedError:
            res = 'error'
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Подключение к серверу отсутсвует!")
            msg.exec()
        if res != 'error':
            return float(res)
        else:
            return 0