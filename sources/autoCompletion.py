#!/usr/bin/python3
#
# autoCompletion.py for Auto completion in /home/jean.walrave/projects/epitech/autoCompletion_2016/sources
#
# Made by Jean Walrave
# Login	 <jean.walrave@epitech.net>
#
# Started on	Thu Jul	6 08:11:12 2017 Jean Walrave
# Last update	Thu Jul	6 08:11:12 2017 Jean Walrave
#

import os
import sys
import argparse

from completion import Completion
from address import Address


ERR_MSG_INVALID_ARGUMENT = 'Invalid argument'

def eprint(*args, **kwargs):
    print (*args, file=sys.stderr, **kwargs)

class AutoCompletion(object):
    def __init__(self):
        # parse program arguments
        args = self.parse_args()
        addresses = self.read_addresses_dictionnary(args.dictionnary)

        if not addresses:
            AutoCompletion.quit_invalid_argument()

        Completion(addresses).do_completion()

        sys.exit(0)

    @staticmethod
    def quit_invalid_argument():
        eprint (ERR_MSG_INVALID_ARGUMENT)

        sys.exit(84)

    def parse_args(self):
        def _check_dictionnary(path):
            if not os.path.isfile(path):
                AutoCompletion.quit_invalid_argument()

            return (path)

        args = sys.argv[1:]

        if not args:
            AutoCompletion.quit_invalid_argument()

        parser = argparse.ArgumentParser()
        parser.add_argument('dictionnary', help='file, containing one address per line, serving as knowledge base', type=_check_dictionnary)

        return (parser.parse_args(args))

    def read_addresses_dictionnary(self, addresses_dictionnary_file):
        addresses = []

        with open(addresses_dictionnary_file) as adf:
            for l in adf.readlines():
                address = l.strip()

                if not Address.is_valid_address(address):
                    eprint (address)
                else:
                    addresses.append(Address(address))

        return (addresses)

AutoCompletion()
