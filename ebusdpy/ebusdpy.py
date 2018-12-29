
import socket

from .const import (SENSOR_TYPES)

def init(address):
    try:
        """ Open the socket at the specified address, call the command sent and return data """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(address)
    except socket.timeout:
        raise socket.timeout(socket.timeout)
    except socket.error:
        raise socket.error(socket.error)
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
        READ_COMMAND = 'read -m {2} -c {0} {1}\n'
        command = READ_COMMAND.format(circuit, name, ttl)
        sock.sendall(command.encode())
        """ Get the result decoded UTF-8 """
        result = sock.recv(256).decode('utf-8').rstrip()
        result = humanize(circuit, name, result)
    except socket.timeout:
        raise socket.timeout(socket.timeout)
    except socket.error:
        raise socket.error(socket.error)
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
        WRITE_COMMAND = 'write -c {0} {1} {2}\n'
        command = WRITE_COMMAND.format(circuit, name, value)
        sock.sendall(command.encode())
        """ Get the result decoded UTF-8 """
        result = sock.recv(256).decode('utf-8').rstrip()
    except socket.timeout:
        raise socket.timeout(socket.timeout)
    except socket.error:
        raise socket.error(socket.error)
    finally:
        sock.close()
    return result

def timer_format(string):
    """Datetime formatter."""
    _r = []
    _s = string.split(';')
    for i in range(0, len(_s) // 2):
        if(_s[i * 2] != '-:-' and _s[i * 2] != _s[(i * 2) + 1]):
            _r.append(_s[i * 2] + '/' + _s[(i * 2) + 1])
    return ' - '.join(_r)

def humanize(circuit, name, value):
    _state = None
    _type = SENSOR_TYPES[circuit][name]
    if _type == 0:
        _state = format(
            float(value), '.1f')
    elif _type == 1:
        _state = timer_format(value)
    elif _type == 2:
        if value == 1:
            _state = 'on'
        else:
            _state = 'off'
    elif _type == 3:
        _state = value
    elif _type == 4:
        if 'ok' not in value.split(';'):
            return
        _state = value.partition(';')[0]
    return _state