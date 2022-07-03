from flask import Flask, render_template, request, abort, redirect, url_for
from random import randint
import config
from db import walletDb
from chain.eth import Eth

app = Flask(__name__)
eth = Eth(config)


@app.route("/")
def index():
    wallets = [*walletDb.find().values()]
    for wallet in wallets:
        wallet["balance"] = eth.getBalance(wallet)
    return render_template("index.html", wallets=wallets)


@app.get("/wallet/<id>/send")
def showSendForm(id):
    wallet = walletDb.findOne(id)
    return render_template("send-form.html", senderAddress=wallet["address"])


@app.post("/wallet/<id>/send")
def sendTransaction(id):
    wallet = walletDb.findOne(id)
    if wallet is None:
        abort(404)

    eth.send(wallet, request.form["receiverAddress"], float(request.form["amount"]))
    return redirect(url_for("index"))


@app.post("/wallet")
def createWallet():
    name = request.form.get("name", "wallet" + str(randint(1, 1000)))
    account = eth.createAccount()
    walletDb.create(name, account.address, account.privateKey)
    return redirect(url_for("index"))


@app.post("/wallet/add")
def addWallet():
    walletDb.create(
        request.form["name"], request.form["address"], request.form["privateKey"]
    )
    return redirect(url_for("index"))


# delete is not supported in html
@app.post("/wallet/<id>/delete")
def deleteWallet(id):
    print(walletDb.find())
    walletDb.delete(id)
    return redirect(url_for("index"))
