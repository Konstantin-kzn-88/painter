import os
import time
import socketserver
import datetime
import json
from server import geom



class ThredingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class Safety_server(socketserver.BaseRequestHandler):
    """
    Класс многопоточного сервера для получения данных от клиента
    и обработки информации
    """

    def handle(self):
        # 1. Получим информацию в байтах от клиента
        bytes_in_handle = self.request.recv(1024).strip()

        # 2. Определим ip-адрес и информацию от клиента
        _ = str(self.client_address[0]) # adress
        request = str(bytes_in_handle.decode())

        # 3. Попоробем взять № пути обработки и данные
        num_direction, data = self.get_data_in_request(request)

        # 4. По номеру пути определим, то что нужно клиенту:
        #    Коды:
        #      0 - проверка ключа
        #      1 - расстояние между 2 точками

        # Ключ
        if num_direction == 0:
            with open('keys.txt') as f:
                print(data,"data")
                if data in f.read():
                    print(data)
                    answer = 'True'
                else:
                    answer = 'False'
        # Расстояние
        elif num_direction == 1:
            data = [float(i) for i in data]
            answer = geom.lenght_for_line(data)

        else:
            answer = 'error'

        # 5. Закодируем ответ в байты и отправим его пользователю
        ans = bytes(str(answer), encoding='utf-8')
        self.send_msg(self.request,ans)



    def get_data_in_request(self, request: str):
        try:
            request = json.loads(request)
            num_direction, data = request
            return num_direction, data
        except:
            num_direction, data = 404, 'error'
            return num_direction, data

    def send_msg(self, sock, msg):
        sock.sendall(msg)

if __name__ == '__main__':
    with ThredingTCPServer(('', 8888), Safety_server) as server:
        server.serve_forever()
