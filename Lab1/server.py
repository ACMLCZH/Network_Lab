# coding = utf-8
from socket import *
from threading import Thread, Lock
from info_extract import WiFi_parser
from loadJson2db import Server_SQL
import re


def receive(client_socket):
    request = client_socket.recv(1024).decode()
    if request.startswith("POST"):
        while "Content-Length" not in request:
            request += client_socket.recv(1024).decode()
        while "\r\n" not in request[request.find("Content-Length"):]:
            request += client_socket.recv(1024).decode()
        curs = request[request.find("Content-Length"):]
        data_len = int(curs[16: curs.find("\r\n")])
    else:
        data_len = 0
    while "\r\n\r\n" not in request:
        request += client_socket.recv(1024).decode()
    if request.startswith("POST"):
        if "Expect: 100-continue" in request:
            client_socket.send('HTTP/1.1 100 Continue\r\n\r\n'.encode("utf-8"))
        while len(request[request.find("\r\n\r\n") + 4:]) < data_len:
            request += client_socket.recv(1024).decode()
    # request += client_socket.recv(1024).decode()
    return request, request[request.find("\r\n\r\n") + 4:], data_len


def recvsocket(client_socket, server_sql, thread_lock):
    request, entry, data_len = receive(client_socket)
    print("request data:\n", request)      # 这里可以看到客户端的请求信息
    method = request.split(' ')[0]
    # print(request.split(' '))
    # print(request.split('\r\n'))
    # print(method)
    # src = request.split(' ')[1]
    # print(src)
    if method == 'GET':
        content = "HTTP/1.1 200 OK\r\n"
        content += "Server: mysql server\r\n\r\n"
        content += 'hello world!'
    elif method == 'POST':
        # print(request)
        # form = request.split('\r\n')
        # content_length = 0
        # print(form[-1])
        # entry = form[-1]    # entry是数据报正文的内容，具体到这个lab里应该是json包

        wifi_signal = WiFi_parser()
        wifi_signal.load_data(entry)
        parse_error = wifi_signal.parse()

        if parse_error:
            print("Parse error!")
        else:
            thread_lock.acquire()
            for data_list in wifi_signal.collect_list:
                if data_list[0]:
                    data_dict = {
                        "wifi_id": wifi_signal.myid,
                        "wifi_mac": wifi_signal.mymac,
                        "collect_time": wifi_signal.collect_time,
                        "device_mac": data_list[1],
                        "device_rssi1": data_list[2][0]
                    }
                    server_sql.send_data(data_dict, "WIFI_signal")
            thread_lock.release()
        # print(wifi_signal.myid)
        # print(wifi_signal.mymac)
        # print(wifi_signal.collect_time)
        # print(wifi_signal.num_collection)
        # print(wifi_signal.collect_list)
        '''

        这里已经得到了json数据包entry,以及数据包的长度conten_length
        在此处需要补充
        1.将entry送到WiFi_parser/BlueToothParser的代码,例如如果是WiFi_parser:
        2.将parser处理完的数据存入SQL数据库的代码(需要数据库部分的同学补充)
        3.利用数据库中的数据,根据定位算法计算结果的代码(算法部分)
        4.将计算结果以适当方式打包进content中,将content发回的代码(下方content为模拟测试用)
        '''

        content = 'HTTP/1.1 200 ok\r\nContent-Type: text/html\r\n\r\n'
        content += 'hello world!'
    else:
        content = 'HTTP/1.1 200 ok\r\nContent-Type: text/html\r\n\r\n'
        content += 'hello world!'

    client_socket.send(content.encode("utf-8"))
    client_socket.close()


if __name__ == '__main__':
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(("", 7788))
    server.listen(5)
    thread_lock = Lock()

    server_sql = Server_SQL()
    # server_sql = None
    while True:
        client_socket, ip_port = server.accept()        # 等待客户端连接
        print(f"{ip_port}>>>正在连接中。。。")        # 显示哪个在连接
        childthread = Thread(target=recvsocket, args=(client_socket, server_sql, thread_lock))   # 分配给线程处理
        childthread.daemon = True
        childthread.start()         # 子线程启动，主线程返回继续等待另一个客户端的连接
    server_sql.close()

