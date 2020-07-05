import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("127.0.0.1", 8989)
client.connect(server_address)

while True:
    data = input("请输入数据：")
    client.sendall(data.encode())
    server_data = client.recv(1024)
    print(f"客户端收到数据：{server_data.decode()}")
    # client.close()
