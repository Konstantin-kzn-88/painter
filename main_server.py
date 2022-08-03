import socketserver
import json
from server import geom

KEY = ('@v&#XST3kH-t9fZad69eN', # мой ключ
       '6fjr9q9yY6-gZ&rdNtVfz', # Дима
       '$g%7cZVW37-UkQH7VvL94',
       '4yw*s3uWR6-$EuaDa3z%%',
       'Drh#rK&5QW-Q&Tpz62$C$',
       'XWPMvdT7zg-&5$PsGPT#k',
       '9D%WMgsUTc-Gx9b46AtPC',
       'RpTmGFG%Zh-upmN7AN%9k',
       '*%bBfYJx5E-D$9BQ$YpjZ',
       '7BjESbFm$q-W%J&NgruWq',
       '3WNkBRpG%Y-b5WPej8&yv',
       '%EtPr@H@&*-f5PVkqb2c*',
       'bG%@Tga7v*-2JHRBpGWx$',
       'L&2GrP@D$5-ra$5b7THh8',
       'gKmpUaX3SX-#U8aQA7QXv',
       'Zztfn43wZS-@$PG&*edp*',
       '$T983MA%DK-7wu&4Bd@cd',
       '6#7jpa2G#c-gZ8qsz7K5z',
       '$Bu#e8VwFu-qbvM6N646z',
       'YN2T2QQ#y2-dQJ#ephJvf',
       'H8fLNnerLG-D@CmE*k6AW',
       's@rRYPg#X9-q$HkLAHgWA',
       'pnGbP*UzxY-F9dxXkV4fq',
       'n6$3stUcL7-u6jYDTdK6V',
       'Cb*sJYVX6p-gcmvG4Ujnb',
       '$Va7R*rH3b-hZkxEY4Y3E',
       '%6pEsSkxQF-nbvu3%A2bK',
       'ChdFK3VD3u-xKVp%jfyp&',
       '$9pG8Z8E4z-&BnXDc$XMS',
       'v6c8LwVk7B-mm3H#mzEh%',
       'sA#DKaS8uv-gwjxL7&Jk%',
       '@aTs9%$FtC-re*eG8wA4K',
       '4Ya#fc*BAu-YdEw5fDe2r',
       '4Gef4KKhuV-gK%QL&MsDj',
       '$eaeah&3@7-Utfc@Vcecv',
       'mpY9v4Tdnf-deLUFQQZ*P',
       '$PF@f79G#D-RkpsdtUGfh',
       'ZgjAq&2SuL-@k$yERC6v2',
       'FSv$&%nFFY-uLmq&zr@j8',
       '%SzArPxwuD-3Uz5XkjZ8&',
       'C4D#vqgDhV-JC$@CcEEx5',
       '*E@8N#anN7-LTEpcUdy&9',
       '@rfAjL5Jbz-u6W8G&64%s',
       'm3uRR9dr2#-93wM95$dzk',
       'v8k&BWr&bC-hneSBwQ2X5',
       'rtD$YYc@W@-JCrPh2vFB8',
       'Rd543xqRpy-ZssWHH%vJ5',
       'f3VCnM%Drk-HRk#wRUV7P',
       'k9@zQ*X3W#-u8nr9tFa&s',
       '*FKx6gGm7z-LK%@$wbEjr',
       'y5J#NbtRPW-6fB%Nckj%x')


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
        _ = str(self.client_address[0])  # adress
        request = recvall(self.request)
        # 3. Попоробем взять № пути обработки и данные
        num_direction, data = self.get_data_in_request(request)
        # 4. По номеру пути определим, то что нужно клиенту:
        #    Коды:
        #      0 - проверка ключа
        #      1 - расстояние между 2 точками
        #      2 - площадь многоугольника
        #      3 - получение зоны с учетом масштаба

        answer = 'error'
        # Ключ
        if num_direction == 0:
            if data in KEY:
                answer = True
            else:
                answer = False

        # Расстояние
        elif num_direction == 1:
            data = [float(i) for i in data]
            answer = geom.lenght_for_line(data)
        # площадь
        elif num_direction == 2:
            data = [float(i) for i in data]
            answer = geom.area_for_poligon(data)

        else:
            answer = 'error'
        print(answer, "answer")
        # 5. Закодируем ответ в байты и отправим его пользователю
        str_json = json.dumps(answer)
        self.request.sendall(bytes(str_json, encoding='utf-8'))

    def get_data_in_request(self, request: bytes):
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
