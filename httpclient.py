#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):

    def get_host_port(self, url):
        parsedURL = urllib.parse.urlparse(url)
        print(str(parsedURL), parsedURL.port)
        host = parsedURL.hostname
        port = 80
        path = parsedURL.path

        if (":" in host):
            tempHost = host.split(":")
            host = tempHost[0]
        
        if (parsedURL.port) != None:
            port = int(parsedURL.port)

        if (path == ""):
            path = "/"

        return (host, port, path)

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        parsedData = data.split(" ")
        code = int(parsedData[1])
        return code

    def get_headers(self, data):

        return None

    def get_body(self, data):
        parsedData = data.split(" ")
        parsedData2 = data.split("\r\n")
        shouldAppend = False
        body = ""
        for responseLines in parsedData2:
            if ("<html" in responseLines):
                shouldAppend = True 
            if (shouldAppend):
                body = body + responseLines + "\r\n"
        return body
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
     
     
        return buffer.decode('utf-8')

    def get_port(self, url):
        parsed_url = urllib.parse.urlparse(url)
        if(parsed_url.port):
            return parsed_url.port
        else:
            return 80

    def get_url_content(self, url):        
        parsed_url = urllib.parse.urlparse(url)

        host = parsed_url.hostname

        path = parsed_url.path
        if(parsed_url.path == ""):
            path = "/"

        #query = ""
        if(parsed_url.query):
            #query = "?"+parsed_url.query
            path += "?"+parsed_url.query
        print(path, "path to life")
        return path, host

    def GET(self, url, args=None):
        host, port, path = self.get_host_port(url)

        self.connect(host, port)

        payload = "GET {} HTTP/1.1\r\nHost: {}\r\n\r\n".format(path, host)
        # print(payload)

        self.sendall(payload)
        connectionData = self.recvall(self.socket)
        self.close()
        splitData= connectionData.split("\r\n")
        code = self.get_code(connectionData)
        body = self.get_body(connectionData)

        self.connect(host, self.get_port(url))

        payload = "GET {} HTTP/1.1\r\nHost: {}\r\n\r\n".format(path, host)
        print(payload)
        self.sendall(payload)

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
