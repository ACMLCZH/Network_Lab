#coding = utf-8
from socket import *
from threading import Thread
import re

def recvsocket(client_socket):
    request = client_socket.recv(1024).decode()
    print("request data:\n", request)      #这里可以看到客户端的请求信息
    # print(request.split(' '))
    # print(request.split('\r\n'))
    method = request.split(' ')[0]
    # print(method)
    # src = request.split(' ')[1]
    # print(src)
    content = ''
    if method == 'GET':
        content = "HTTP/1.1 200 OK\r\n"
        content += "Server: mysql server\r\n\r\n"
        content += 'hello world!'
    elif method == 'POST':
        # print(request)
        form = request.split('\r\n')
        content_length = 0
        # 这一步提取出数据报正文的长度content_length
        for header in form:
            if re.match('Content-Length', header):
                content_length = int(header[16:])
                break
        # print(content_length)
        # print(form[-1])
        entry = form[-1] # entry是数据报正文的内容，具体到这个lab里应该是json包

        '''

        这里已经得到了json数据包entry,以及数据包的长度conten_length
        在此处需要补充
        1.将entry送到WiFi_parser/BlueToothParser的代码,例如如果是WiFi_parser:
        wifi_signal = WiFi_parser()
        wifi_signal.load_data(entry)
        wifi_signal.parse()
        print(wifi_signal.myid)
        print(wifi_signal.mymac)
        print(wifi_signal.collect_time)
        print(wifi_signal.num_collection)
        print(wifi_signal.collect_list)
        2.将parser处理完的数据存入SQL数据库的代码(需要数据库部分的同学补充)
        3.利用数据库中的数据,根据定位算法计算结果的代码(算法部分)
        4.将计算结果以适当方式打包进content中,将content发回的代码(下方content为模拟测试用)

        '''

        content = 'HTTP/1.1 200 ok\r\nContent-Type: text/html\r\n\r\n'
        content += 'hello world!'
    else:
        pass

    client_socket.send(content.encode("utf-8"))
    client_socket.close()

if __name__ == '__main__':
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(("", 7788))
    server.listen(5)
    while True:
        client_socket, ip_port = server.accept()    #等待客户端连接
        print("%s:%s>>>正在连接中。。。"%ip_port)     #显示哪个在连接
        childthread = Thread(target=recvsocket , args=(client_socket,))   #分配给线程处理
        childthread.start()        #子线程启动，主线程返回继续等待另一个客户端的连接