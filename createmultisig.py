#!/usr/bin/python

import argparse
import json
import sys

from bitcoinrpc.connection import BitcoinConnection

user = 'abc123'
password = 'def456'
port = '18332'

class getkeys(object):
    def __init__(self, reqSig, pubkey1, pubkey2):
        bitcoin = BitcoinConnection(user=user, password=password, port=port)

        keys = [pubkey1, pubkey2]
        try:
            cr = bitcoin.createmultisig(reqSig, keys)
        except Exception, e:
            print "Caught: ", e
            sys.exit(1)
        print cr
if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='')
    argparser.add_argument("reqSig", help="signature required to spent this address' money", default="")
    argparser.add_argument("pubkey1", help="bitcoin public key 1", default="")
    argparser.add_argument("pubkey2", help="bitcoin public key 2", default="")
    args = argparser.parse_args()
    hw = getkeys(int(args.reqSig), args.pubkey1, args.pubkey2)
