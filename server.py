from lib.http import *
from urllib.parse import unquote

import os
import sys

class serverInfo():
    def __init__(self) -> None:
        self.downloadPath = "./downloads"

class clientInfo():
    def __init__(self) -> None:
        self.userId = 0

serverInfomation = serverInfo()
clientInformation = clientInfo()

def serverIORoutine(requestMethods: str, requestBody: bytes, requestHeader: str):
    path = requestMethods.split(" ")[1]
    path = unquote(path)

    body = '{"status":"success"}'
    headerList = [
        ("content-type", "text"),
        ("connection", "close"),
        ("content-length", str(len(body)))
    ]

    httpResponseMessage = setHttpResponseMessage("200 OK", headerList, body)

    if requestMethods.split(" ")[0] == "POST":
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

            saveFilePath = serverInfomation.downloadPath + "/" + userId + "/" + saveFilePath

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

            # .. path name meaning is before path. that is security problem
            if directoryName == "..":
                httpResponseMessage = setHttpResponseMessage("406 Not Acceptable", headerList, "{\"status:\"security error\"}") 
            else:
                f = open(saveFilePath, "wb")
                f.write(requestBody)
                f.close()

                httpResponseMessage = setHttpResponseMessage("201 Created", headerList, "{\"status:\"done\"}") 

    return httpResponseMessage

def main():
    
    httpServer(serverIORoutine)
    return 

if __name__ == "__main__":
    main()