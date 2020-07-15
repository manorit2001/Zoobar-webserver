from zoodb import *
from debug import *
import rpclib

import time

sock="/banksvc/sock"
def transfer(sender, recipient, zoobars,token):
    with rpclib.client_connect(sock) as c:
        ret=c.call("transfer",sender=sender,recipient=recipient,zoobars=zoobars,token=token)
        return ret

def balance(username):
    with rpclib.client_connect(sock) as c:
        ret=c.call("balance",username=username)
        return ret

def get_log(username):
    # db=transfer_setup()
    # return db.query(Transfer).filter(or_(Transfer.sender==username,Transfer.recipient==username))
    with rpclib.client_connect(sock) as c:
        ret=c.call("get_log",username=username)
        return ret

