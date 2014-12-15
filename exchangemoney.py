#!/usr/bin/python

import argparse
import json
import sys

from bitcoinrpc.connection import BitcoinConnection

from getkeys import getkeys

user = 'abc123'
password = 'def456'
port = '18332'

'''
 sceranio : after createmultisig address, keep querying whether A & B for their deposit to this address.
            if they did, exchange their funds.
            else return the funds.
'''
class ExchangeMoney(object):
    def create_multisig(self, bitcoin, reqSig, keys):
        try:
            cr = bitcoin.addmultisigaddress(reqSig, keys)
        except Exception, e:
            print "Caught: ", e
            sys.exit(1)
        return cr

    def waiting_for_deposit(self, bitcoin, multisigAddress):
        print "\nThis section is for confirming deposit"
        return ("txidA", "txidB",)

    def create_raw_tx(self, bitcoin):
        return "rawtx_hex"

    def __init__(self, pubkey1, pubkey2):
        bitcoin = BitcoinConnection(user=user, password=password, port=port)

        # get C's address, pubkey, privkey
        try:
            addressC = bitcoin.getnewaddress()
        except Exception, e:
            print "Caught: ", e
            sys.exit(1)
        Ckeys = getkeys(addressC).keys

        # addmultisig address made of A, B, C
        # use addmultisigaddress instead of createmultisig is due to
        # the fact that we can use listunspent to track this address.
        addr = self.create_multisig(bitcoin, 2, [pubkey1, pubkey2, Ckeys['pubkey']])

        # fetch the redeemScript for this multisigaddress
        try:
            vr = bitcoin.validateaddress(addr).__dict__
        except Exception, e:
            print "Caught: ", e
            sys.exit(1)
        multisigAddress = {
                            "address"       : addr.encode('utf-8'),
                            "redeemscript"  : vr['hex'].encode('utf-8')
                           }

        # wait for deposit
        (txidA, txidB,) = self.waiting_for_deposit(bitcoin, multisigAddress)

        # create txs for return funds

        # sign txs

        # return these txs back to A and B

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Get pubkeys and privkeys from the address in your wallet.')
    argparser.add_argument("pubkey1", help="bitcoin public key 1", default="")
    argparser.add_argument("pubkey2", help="bitcoin public key 2", default="")
    args = argparser.parse_args()
    hw = ExchangeMoney(args.pubkey1, args.pubkey2)
