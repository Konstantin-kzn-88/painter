import socketserver
import json
from server import geom
from server import draw

class ThredingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class Painter_server(socketserver.BaseRequestHandler):

    def handle(self):
        def recvall(request):
            BUFF_SIZE = 4096  # 4 KiB
            data = b''
            while True:
                part = request.recv(BUFF_SIZE)
                data += part
                if len(part) < BUFF_SIZE:
                    break
            return data

        # 2. Определим ip-адрес и информацию от клиента
        _ = str(self.client_address[0]) # adress
        request = recvall(self.request)
        # 3. Попоробем взять № пути обработки и данные
        num_direction, data = self.get_data_in_request(request)
        # 4. По номеру пути определим, то что нужно клиенту:
        #    Коды:
        #      0 - проверка ключа
        #      1 - расстояние между 2 точками
        #      2 - площадь многоугольника
        #      3 - рисование зон

        answer = 'error'
        # Ключ
        if num_direction == 0:
            with open('keys.txt', 'r') as file:
                for line in file:
                    if str(data) == str(line).splitlines():
                        answer = 'True'
                        break
                    else:
                        answer = 'False'
        # Расстояние
        elif num_direction == 1:
            data = [float(i) for i in data]
            answer = geom.lenght_for_line(data)
        # площадь
        elif num_direction == 2:
            data = [float(i) for i in data]
            answer = geom.area_for_poligon(data)
        #  зоны
        elif num_direction == 3:
            scale_plan = data.pop()
            color_zone = data.pop()
            size_pic = data.pop()
            object_with_radius = data
            draw.Data_draw().draw_zone(object_with_radius, size_pic, color_zone, scale_plan)
            answer = "QPixmap"
        else:
            answer = 'error'
        print(answer, "answer")
        # 5. Закодируем ответ в байты и отправим его пользователю
        str_json = json.dumps(answer)
        self.request.sendall(bytes(str_json, encoding='utf-8'))


    def get_data_in_request(self, request: bytes):
        print('get_data_in_request')
        try:
            request = json.loads(request)
            num_direction, data = request
            return num_direction, data
        except:
            num_direction, data = 404, 'error'
            return num_direction, data


if __name__ == '__main__':
    with ThredingTCPServer(('', 8888), Painter_server) as server:
        server.serve_forever()

