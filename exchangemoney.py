#!/usr/bin/python

import argparse
import json
import sys

from bitcoinrpc.connection import BitcoinConnection

from createmultisig import createmultisig
from waitfordeposit import waitfordeposit

user = 'abc123'
password = 'def456'
port = '18332'

feeRate = 0.01
'''
 sceranio : after createmultisig address, keep querying whether A & B for their deposit to this address.
            if they did, exchange their funds.
            else return the funds.
'''
class exchangemoney(object):
    def __init__(self, AKeys, BKeys, CKeys, multisigAddress, state):
        bitcoin = BitcoinConnection(user=user, password=password, port=port)

        # create txs for return funds
        if state['success'] is True:
        # refer A's output to B

            # count the output value deduct the fee.
            outputValue = state['txA']['value'] / float(1 + feeRate) #

            rawTxToB_Txin = [
                        {   "txid"          : state['txA']['txid'],
                            "vout"          : 0,
                            "scriptPubKey"  : state['txA']['scriptPubKey'],
                            "redeemScript"  : multisigAddress['redeemScript']
                        }
                       ]
            rawTxToB_Txout = {
                            BKeys['address'] : outputValue
                            }
            # get rawTx's hex
            rawTxToB_Hex = bitcoin.createrawtransaction(rawTxToB_Txin, rawTxToB_Txout, state['txA']['color']).encode('utf-8')
            # sign by C
            rawTxToB_SignedByC = bitcoin.signrawtransaction(rawTxToB_Hex, rawTxToB_Txin, [CKeys['privkey']])['hex'].encode('utf-8')

        # refer B's output to A

            # count the output value deduct the fee.
            outputValue = state['txB']['value'] / float(1 + feeRate) #

            rawTxToA_Txin = [
                        {   "txid"          : state['txB']['txid'],
                            "vout"          : 0,
                            "scriptPubKey"  : state['txB']['scriptPubKey'],
                            "redeemScript"  : multisigAddress['redeemScript']
                        }
                       ]
            rawTxToA_Txout = {
                            AKeys['address'] : outputValue
                        }
            # get rawTx's hex
            rawTxToA_Hex = bitcoin.createrawtransaction(rawTxToA_Txin, rawTxToA_Txout, state['txB']['color']).encode('utf-8')
            # sign by C
            rawTxToA_SignedByC = bitcoin.signrawtransaction(rawTxToA_Hex, rawTxToA_Txin, [CKeys['privkey']])['hex'].encode('utf-8')
            self.ret = {
                    "HexTxToA" : rawTxToA_SignedByC,
                    "HexTxToB" : rawTxToB_SignedByC
                        }
        # return these txs back to A and B
'''
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
    hw = exchangemoney(AKeys, BKeys)
'''
