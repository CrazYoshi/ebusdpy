
import socket

READ_COMMAND = 'read -m {2} -c {0} {1}\n'
WRITE_COMMAND = 'write -c {0} {1} {2}\n'

class SocketTimeout(Exception):
   """Socket timeout exception"""
   pass

class SocketError(Exception):
   """Socket error exception"""
   pass

def init(address):
    try:
        """ Open the socket at the specified address, call the command sent and return data """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(address)
    except socket.timeout:
        raise SocketTimeout(socket.timeout)
    except socket.error:
        raise SocketError(socket.error)
    finally:
        sock.close()

def read(address, circuit, name, ttl):
    result = None
    try:
        """ Open the socket at the specified address, call the command sent and return data """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(address)
        """ Send the command """
        command = READ_COMMAND.format(circuit, name, ttl)
        sock.sendall(command.encode())
        """ Get the result decoded UTF-8 """
        result = sock.recv(256).decode('utf-8').rstrip()
    except socket.timeout:
        raise SocketTimeout(socket.timeout)
    except socket.error:
        raise SocketError(socket.error)
    finally:
        sock.close()
    return result

def write(address, circuit, name, value):
    result = None
    try:
        """ Open the socket at the specified address, call the command sent and return data """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(address)
        """ Send the command """
        command = WRITE_COMMAND.format(circuit, name, value)
        sock.sendall(command.encode())
        """ Get the result decoded UTF-8 """
        result = sock.recv(256).decode('utf-8').rstrip()
    except socket.timeout:
        raise SocketTimeout(socket.timeout)
    except socket.error:
        raise SocketError(socket.error)
    finally:
        sock.close()
    return result
