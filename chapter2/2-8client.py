#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import threading

HOST = 'localhost'
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


cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect(ADDR)

# 启一个线程专门接收数据
t = threading.Thread(target=recv_message, args=(cs, ADDR, BUFSIZE))
t.setDaemon(True)
t.start()

while True:
    send_data = raw_input('> ')
    if send_data:
        cs.sendall(send_data)
    else:
        break
cs.close()