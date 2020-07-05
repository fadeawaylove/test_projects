import socket
import select
import queue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ipv4 tcp
server.setblocking(False)  # 设置非阻塞
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = ("127.0.0.1", 8989)
server.bind(server_address)
server.listen(10)

inputs = [server]
outputs = []
message_queue = {}
time_out = 60

while True:
    print("等待活动连接...")
    readable, writeable, exceptional = select.select(inputs, outputs, inputs, time_out)
    if not (readable or writeable or exceptional):
        print("select超时无活动连接,重新连接select...")
        continue
    for s in readable:
        # 如果是server监听的socket
        if s is server:
            connection, client_address = s.accept()
            print(f"新连接：{client_address}")
            connection.setblocking(False)
            # 将连接加入输入
            inputs.append(connection)
            message_queue[connection] = queue.Queue()
        else:
            # 客户端发来的消息
            data = s.recv(1024)
            if data:
                print(f"收到数据：{data.decode()}, 客户端：{s.getpeername()}")
                message_queue[s].put(data)
                if s not in outputs:
                    outputs.append(s)
            else:
                print(f"关闭连接：{s.getpeername()}")
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                del message_queue[s]
    for s in writeable:
        try:
            msg = message_queue[s].get_nowait()
        except queue.Empty:
            print(f"连接：{s.getpeername()}消息队列为空")
            outputs.remove(s)
        else:
            s.send(msg)
    for s in exceptional:
        print(f"异常连接：{s.getpeername()}")
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del message_queue[s]
