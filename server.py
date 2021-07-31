from lib.http import *
import socket

def serverIORoutine(clientMessage: bytes):
    body = "hello, world"
    headerList = [
        ("content-type", "text"),
        ("connection", "close"),
        ("content-length", str(len(body)))
    ]
    
    httpResponseMessage = "HTTP/1.1 200 OK".encode() + createHttpBuffer(headerList, body.encode())

    return httpResponseMessage

def main():
    
    httpServer(serverIORoutine)
    
    return 

if __name__ == "__main__":
    main()