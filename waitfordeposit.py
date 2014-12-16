from bitcoinrpc.connection import BitcoinConnection

user = 'abc123'
password = 'def456'
port = '18332'

class waitfordeposit(object):
    def __init__(self, multisigAddress, AKeys, BKeys):
        bitcoin = BitcoinConnection(user=user, password=password, port=port)
        '''
        - need to verify
            1. address
            2. value
            3. comfirmations
        - need to record
            1. scriptPubKey
            2. value
        '''
        txidA = "2c4bbd08ce27702cd04ff69819ab44c4dd24d8f424fc91cbe9aa4acbe0997795"
        scriptPubKeyA = "a9148e373ae21e902662561dab6de709d20121dcd19487"
        valueA = float(100)
        colorA = int(0)

        txidB = "2c4bbd08ce27702cd04ff69819ab44c4dd24d8f424fc91cbe9aa4acbe0997795"
        scriptPubKeyB = "a9148e373ae21e902662561dab6de709d20121dcd19487"
        valueB = float(100)
        colorB = int(0)

        self.state = {
                "success"   : True,
                "txA"       :
                                {
                                    "txid"          : txidA,
                                    "scriptPubKey"  : scriptPubKeyA,
                                    "value"         : valueA,
                                    "color"         : colorA
                                },
                "txB"       :
                                {
                                    "txid"          : txidB,
                                    "scriptPubKey"  : scriptPubKeyB,
                                    "value"         : valueB,
                                    "color"         : colorB
                                }
                }
