# PyProxy
A simple http/https proxy that helps you bypass firewalls

## Dependency
- socket
- threading
- time

## How to use it?
### For Server:
```
def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('0.0.0.0', 5200))
	sock.listen(4096)
```
You can modify the server listen port, the maximum number of TCP keep-alive connections here.

And then, run `python server.py` to start the proxy server.

### For Client:
```
def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('127.0.0.1', 1080))
	sock.listen(256)
```
You can modify the client listen port, the maximum number of TCP keep-alive connections here.

```
def clientIn(client, address):
	sockr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sockr.connect(('127.0.0.1', 5200))
```
You should put your server ip and port here.

And then, run `python client.py` to start the proxy client.

### Demo Server
Server Address: pp.pakho.xyz
Server Port: 5200

### Finally
Configure http/https(not socks4/socks5) proxy with your client ip and port in any software supported it.

Have fun!

## License
PyProxy is published under MIT License. See the LICENSE file for more.

<hr>

# PyProxy
一个简单的http/https代理，可以帮助你穿越防火墙

## 依赖
- socket
- threading
- time

## 怎样使用？
### 服务端:
```
def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('0.0.0.0', 5200))
	sock.listen(4096)
```
你可以在这里设置服务器IP和监听端口，还可以修改最大TCP连接数。

然后，运行 `python server.py` 启动服务端。

### 客户端:
```
def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('127.0.0.1', 1080))
	sock.listen(256)
```
你可以在这里设置本地客户端的监听端口，还可以修改最大TCP连接数。

```
def clientIn(client, address):
	sockr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sockr.connect(('127.0.0.1', 5200))
```
你应该把服务器IP和端口填在这里。

然后，运行 `python client.py` 启动客户端。

### 测试服务器
服务器地址: pp.pakho.xyz
服务器端口: 5200

### 最后
在你的软件中，使用客户端IP和端口来配置http/https代理，不是socks4/socks5代理。

祝你愉快！

## 许可协议
PyProxy采用MIT许可协议。查看LICENSE文件了解更多。