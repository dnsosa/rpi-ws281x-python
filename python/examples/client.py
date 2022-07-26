import socket
import threading
import time
import encodings

HOST = '10.30.23.124'
#HOST = '10.30.1.232'
PORT = 65433

def my_client():
    threading.Timer(3, my_client).start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Trying to connect...")
        s.connect((HOST, PORT))
        inp = input("Enter Command ")
        inp_enc = inp.encode('utf-8')
        s.sendall(inp_enc)
        while True:
            data = s.recv(1024).decode('utf-8')
            print(data)
            
        s.close()
        # time.sleep(5)

if __name__ == '__main__':
    while 1:
        my_client()
