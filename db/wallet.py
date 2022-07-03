from uuid import uuid4


class Wallet:
    def __init__(self):
        self.wallets = {}

    def find(self):
        return self.wallets

    def findOne(self, id):
        return self.wallets[id]

    def create(self, name, address, privateKey):
        wallet = {
            "id": str(uuid4()),
            "name": name,
            "address": address,
            "privateKey": privateKey,
        }
        self.wallets[wallet["id"]] = wallet
        return wallet

    def delete(self, id):
        del self.wallets[id]
