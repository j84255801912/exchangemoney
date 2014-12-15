#!/usr/bin/python

import argparse
from bitcoinrpc.connection import BitcoinConnection

user = 'abc123'
password = 'def456'
port = '18332'

class getkeys(object):
    def __init__(self, address):
        self.keys = {
                    'address' : address.encode('utf-8'),
                    'pubkey'  : None,
                    'privkey' : None
                    }
        bitcoin = BitcoinConnection(user=user, password=password, port=port)

        # fetch pubkey
        try:
            vr = bitcoin.validateaddress(address).__dict__
        except Exception, e:
            print "Caught: ", e
            sys.exit(1)
        # validate address
        if vr['isvalid'] is False:
            raise ValueError('Address is not valid')
        elif vr['ismine'] is False:
            raise ValueError('Address is not yours')
        self.keys['pubkey'] = vr['pubkey'].encode('utf-8')

        # fetch privkey
        try:
            dr = bitcoin.dumpprivkey(address)
        except Exception, e:
            print "Caught: ", e
            sys.exit(1)
        self.keys['privkey'] = dr.encode('utf-8')

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Get pubkeys and privkeys from the address in your wallet.')
    argparser.add_argument("address", help="bitcoin address", default="")
    args = argparser.parse_args()
    hw = getkeys(args.address)
    print hw.keys
