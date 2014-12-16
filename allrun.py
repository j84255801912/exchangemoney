#!/usr/bin/python

import argparse
import json
import sys

from bitcoinrpc.connection import BitcoinConnection

from createmultisig import createmultisig
from waitfordeposit import waitfordeposit
from exchangemoney import exchangemoney

user = 'abc123'
password = 'def456'
port = '18332'

feeRate = 0.01
'''
 sceranio : after createmultisig address, keep querying whether A & B for their deposit to this address.
            if they did, exchange their funds.
            else return the funds.
'''
class allrun(object):
    def __init__(self, AKeys, BKeys):
        bitcoin = BitcoinConnection(user=user, password=password, port=port)

        # get keys
        multisig = createmultisig(AKeys, BKeys)
        multisigAddress = multisig.multisigAddress
        CKeys = multisig.CKeys

        # wait for deposit
        state = waitfordeposit(multisigAddress, AKeys, BKeys).state
        
        # do exchange
        ret = exchangemoney(AKeys, BKeys, CKeys, multisigAddress, state).ret
        # return these txs back to A and B
        print ret
if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Get pubkeys and privkeys from the address in your wallet.')
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
    hw = allrun(AKeys, BKeys)
