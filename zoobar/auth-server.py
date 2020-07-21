#!/usr/bin/python

import rpclib
import sys
# import auth
from debug import *
from zoodb import *
import random,hashlib
import pbkdf2
from base64 import b64encode

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
        if cred.password == pbkdf2.PBKDF2(password,cred.salt).hexread(32):
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
        newcred.salt = b64encode(os.urandom(64).strip()).decode("UTF-8")
        newcred.password = pbkdf2.PBKDF2(password,newcred.salt).hexread(32)
        db.add(newcred)
        db.commit()
        return newtoken(db, newcred)

    def rpc_check_token(self,username, token):
        db = cred_setup()
        cred = db.query(Cred).get(username)
        if cred and cred.token == token:
            return True
        else:
            print("cred.token:",cred.token)
            print("token:",token)
            return False

(_, dummy_zookld_fd, sockpath) = sys.argv

s = AuthRpcServer()
s.run_sockpath_fork(sockpath)
