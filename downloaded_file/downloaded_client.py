# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.4 (default, Jul 13 2020, 21:16:07) 
# [GCC 9.3.0]
# Embedded file name: downloaded_client.py
"""
The Catch 2020 - Botnet client in "Downloaded file"
Client
"""
import sys, argparse, pyaes
__author__ = 'Aleš Padrta @ CESNET.CZ'
__version__ = '1.0'

def get_args():
    """
        Cmd line argument parsing (preprocessing)
        """
    parser = argparse.ArgumentParser(description='FT2-Botnet: Client')
    parser.add_argument('-ip', '--ipaddress', type=str, help='Server IP address', required=True)
    parser.add_argument('-p', '--port', type=int, help='Server port', required=True)
    args = parser.parse_args()
    return (
     args.ipaddress, args.port)


def get_key(srv_ip, srv_port):
    """
        Create key according to defined parameters
        """
    key_base = b"\xfdd\xe2\x95\x86\x14'9\xfb\x15\x82\xdb|\xc2=\xe7\xf0BT\xd3\x17`:\xeb\x97\x93"
    aeskey = key_base
    for octet in srv_ip.split('.'):
        aeskey = aeskey + int(octet).to_bytes(1, byteorder='big')

    aeskey = aeskey + srv_port.to_bytes(2, byteorder='big')
    return aeskey


def get_msg(key):
    """
        Create return message
        """
    encmsg = b"\xce\xedC\xa7\xe3\xf8\xc8U\xd0d'&cQ\x00py\x88\x8e\x1c \x0c\xb7\x9c\x08"
    aes = pyaes.AESModeOfOperationCTR(key)
    decmsg = aes.encrypt(encmsg)
    try:
        if 'FLAG' not in decmsg.decode():
            return 'invalid parameters'
    except Exception as excdesc:
        return 'invalid parameters'

    return decmsg.decode()


def main():
    """
        Main function
        """
    if sys.version_info[0] < 3:
        print('ERROR: Python3 required.')
        exit(1)
    srv_ip, srv_port = get_args()
    key = get_key(srv_ip, srv_port)
    msg = get_msg(key)
    print('{}'.format(msg))


main()
# okay decompiling client_extracted/downloaded_client.pyc
