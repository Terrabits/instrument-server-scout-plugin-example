from socket import socket


# constants
SERVER_ADDRESS = ('localhost', 9000)
EMPTY_LIST     = '[]'

# connect
client = socket()
client.connect(SERVER_ADDRESS)

# init
client.sendall(b'init\n')

# is error?
client.sendall(b'errors?\n')
errors = client.recv(1024).strip().decode()
if errors != EMPTY_LIST:
    print('Error(s) occurred:')
    print(errors)
