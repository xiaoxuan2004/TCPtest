TCP客户端-服务器反转文本传输模拟

#1. 项目说明

本项目实现了一个基于TCP的客户端-服务器通信系统，客户端将一个ASCII文本文件按随机长度切分成若干块，逐块发送给服务器，服务器对每块文本进行反转并返回给客户端。客户端在接收完所有反转块后，按顺序合并成完整的反转文本，并输出到终端。服务器设置为非阻塞，可同时处理多个客户端请求。

#2. 运行环境

- Python 3.x
- 标准 Python 库：`socket`、`random`、`time`、`select`、`sys`

#3. 配置选项

1) 客户端配置选项
- `server_ip`：服务器的IP地址
- `server_port`：服务器的端口号
- `filename`：待发送的ASCII文件名
- `Lmin`：每块数据的最小长度，默认值为50
- `Lmax`：每块数据的最大长度，默认值为100
2) 服务器配置选项
- `server_ip`：服务器的IP地址
- `server_port`：服务器的端口号

#4. 运行服务器

(1)服务器设置：
1. 确保服务器机器的IP地址和端口可访问。
2. 在服务器的终端或命令提示符中执行以下命令：
    python tcpserver.py
(2)服务器代码说明：
- `Server.__init__(self, server_ip, server_port)`：初始化服务器，绑定IP和端口，设置为非阻塞模式。
- `Server.run(self)`：运行服务器，监听和处理客户端的请求。
- `Server.handle_data(self, client_socket)`：处理客户端数据，包括接收数据块和发送反转后的数据块。
- `Server.process_block(self, client_socket, message)`：反转接收到的数据块并发送回客户端。

#5. 运行客户端

(1)客户端设置：
1. 确保客户端机器能够访问服务器的IP地址和端口。
2. 在客户端的终端或命令提示符中执行以下命令：
    python tcpclient.py <ServerIP> <ServerPort> <Filename> [<Lmin> <Lmax>]
例如：
    python tcpclient.py 127.0.0.1 12345 example.txt 50 100
    python tcpclient.py 127.0.0.1 12345 example.txt
(2)客户端代码说明：
- `Client.__init__(self, server_ip, server_port, filename, Lmin, Lmax, content)`：初始化客户端，设置服务器IP和端口、文件名及分块长度。
- `Client.split_file(self)`：按指定长度随机切分文件。
- `Client.send_initialization(self)`：发送初始化报文，告知服务器要发送的块数。
- `Client.recv_agree(self)`：接收服务器的同意连接报文。
- `Client.reverse_file(self)`：逐块发送数据并接收反转后的数据块，最终输出反转后的完整文本。
- `Client.disconnection(self)`：关闭客户端套接字。

#6. 注意事项

- 请确保服务器和客户端的IP和端口配置正确，以便双方能够正常通信。
- 可以根据需要调整数据块的最小和最大长度。
- 服务器端需设置为非阻塞模式以处理多个客户端的连接请求。
- 示例文件内容：
请在项目目录下创建一个ASCII文件（例如，`example.txt`），其内容可自定义：
例如：
A little monkey likes bananas.
