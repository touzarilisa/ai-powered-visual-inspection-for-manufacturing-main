from threading import Thread
import os 
import sys

cwd = os.getcwd()
sys.path.append(cwd + '/./grpc/')
from grpc_server import RgbImageServicer

cwd = os.getcwd()
sys.path.append(cwd + '/./gui/')
from qml_connector import main as qml_main

class grpc_server(Thread):
    def __init__(self,ip_address, port):
        Thread.__init__(self)
        self.ip_address = ip_address
        self.port = port
        self.server = RgbImageServicer()
        self.server.start(ip_address, port)
        self.running = True

    def run(self):
        self.server.loop()

    def stop(self):
        self.server.stop()
        self.running = False


class grpc_client(Thread):
    def __init__(self,ip_address, port):
        Thread.__init__(self)
        self.ip_address = ip_address
        self.port = port
        self.running = True
       
    def run(self):        
        # Execute main function with arguments
        qml_main()

    def stop(self):
        self.running = False
    


if __name__ == '__main__':

    a = grpc_server('localhost', '50051')
    a.start()

    b = grpc_client('localhost', '50051')
    b.start()

    a.join()
    b.join()







