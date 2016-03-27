#!/usr/bin/env python

import poloniex, sys, json, time

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

def usage():
    print "on off bal hist newaddr wd"

if len(sys.argv) < 2:
    usage()
elif sys.argv[1] == 'on':
    turnOnAutoRenew()
elif sys.argv[1] == 'off':
    turnOffAutoRenew()
elif sys.argv[1] == 'bal':
    b = p.returnAvailableAccountBalances()
    for a in b:
        for k in b[a]:
            if k != 'BTM' and b[a][k] != "0.00000000":
                print "%10s: %12s %s" % (a, b[a][k], k)
elif sys.argv[1] == 'h' or sys.argv[1] == 'hist' or sys.argv[1] == 'history':
    print time.ctime(p.returnDepositsWithdrawals(time.time() - 24*3600*4, time.time())['withdrawals'][-1]['timestamp'])
elif sys.argv[1] == 'newaddr':
    if len(sys.argv) == 3:
        ret = p.generateNewAddress(sys.argv[2])
        if ret.has_key('address'):
            print ret['address']
        else:
            print ret['response']
    else:
        print "newaddr <currency>"
elif sys.argv[1] == 'wd': # wd 2.3 BTC 1address
    amount   = sys.argv[2]
    currency = sys.argv[3]
    address  = sys.argv[4]
    pp(p.withdraw(currency, amount, address, paymentId = None))
else:
    usage()
