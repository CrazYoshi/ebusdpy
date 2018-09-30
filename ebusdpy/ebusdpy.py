
import socket

def send_command(address, command):
    result = None
    try:
        """ Open the socket at the specified address, call the command sent and return data """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(address)
        """ Send the command """
        sock.sendall(command.encode())
	    """ Get the result decoded UTF-8 """
        result = sock.recv(256).decode('utf-8').rstrip()
    except socket.timeout:
        raise RuntimeError(socket.timeout)
    except socket.error:
        raise RuntimeError(socket.error)
	finally:
        sock.close()
    return result
