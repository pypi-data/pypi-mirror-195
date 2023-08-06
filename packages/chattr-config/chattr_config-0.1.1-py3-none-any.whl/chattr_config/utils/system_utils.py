from functools import lru_cache
import os
import socket


@lru_cache()
def get_ip_address():
    try:
        ip_address = socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        ip_address = '127.0.0.1'

    return ip_address


@lru_cache()
def get_fqdn():
    return socket.getfqdn()


@lru_cache()
def get_process_id():
    return os.getpid()


@lru_cache()
def get_machine_info():
    return {'ip_address': get_ip_address(), 'fully_qualified_domain_name': get_fqdn(), 'process_id': get_process_id()}
