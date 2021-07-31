import requests

requests.post("http://localhost/sendFile/?id=admin&path=/test.txt", data="hello, world!")