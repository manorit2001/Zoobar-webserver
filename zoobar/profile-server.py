#!/usr/bin/python

import rpclib
import sys
import os
import sandboxlib
import urllib
import hashlib
import socket
import bank
import zoodb

from debug import *

## Cache packages that the sandboxed code might want to import
import time
import errno
#from zoodb import *

class ProfileAPIServer(rpclib.RpcServer):
    def __init__(self, user, visitor):
        self.user = user
        self.visitor = visitor
        db=zoodb.cred_setup()
        cred = db.query(zoodb.Cred).get(user)
        self.token=cred.token

    def rpc_get_self(self):
        return self.user

    def rpc_get_visitor(self):
        return self.visitor

    def rpc_get_xfers(self, username):
        xfers = []
        for xfer in bank.get_log(username):
            xfers.append({ 'sender': xfer["sender"],
                           'recipient': xfer["recipient"],
                           'amount': xfer["amount"],
                           'time': xfer["time"],
                         })
        print(xfers)
        return xfers

    def rpc_get_user_info(self, username):
        person_db = zoodb.person_setup()
        p = person_db.query(zoodb.Person).get(username)
        if not p:
            return None
        return { 'username': p.username,
                 'profile': p.profile,
                 'zoobars': bank.balance(username),
               }

    def rpc_xfer(self, target, zoobars):
        print(self.token)
        bank.transfer(self.user, target, zoobars, self.token)

def run_profile(pcode, profile_api_client):
    globals = {'api': profile_api_client}
    exec pcode in globals

class ProfileServer(rpclib.RpcServer):
    def rpc_run(self, pcode, user, visitor):
        uid = 61020
        db=zoodb.uid_setup()
        uid += db.query(zoodb.UID).filter_by(username=user).first().id

        userdir = '/tmp/'+hashlib.sha256(user.encode()).hexdigest()
        if(not os.path.isdir(userdir)):
            os.makedirs(userdir)
            os.chown(userdir,uid,uid)

        (sa, sb) = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM, 0)
        pid = os.fork()
        if pid == 0:
            if os.fork() <= 0:
                sa.close()
                ProfileAPIServer(user, visitor).run_sock(sb)
                sys.exit(0)
            else:
                sys.exit(0)
        sb.close()
        os.waitpid(pid, 0)

        sandbox = sandboxlib.Sandbox(userdir, uid, '/profilesvc/lockfile')
        with rpclib.RpcClient(sa) as profile_api_client:
            return sandbox.run(lambda: run_profile(pcode, profile_api_client))

(_, dummy_zookld_fd, sockpath) = sys.argv

s = ProfileServer()
s.run_sockpath_fork(sockpath)
