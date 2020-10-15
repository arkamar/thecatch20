# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.4 (default, Jul 13 2020, 21:16:07) 
# [GCC 9.3.0]
# Embedded file name: fake_client.py
"""
The Catch 2020 - Botnet client in "Downloaded file"
Fake file
"""
import sys
from time import sleep
__author__ = 'Aleš Padrta @ CESNET.CZ'
__version__ = '1.0'

def main():
    """
        Main function
        """
    if sys.version_info[0] < 3:
        print('ERROR: Python3 required.')
        exit(1)
    outtext = 'Connection failed, try again  '
    sleep(5)
    print('{}'.format(outtext))


main()
