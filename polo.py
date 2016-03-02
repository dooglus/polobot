#!/usr/bin/env python

import poloniex, sys, json

p = poloniex.poloniex('put your API key here', 'put your API secret here')

def turnOffAutoRenew():
    for loan in p.returnActiveLoans()['provided']:
        if loan['autoRenew']:
            id = loan['id']
            print id, p.toggleAutoRenew(id)

def turnOnAutoRenew():
    for loan in p.returnActiveLoans()['provided']:
        if not loan['autoRenew']:
            id = loan['id']
            print id, p.toggleAutoRenew(id)

def pp(x):
    print json.dumps(x, indent = 2)

# print p.returnAvailableAccountBalances()
# th = p.returnTradeHistory("BTC_CLAM", 1455482888, 1455569288)
# pp(th)

# turnOffAutoRenew()
turnOnAutoRenew()
