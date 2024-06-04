import socket
import sys
import random


class Client:
    def __init__(self, server_ip, server_port, filename, Lmin, Lmax, content):
        # 初始化变量
        self.server_ip = server_ip
        self.server_port = server_port
        self.filename = filename
        self.Lmin = Lmin
        self.Lmax = Lmax
        self.content = content
        self.data_blocks = None
        # 创建套接字
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))

    # 读取文件内容
    # def readfile(self):
    #     with open(self.filename, 'r') as f:
    #         self.content = f.read()

    # 切分文件
    def split_file(self):
        # data_blocks用来存放切分的文件块
        self.data_blocks = []
        file_length = len(self.content)
        start = 0
        while start < file_length:
            # 随机切分块
            block_length = random.randint(self.Lmin, self.Lmax)
            end = min(start + block_length, file_length)
            self.data_blocks.append(self.content[start:end])
            start = end

    # 发送 Initialization 报文
    def send_initialization(self):
        Type = (1).to_bytes(2, byteorder='big')
        N = len(self.data_blocks).to_bytes(4, byteorder='big')
        init_message = Type + N
        self.client_socket.sendall(init_message)

    # 接收agree报文
    def recv_agree(self):
        agree_message = self.client_socket.recv(1024)
        if agree_message != (2).to_bytes(2, byteorder='big'):
            print("Fail to receive the agree message of server")
            self.client_socket.close()
            sys.exit(1)

    # 发送reverseRequest报文并接收reverseAnswer报文
    def reverse_file(self):
        reversed_content = ""
        for i, block in enumerate(self.data_blocks):
            Type = (3).to_bytes(2, byteorder='big')
            block_length = len(block)
            Length = block_length.to_bytes(4, byteorder='big')
            Data = block.encode()
            request_message = Type + Length + Data
            self.client_socket.sendall(request_message)
            # 接收 reverseAnswer 报文
            ans_message = self.client_socket.recv(1024)
            ans_Type = int.from_bytes(ans_message[:2], byteorder='big')
            ans_Length = int.from_bytes(ans_message[2:6], byteorder='big')
            ans_data = ans_message[6:].decode()
            if ans_Type != 4:
                print(f"Receive false type: {ans_Type}")
                self.client_socket.close()
                sys.exit(1)
            else:
                print(f"第{i + 1}块：{ans_data}")
                reversed_content=ans_data+reversed_content
        return reversed_content

    def disconnection(self):
        self.client_socket.close()


# 检查命令行参数

# 从命令行获取参数
def get_arguments():
    # check arguments
    if len(sys.argv) not in [4, 6]:
        print("python3 client.py <ServerIP> <ServerPort> <Filename> [<Lmin> <Lmax>]")
        sys.exit(1)
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    filename = sys.argv[3]
    # 设置默认值（若用户未输入）
    Lmin = 50
    Lmax = 100
    # 读取文件内容
    with open(filename, 'r') as f:
        content = f.read()
    #初始化并检查Lmin和Lmax
    if len(sys.argv) > 4:
        Lmin = int(sys.argv[4])
    if len(sys.argv) > 5:
        Lmax = int(sys.argv[5])
    if Lmin > Lmax:
        print("error:Lmin>Lmax")
        sys.exit(1)
    if Lmin <= 0 or Lmax > len(content):
        print("error:Lmin<=0")
        sys.exit(1)
    if Lmax > len(content):
        print("error:Lmax>content")
        sys.exit(1)
    return server_ip, server_port, filename, Lmin, Lmax, content


#
def main():
    # 检查并获取参数
    server_ip, server_port, filename, Lmin, Lmax, content = get_arguments()
    # 创建client类并处理文件
    client = Client(server_ip, server_port, filename, Lmin, Lmax,content)
    client.split_file()
    client.send_initialization()
    client.recv_agree()
    reversed_content = client.reverse_file()
    # 输出接收到的反转文本
    print("反转后的文本为：")
    print(reversed_content)
    # 关闭套接字
    client.disconnection()


if __name__ == "__main__":
    main()

# 面向过程
# if len(sys.argv) not in [4, 6]:
#     print("python3 client.py <ServerIP> <ServerPort> <Filename> [<Lmin> <Lmax>]")
#     sys.exit(1)
# # 从命令行获取参数
# server_ip = sys.argv[1]
#     server_port = int(sys.argv[2])
#     filename = sys.argv[3]
#     if len(sys.argv > 4):
#         Lmin = sys.srgv[4]
#     else:
#         Lmin = 50
#     if len(sys.argv > 5):
#         Lmax = sys.srgv[5]
#     else:
#         Lmax = 100
#     return server_ip,server_port,filename,Lmin,Lmax
# 读取文件内容
# def readfile():
#     with open(filename, 'r') as f:
#         content = f.read()
# # 创建套接字
# def create_socket():
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect((server_ip, server_port))
# # 切分文件
# def split_file():
#     # data_blocks用来存放切分的文件块
#     data_blocks = []
#     file_length = len(content)
#     start = 0
#     while start < file_length:
#         # 随机切分块
#         block_length = random.randint(Lmin, Lmax)
#         end = min(start + block_length, file_length)
#         data_blocks.append(content[start:end])
#         start = end
# # 发送 Initialization 报文
# def send_Initialization():
#     Type = (1).to_bytes(2, byteorder='big')
#     N = len(data_blocks).to_bytes(4, byteorder='big')
#     init_message = Type + N
#     client_socket.sendall(init_message)
# # 接收agree报文
# def recv_agree():
#     agree_message = client_socket.recv(1024)
#     if agree_message != (2).to_bytes(2, byteorder='big'):
#         print("Fail to receive the agree message of server")
#         client_socket.close()
#         sys.exit(1)
# # 发送reverseRequest报文
# def send_reverseRequest():
#     reversed_content = ""
#     for i, block in enumerate(data_blocks):
#         Type = (3).to_bytes(2, byteorder='big')
#         block_length = len(block)
#         Length = block_length.to_bytes(4, byteorder='big')
#         Data = block.encode()
#         request_message = Type + Length + Data
#         client_socket.sendall(request_message)
#         # 接收reverseAnswer报文
#         ans_message = client_socket.recv(1024)
#         ans_Type = int.from_bytes(ans_message[:2], byteorder='big')
#         ans_Length = int.from_bytes(ans_message[2:6], byteorder='big')
#         ans_data = ans_message[6:].decode()
#         if ans_Type != 4:
#             print(f"Receive false type:{ans_Type}")
#             client_socket.close()
#             sys.exit(1)
#         else:
#             print(f"第{i + 1}块：{ans_data}")
#             reversed_content += ans_data
# print("反转后的文本为：")
# print(reversed_content)
# # 关闭套接字
# client_socket.close()
