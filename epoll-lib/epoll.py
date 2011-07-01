#!/usr/bin/python2.6

import select
import socket
import logging

TIMEOUT = 5 

class Epoll(object):
  def __init__(self, listen_fd, epoll_flags):
    self._listen_fd = listen_fd
    self._listen_events = epoll_flags
    self._connections = {}

  def Init(self):
    self.__epoll = select.epoll()
    self.__epoll.register(self._listen_fd)

  def Loop(self):
    while True:
      events = self.__epoll.poll(TIMEOUT)
      for fd, event in events:
        if fd == self._listen_fd.fileno():
          conn, addr = self._listen_fd.accept()
          conn.setblocking(0)
          self.__epoll.register(conn.fileno(), select.EPOLLIN | select.EPOLLET)
          self._connections[conn.fileno()] = conn
        elif event & select.EPOLLIN:
          data = self._connections[fd].recv(1024)
          if data == '':
            self.__epoll.unregister(fd)
            self._connections[fd].close()
            del self._connections[fd]
          else:
            print data
        elif event & select.EPOLLHUP:
          self.__epoll.unregister(fd)
          self._connections[fd].close()
          del self._connections[fd]


def InitListenSocket(port):
  listen_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  listen_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  listen_fd.bind(('0.0.0.0', port))
  listen_fd.listen(socket.SOMAXCONN)
  return listen_fd


def SetupStreamEpoll(port):
  listen_fd = InitListenSocket(port)
  epoll = Epoll(listen_fd, select.EPOLLIN)
  epoll.Init()
  epoll.Loop()
          

def main():
  # setup listing socket on a high port.
  SetupStreamEpoll(11111)

if __name__ == '__main__':
  main()
