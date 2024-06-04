import socket
import select


class Server:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        # 创建TCP套接字
        # 生成socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen(5)
        # 不经过WAIT_TIME 直接关闭
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 设置非阻塞编程
        self.server_socket.setblocking(False)

        # 初始化输入列表
        self.inputs = [self.server_socket]
        # 将客户端套接字及地址保存在一个字典中
        self.clients = {}

    # 在run方法中，区分可读的套接字是服务器套接字(self.server_socket)还是客户端套接字的原因：
    #
    # 服务器套接字(self.server_socket):
    # 服务器套接字是专门用于监听新的连接请求的。当select函数返回服务器套接字可读时，意味着有一个新的客户端尝试连接到服务器。
    # 处理方式是接受这个新的连接，生成一个新的客户端套接字。这个新的客户端套接字将用于与该客户端进行后续的通信。
    #
    # 客户端套接字:
    # 客户端套接字是用于与特定客户端进行数据通信的。当select函数返回客户端套接字可读时，意味着该客户端发送了数据。
    # 处理方式是从该套接字读取数据，并根据数据内容进行相应的处理。
    def run(self):
        print(f"Server is listening on {self.server_ip}:{self.server_port}")
        while True:
            # r, w, e, = select.select（rlist, wlist,xlist[, timeout]）
            # 传递三个参数，一个为输入而观察的文件对象列表，一个为输出而观察的文件对象列表和一个观察错误异常的文件列表。
            # 第四个是一个可选参数，表示超时秒数。
            r_list, w_list, e_list = select.select(self.inputs, self.inputs, self.inputs)
            for sock in r_list:
                if sock is self.server_socket:
                    client_socket, client_addr = self.server_socket.accept()
                    print(f"Accepted connection from {client_addr}")
                    # 设置非阻塞连接
                    client_socket.setblocking(False)
                    self.inputs.append(client_socket)
                    self.clients[client_socket] = {
                        'addr': client_addr,
                        'block_exp': 0,  # 预期需要接受的block数目
                        'block_recv': 0  # 现已经接收到的block数目
                    }
                else:
                    if not self.handle_data(sock):
                        self.inputs.remove(sock)
                        del self.clients[sock]
                        sock.close()
            for sock in e_list:
                self.inputs.remove(sock)
                del self.clients[sock]
                sock.close()

    def handle_data(self, client_socket):
        try:
            message = client_socket.recv(1024)
            if not message:
                return False
            client_info = self.clients[client_socket]
            # 若预期接受的块数为0 message即接收Initialization报文
            # int.from_bytes(message[:2], byteorder='big') == 1
            if client_info['block_exp'] == 0:
                if int.from_bytes(message[:2], byteorder='big') == 1:
                    client_info['block_exp'] = int.from_bytes(message[2:6], byteorder='big')
                    # 发送agree报文
                    agree_message = (2).to_bytes(2, byteorder='big')
                    client_socket.sendall(agree_message)
            else:
                client_info['block_recv'] += 1
                self.process_block(client_socket, message)

                # 若所有块都处理完毕，用户端会关闭它的套接字，因此，需要在server端清除该socket
                if client_info['block_recv'] == client_info['block_exp']:
                    print(f"All blocks received from {client_info['addr']}. Closing connection.")
                    return False
            return True
        except Exception as e:
            print(f"Error handling client data: {e}")
            return False

    def process_block(self, client_socket, message):
        client_info = self.clients[client_socket]
        client_addr = client_info['addr']
        message_Type = int.from_bytes(message[:2], byteorder='big')
        if message_Type == 3:
            message_Length = int.from_bytes(message[2:6], byteorder='big')
            content = message[6:6+message_Length].decode()
            # 反转文本
            reversed_content = content[::-1]
            Type = (4).to_bytes(2, byteorder='big')
            Length = message_Length.to_bytes(4, byteorder='big')
            response = Type + Length + reversed_content.encode()
            client_socket.sendall(response)
            print(f"Processed and responded to a block from {client_addr}")


def main():
    server_ip = '127.0.0.1'
    server_port = 12345
    server = Server(server_ip, server_port)
    server.run()

if __name__ == "__main__":
    main()
