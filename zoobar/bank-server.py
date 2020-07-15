#!/usr/bin/python
#
# Insert bank server code here.
#
import rpclib
import sys
from zoodb import *
from debug import *
import time

class BankRpcServer(rpclib.RpcServer):
    def rpc_createacc(self,username):
        bankdb = bank_setup()
        bank= Bank()
        bank.username=username
        bank.zoobars=10
        bankdb.add(bank)
        bankdb.commit()
    def rpc_transfer(self,sender, recipient, zoobars,token):
        with rpclib.client_connect('/authsvc/sock') as c:
            ret = c.call('check_token',username=sender,token=token)
            if(ret==False):
                raise Exception("Token error")
        bankdb = bank_setup()
        senderp = bankdb.query(Bank).get(sender)
        recipientp = bankdb.query(Bank).get(recipient)

        sender_balance = senderp.zoobars - zoobars
        recipient_balance = recipientp.zoobars + zoobars

        if sender_balance < 0 or recipient_balance < 0:
            raise ValueError()

        senderp.zoobars = sender_balance
        recipientp.zoobars = recipient_balance
        bankdb.commit()

        transfer = Transfer()
        transfer.sender = sender
        transfer.recipient = recipient
        transfer.amount = zoobars
        transfer.time = time.asctime()

        transferdb = transfer_setup()
        transferdb.add(transfer)
        transferdb.commit()

    def rpc_balance(self,username):
        db = bank_setup()
        bank = db.query(Bank).get(username)
        return bank.zoobars

    def rpc_get_log(self,username):
        db = transfer_setup()
        x=[]
        for i in db.query(Transfer).filter(or_(Transfer.sender==username,Transfer.recipient==username)):
            temp=i.__dict__
            del temp['_sa_instance_state']
            x+=[temp]
        return x
(_,dummy_zookld_fd,sockpath) = sys.argv
s = BankRpcServer()
s.run_sockpath_fork(sockpath)
        


