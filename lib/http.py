import socket
import select
from typing import Callable

def createHttpBuffer(headerList:list=[("connection", "close")], content:bytes=None) -> bytearray:
    headerBuffer = ""
    
    for header in headerList:
        header: tuple(str, str)
        
        headerBuffer += header[0]
        headerBuffer += ":"
        headerBuffer += header[1]
        headerBuffer += "\r\n"

    _headerBufffer = headerBuffer.lower()
    
    if "content-length" not in _headerBufffer:
        if content != None:
            headerBuffer += "content-length:" + str(len(content)) + "\r\n"

    headerBuffer += "\r\n"

    headerBuffer = headerBuffer.encode()
    headerBuffer += content

    return headerBuffer

class serverObject():
    def __init__(self, port: int = 80, backlog: int = 256) -> None:
        self.serverSocket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(("", port))
        self.serverSocket.listen(backlog)

    def getAcceptableSocket(self) -> list:
        (acceptableSocket, _, __) = select.select([self.serverSocket], [], [])
        return acceptableSocket

    def accept(self) -> socket.socket or None:
        if self.serverSocket in self.getAcceptableSocket():
            (clientSocket, _) = self.serverSocket.accept()
            return clientSocket
        else:
            return None

def readHttpMessage(readSocket: socket.socket):
    HttpMessage: bytes 

    httpHeader = ""
    while "\r\n\r\n" not in httpHeader:
        try:
            httpHeader += readSocket.recv(1).decode("utf-8")
        except:
            return

    _httpHeader = httpHeader.lower()
    _httpHeader = _httpHeader.replace(" ", "")

    HttpMessage = httpHeader.encode()

    if "content-length:" in _httpHeader:
        contentLength = int(_httpHeader.split("content-length:")[1])
        if contentLength > 0:
            httpBody = readSocket.recv(contentLength)

            HttpMessage += httpBody
    
    return HttpMessage

def httpServer(callback: Callable[[bytes], bytes], address: str = "", port: int = 80, backlog: int = 256, reverse: bool =False) -> socket.socket:
    server = serverObject()
    
    while True:
        clientSocket = server.accept()
        if clientSocket != None:
            clientMessage = readHttpMessage(clientSocket)
            clientSocket.send(callback(clientMessage))

            clientSocket.shutdown(socket.SHUT_RDWR)
            clientSocket.close()
        
        if server.serverSocket.fileno() == -1:
            break 
    
    return server.serverSocket