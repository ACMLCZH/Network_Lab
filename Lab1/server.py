#coding = utf-8
from socket import *
from threading import Thread

def recvsocket(client_socket):
    request = client_socket.recv(1024).decode()
    print("request data:", request)      #这里可以看到客户端的请求信息
    method = request.split(' ')[0]
    src = request.split(' ')[1]
    content = ''
    if method == 'GET':
        content = "HTTP/1.1 200 OK\r\n"
        content += "Server: pycharm server\r\n\r\n"
        content += 'hello world!'
    elif method == 'POST':
        print(request)
        form = request.split('\r\n')
        entry = form[-1]
        content = 'HTTP/1.1 200 ok\r\nContent-Type: text/html\r\n\r\n'
        content += entry
        content += 'hello world!'
    else:
        pass

    '''response_start_line = "HTTP/1.1 200 OK\r\n"      #按照网页的响应报头格式编写响应信息
    response_headers = "Server: pycharm server\r\n"
    response_boby = "hello world"     #响应内容
    response = response_start_line + response_headers + "\r\n" + response_boby
    client_socket.send(response.encode("utf-8"))'''
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