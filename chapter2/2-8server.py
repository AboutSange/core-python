#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
2-8 全双工聊天。更新上一个练习的解决方案，修改它以使你的聊天服务现在成为全双
工模式，意味着通信两端都可以发送并接收消息，并且二者相互独立。
"""

import socket
import threading

HOST = ''
PORT = 55555
ADDR = (HOST, PORT)
BUFSIZE = 1024


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


def recv_message(the_socket, addr, bufsize=1024):
    print 'recv_message start'
    while True:
        data = recvall(the_socket, bufsize)
        if data:
            print '{} {}'.format(addr, data)
            print '> ',
        else:
            break
    print 'recv_message end'


ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(ADDR)
ss.listen(5)

while True:
    print 'waiting connecting ...'
    cs, addr = ss.accept()
    print 'connected with {}'.format(addr)

    # 启一个线程专门接收数据
    t = threading.Thread(target=recv_message, args=(cs, addr, BUFSIZE))
    t.setDaemon(True)
    t.start()

    while True:
        send_data = raw_input('> ')
        if send_data:
            cs.sendall(send_data)
        else:
            break
    cs.close()
ss.close()


