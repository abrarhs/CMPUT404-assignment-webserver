#  coding: utf-8 
import socketserver
import os.path, os

# Copyright 2023 Abrar Hussain, Abram Hindle, Eddie Antonio Santos
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):

        self.data = self.request.recv(1024).strip()
        decoded = self.data.split(b"\r\n") # split header 
        command = decoded[0].split(b" ")[0].decode("utf-8") # split 'GET /'
        location =  decoded[0].split(b" ")[1].decode("utf-8") # split '/'
        path = ''

        if command != "GET": # only GET requests are allowed
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n",'utf-8'))
            return
        else: # if it is a GET request
            if "css" not in location and "index.html" not in location:
                if location[-1] == "/": # check if in parent directory
                        location = location + "index.html" # update path to index.html
                else: # if not in parent directory
                        # file moved send 301 code
                    self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation:" + location +'/' +"\r\n",'utf-8'))
                    return
        
        path = "./www" + location # update path

        if ".html" in location:
            if os.path.isfile(path):
                file = open(path,'r')
                contents = file.read()
                self.request.sendall(bytearray('HTTP/1.1 200 OK\r\n'+"Content-Type:" +'text/html' +"\r\n" + contents,'utf-8'))
                return
            else:
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
                return
        elif ".css" in location:
            if os.path.isfile(path):
                file = open(path,'r')
                contents = file.read()
                self.request.sendall(bytearray('HTTP/1.1 200 OK\r\n'+"Content-Type:" +'text/css' +"\r\n" + contents + "\r\n",'utf-8'))
                return
            else:
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
                return

        print ("Got a request of: %s\n" % self.data)
        self.request.sendall(bytearray("OK",'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
