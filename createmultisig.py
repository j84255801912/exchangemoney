#!/usr/bin/python

import argparse
import json
import sys

from bitcoinrpc.connection import BitcoinConnection
from getkeys import getkeys

user = 'abc123'
password = 'def456'
port = '18332'

class createmultisig(object):
    def returnkeys(self):
        bitcoin = BitcoinConnection(user=user, password=password, port=port)
        AKeys = self.AKeys
        BKeys = self.BKeys

        # get C's address, pubkey, privkey
        try:
            addressC = bitcoin.getnewaddress()
        except Exception, e:
            print "Caught: ", e
            sys.exit(1)
        CKeys = getkeys(addressC).keys

        # addmultisig address made of A, B, C
        # use addmultisigaddress instead of createmultisig is due to
        # the fact that we can use listunspent to track this address.
        try:
            addr = bitcoin.addmultisigaddress(2, [AKeys['pubkey'], BKeys['pubkey'], CKeys['pubkey']]).encode('utf-8')
        except Exception, e:
            print "Caught: ", e
            sys.exit(1)

        # fetch the redeemScript for this multisigaddress
        try:
            vr = bitcoin.validateaddress(addr).__dict__
        except Exception, e:
            print "Caught: ", e
            sys.exit(1)
        multisigAddress = {
                            "address"       : addr,
                            "redeemScript"  : vr['hex'].encode('utf-8'),
                           }
        return multisigAddress, CKeys
    def __init__(self, AKeys, BKeys):
        self.AKeys = AKeys
        self.BKeys = BKeys
if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='create multisig address and return CKeys')
    argparser.add_argument("addressA", help="bitcoin address A", default="")
    argparser.add_argument("pubkeyA", help="bitcoin public key A", default="")
    argparser.add_argument("addressB", help="bitcoin address B", default="")
    argparser.add_argument("pubkeyB", help="bitcoin public key B", default="")
    args = argparser.parse_args()
    AKeys = {
                "address"   : args.addressA,
                "pubkey"    : args.pubkeyA,
            }
    BKeys = {
                "address"   : args.addressB,
                "pubkey"    : args.pubkeyB,
            }
    args = argparser.parse_args()
    hw = createmultisig(AKeys, BKeys)
