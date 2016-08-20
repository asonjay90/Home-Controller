import SimpleHTTPServer
import SocketServer
import os

PORT = 88
PATH = "/home/jason/Home-Controller/Front-End"

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

os.chdir(PATH)

print "serving at port", PORT
httpd.serve_forever()
