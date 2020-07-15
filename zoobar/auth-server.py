#!/usr/bin/python

import rpclib
import sys
# import auth
from debug import *
from zoodb import *
import random,hashlib

def newtoken(db, cred):
    hashinput = "%s%.10f" % (cred.password, random.random())
    cred.token = hashlib.md5(hashinput).hexdigest()
    db.commit()
    return cred.token

class AuthRpcServer(rpclib.RpcServer):
    ## Fill in RPC methods here.
    
    def rpc_login(self,username, password):
        db = cred_setup()
        cred = db.query(Cred).get(username)
        if not cred:
            return None
        if cred.password == password:
            return newtoken(db, cred)
        else:
            return None

    def rpc_register(self,username, password):
        db = cred_setup()
        cred = db.query(Cred).get(username)
        if cred:
            return None
        newcred = Cred()
        newcred.username = username
        newcred.password = password
        db.add(newcred)
        db.commit()
        return newtoken(db, newcred)

    def rpc_check_token(self,username, token):
        db = cred_setup()
        cred = db.query(Cred).get(username)
        if cred and cred.token == token:
            return True
        else:
            return False

(_, dummy_zookld_fd, sockpath) = sys.argv

s = AuthRpcServer()
s.run_sockpath_fork(sockpath)
