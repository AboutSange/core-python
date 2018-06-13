# core-python
python核心编程 第三版 练习解答

## chapter2
### 2-5 基本socket的使用

**sendall()爽？recvall()了解一下**
主要是通过循环调用recv()实现：
- （1）如果接收到的数据小于bufsize，则说明数据接收完毕；
- （2）如果接收到的数据等于bufsize，则可能接收完毕，也可能还有数据未接收；
- （3）如果接收到的数据大于bufsize，则说明你该去看眼科医生了；

如果是上述第（2）种情况怎么办？继续调用recv()，阻塞？那我就设为非阻塞咯！然后数据接收完设回阻塞，搞定。
```
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
```
使用方法：
```
data = recvall(client_socket, BUFSIZE)  # 可以接受全部的数据
```

### 2-8 全双工聊天
使用多线程模块threading实现，暂只支持一对一全双工聊天（server与client）
