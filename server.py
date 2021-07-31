from lib.http import *
from urllib.parse import unquote


def serverIORoutine(methods: str, body: bytes, header: str):
    path = methods.split(" ")[1]
    path = unquote(path)
    
    body = path
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