#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import socket
import threading


def getHost_IP(host):
    ip = host
    kw = ':'
    if not len(ip): return ''
    if kw in ip: ip = ip.split(kw)[0]
    try:
        ip = socket.gethostbyname(ip)
        if '127.0.0.' in ip: ip = ''
        return ip
    except:
        return ''


def getHost_Port(host):
    port = host
    kw = ':'
    if not len(port): return 0
    if kw in port:
        return int(port.split(kw)[1])
    else:
        return 80


def clientIn(client, address):
    sockr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sockr.connect(('127.0.0.1', 5200))
    except:
        print('ConnectERR: Server')
        client.close()
    else:
        sockrSend(client, sockr)


def sockrRecv(client, sockr):
    SSL = 0
    header = ''
    headerOver = 0
    status = 1
    length = -1
    lengthRecv = -1
    gzip = 0
    while True:
        try:
            sockr.settimeout(15)
            recv = sockr.recv(256)
        except:
            print('Socket Timeout')
            break
        if len(recv):
            if headerOver == 0:
                header += recv
                if '\r\n\r\n' in header: headerOver = 1
                if '\r\n' in header and status == 1:
                    statusSplit = header.split('\r\n')[0]
                    if ' 1' in statusSplit: status = 0
                    if '204' in statusSplit: status = 0
                    if '304' in statusSplit: status = 0
                if '\r\nContent-Length: ' in header and length == -1:
                    lengthSplit = header.split('\r\nContent-Length: ')[1]
                    if '\r\n' in lengthSplit: length = int(lengthSplit.split('\r\n')[0])
                if '\r\nTransfer-Encoding: chunked\r\n' in header and gzip == 0: gzip = 1
            if headerOver == 1:
                if lengthRecv == -1:
                    lengthRecv = len(header.split('\r\n\r\n')[1])
                else:
                    lengthRecv = len(recv)
                if status == 0:
                    recv = recv.split('\r\n\r\n')[0] + '\r\n\r\n'
                elif length != -1:
                    if length > lengthRecv:
                        length -= lengthRecv
                    else:
                        recv = recv[:length]
                        length = 0
                elif gzip == 1:
                    if '\r\n0\r\n\r\n' in recv:
                        recv = recv.split('\r\n0\r\n\r\n')[0] + '\r\n0\r\n\r\n'
                        gzip = -1
            if header == 'HTTP/1.1 200 Connection Established\r\n\r\n':
                threadRecvSSL = threading.Thread(target=sockrRecvSSL, args=(client, sockr))
                threadRecvSSL.start()
                threadSendSSL = threading.Thread(target=sockrSendSSL, args=(client, sockr))
                threadSendSSL.start()
                SSL = 1
                length = 0
            try:
                client.send(recv)
            except:
                print('Client Closed')
                break
            if headerOver == 1:
                if status == 0 or length == 0 or gzip == -1:
                    break
        else:
            break
    if SSL == 0:
        sockr.close()
        client.close()


def sockrSend(client, sockr):
    succ = 1
    header = ''
    headerOver = 0
    length = -1
    lengthRecv = -1
    while True:
        try:
            client.settimeout(15)
            recv = client.recv(10)
        except:
            print('Client Timeout')
            succ = 0
            break
        if len(recv):
            if headerOver == 0:
                header += recv
                if '\r\n\r\n' in header: headerOver = 1
                if '\r\nContent-Length: ' in header and length == -1:
                    lengthSplit = header.split('\r\nContent-Length: ')[1]
                    if '\r\n' in lengthSplit: length = int(lengthSplit.split('\r\n')[0])
            if headerOver == 1:
                if lengthRecv == -1:
                    lengthRecv = len(header.split('\r\n\r\n')[1])
                else:
                    lengthRecv = len(recv)
                if length != -1 and length != 0:
                    if length > lengthRecv:
                        length -= lengthRecv
                    else:
                        recv = recv[:length]
                        length = 0
            try:
                sockr.send(recv[::-1])
            except:
                print('Socket Closed')
                succ = 0
                break
            if headerOver == 1:
                if length == -1 or length == 0:
                    break
        else:
            break
    if succ == 1:
        sockrRecv(client, sockr)
    else:
        sockr.close()
        client.close()


def sockrRecvSSL(client, sockr):
    while True:
        try:
            sockr.settimeout(30)
            recv = sockr.recv(256)
        except:
            break
        if len(recv):
            try:
                client.send(recv)
            except:
                break
        else:
            break
    sockr.close()
    client.close()


def sockrSendSSL(client, sockr):
    while True:
        try:
            client.settimeout(30)
            recv = client.recv(10)
        except:
            break
        if len(recv):
            try:
                sockr.send(recv)
            except:
                break
        else:
            break
    sockr.close()
    client.close()


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 1080))
    sock.listen(256)
    while True:
        client, address = sock.accept()
        thread = threading.Thread(target=clientIn, args=(client, address))
        thread.start()


if __name__ == '__main__':
    main()
