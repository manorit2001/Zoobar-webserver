from debug import *
from zoodb import *
import rpclib

def login(username, password):
    with rpclib.client_connect('/authsvc/sock') as c:
        ret=c.call('login',username=username,password=password)
        return ret
    ## Fill in code here.

def register(username, password):
    with rpclib.client_connect('/authsvc/sock') as c:
        ret=c.call('register',username=username,password=password)
        if(ret!=None):
            db = person_setup()        
            newperson = Person()
            newperson.username=username
            db.add(newperson)
            db.commit()
            with rpclib.client_connect('/banksvc/sock') as s:
                s.call('createacc',username=username)
        return ret
    ## Fill in code here.

def check_token(username, token):
    with rpclib.client_connect('/authsvc/sock') as c:
        ret=c.call('check_token',username=username,token=token)
        return ret
    ## Fill in code here.
