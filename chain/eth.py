from web3 import Web3


class Eth:
    def __init__(self, config):
        self.web3 = Web3(Web3.HTTPProvider(config.ETH_NODE_URL)).eth

    def createAccount(self):
        return self.web3.account.create()

    def send(self, wallet, receiverAddress, amount):
        # get the nonce.  Prevents one from sending the transaction twice
        nonce = self.web3.getTransactionCount(wallet["address"])
        print(self.web3.gas_price)
        # build a transaction in a dictionary
        tx = {
            "nonce": nonce,
            "from": wallet["address"],
            "to": receiverAddress,
            "value": Web3.toWei(amount, "ether"),
            "gas": 21000,
            "maxFeePerGas": Web3.toWei(10, "gwei"),
            "maxPriorityFeePerGas": self.web3.max_priority_fee,
            "chainId": 4,
        }

        # sign the transaction
        signedTx = self.web3.account.sign_transaction(tx, wallet["privateKey"])

        # send transaction
        txHash = self.web3.sendRawTransaction(signedTx.rawTransaction)
        txReceipt = self.web3.wait_for_transaction_receipt(txHash)
        print(txReceipt)

        # get transaction hash
        return Web3.toHex(txHash)

    def getBalance(self, wallet):
        return Web3.fromWei(self.web3.get_balance(wallet["address"]), "ether")
