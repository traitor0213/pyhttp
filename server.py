from lib.http import *
from urllib.parse import unquote

import os
import sys

class serverInfo():
    def __init__(self) -> None:
        self.downloadPath = "./downloads"
        self.uploadPath = "./uploads"

class clientInfo():
    def __init__(self) -> None:
        self.userId = 0

serverInfomation = serverInfo()
clientInformation = clientInfo()

def serverIORoutine(requestMethods: str, requestBody: bytes, requestHeader: str):
    path = requestMethods.split(" ")[1]
    path = unquote(path)

    # set default http response message
    body = '{"status":"success"}'
    headerList = [
        ("content-type", "text"),
        ("connection", "close"),
        ("content-length", str(len(body)))
    ]

    httpResponseMessage = setHttpResponseMessage("200 OK", headerList, body)

    # GET method
    if requestMethods.split(" ")[0] == "GET":

        # route for client recv file from server request
        if "/recvFile" in path:
            # get http query from string to list[dict] 
            queryList = getHttpRequestQuery(path)

            sendFilePath = ""
            userId = ""

            # extract http query
            for query in queryList:
                if query["query"] == "path":
                    sendFilePath = query["value"]
            
            # TODO: send file from server to client 
            sendFilePath = serverInfomation.uploadPath + sendFilePath

            if os.path.exists(sendFilePath) == True:
                fileName = ""

                i = 0 
                while True:
                    if i == len(sendFilePath):
                        break 

                    if sendFilePath[i] == "/" or sendFilePath[i] == "\\":
                        fileName = ""
                    else:
                        fileName += sendFilePath[i]
                    
                    i += 1

                print(fileName)

                f = open(sendFilePath, "rb")
                fileContent = f.read()
                f.close()

                body = fileContent
                headerList = [
                    ("content-type", "text"),
                    ("connection", "close"),
                    ("Content-Disposition", ("attachment; filename=\"" + fileName + "\"")),
                    ("content-length", str(len(bytes(body))))
                ]

                httpResponseMessage = setHttpResponseMessage("200 OK", headerList, bytes(body))

                # TODO

    
    # POST method 
    if requestMethods.split(" ")[0] == "POST":
        
        # route for client send file to server request
        if "/sendFile" in path and "id=" in path:

            # get http query from string to list[dict] 
            queryList = getHttpRequestQuery(path)

            saveFilePath = ""
            userId = ""

            # extract http query
            for query in queryList:
                if query["query"] == "path":
                    saveFilePath = query["value"]
                if query["query"] == "id":
                    userId = query["value"]

            saveFilePath = serverInfomation.downloadPath + "/" + userId + saveFilePath
            
            # create download directory
            fullDirectory = ""
            directoryName = ""
            for pathChar in saveFilePath:
                directoryName += pathChar
                if pathChar == "/" or pathChar == "\\":
                    if directoryName == "..":
                        break 

                    fullDirectory += directoryName        
                    if os.path.exists(fullDirectory) == False:
                        os.mkdir(fullDirectory)
                    
                    directoryName = ""

            # .. path name mean's before path. that makes security problem

            if directoryName == "..":
                body = "{\"status:\"security error\"}"
                
                headerList = [
                    ("content-type", "text"),
                    ("connection", "close"),
                    ("content-length", str(len(body)))
                ]

                httpResponseMessage = setHttpResponseMessage("406 Not Acceptable", headerList, body) 
            else:

                f = open(saveFilePath, "wb")
                f.write(requestBody)
                f.close()
                
                body = "{\"status:\"done\"}"
                headerList = [
                    ("content-type", "text"),
                    ("connection", "close"),
                    ("content-length", str(len(body)))
                ]

                httpResponseMessage = setHttpResponseMessage("201 Created", headerList, body) 

    return httpResponseMessage

def main():
    
    httpServer(serverIORoutine)
    return 

if __name__ == "__main__":
    main()