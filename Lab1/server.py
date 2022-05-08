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
    return request, request[request.find("\r\n\r\n") + 4:], data_len


def recvsocket(client_socket, server_sql, thread_lock):
    request, entry, data_len = receive(client_socket)
    print("request data:\n", request)      # 这里可以看到客户端的请求信息
    method = request.split(' ')[0]
    if method == 'GET':
        content = "HTTP/1.1 200 OK\r\n"
        content += "Server: mysql server\r\n\r\n"
        content += 'hello world!'
    elif method == 'POST':

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

