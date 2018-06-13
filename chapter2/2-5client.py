#!/usr/bin/env python
#  -*- coding:utf-8 -*-

"""
2-5 网络互连和套接字。
实现 Python 库参考文档中关于 socket 模块中的 TCP 客户端/服务器程序示例，并使其能够正常工作。首先运行服务器，然后启动客户端。
也可以在 http://docs.python.org/library/socket#example 网址中找到在线源码。
如果你觉得示例中服务器的功能太单调，那么可以更新服务器代码，以使它具有更多功能，令其能够识别以下命令。
date 服务器将返回其当前日期/时间戳，即 time.ctime()。
os 获取操作系统信息（os.name）。
ls 列出当前目录文件清单（提示： os.listdir()列出一个目录， os.curdir 是当前目录）。

选做题：接受 ls dir 命令，返回 dir 目录中的文件清单。
你不需要一个网络来完成这个任务，因为你的计算机可以与自己通信。请注意，在服务器退出之后，在再次运行它之前必须清除它的绑定。
否则，可能会遇到“端口已绑定”的错误提示。此外，操作系统通常会在 5 分钟内清除绑定，所以请耐心等待
"""

import socket

HOST = 'localhost'
PORT = 55555
ADDR = (HOST, PORT)
BUFSIZE = 30


def recvall(the_socket, bufsize=1024):
    all_data = []
    while True:
        recv_data = ''  # init
        try:
            recv_data = the_socket.recv(bufsize)
        except socket.error as e:
            print e

        if recv_data:
            all_data.append(recv_data)
            if len(recv_data) == bufsize:
                the_socket.setblocking(0)  # 非阻塞
            else:
                break
        else:
            break
    the_socket.setblocking(1)  # 阻塞
    return ''.join(all_data)

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect(ADDR)

while True:
    data = recvall(cs, BUFSIZE)
    print data
    data = raw_input('>')
    if data:
        cs.sendall(data)
    else:
        break

cs.close()
