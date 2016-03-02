import hashlib, hmac, json, time, urllib, urllib2

class poloniex:
    def __init__(self, APIKey = None, Secret = None):
        self.APIKey = APIKey
        self.Secret = Secret

    def public_api_query(self, url):
        return json.loads(urllib2.urlopen(urllib2.Request('https://poloniex.com/public?command=' + url)).read())

    def api_query(self, command, req = {}):
        if command == "returnTicker" or command == "return24Volume":
            return self.public_api_query(command)

        if command == "returnOrderBook":
            return self.public_api_query(command + '&currencyPair=' + str(req['currencyPair']))

        if command == "returnMarketTradeHistory":
            return self.public_api_query("returnTradeHistory" + '&currencyPair=' + str(req['currencyPair']))

        req['command'] = command
        req['nonce'] = int(time.time() * 1000)
        post_data = urllib.urlencode(req)
        return json.loads(urllib2.urlopen(urllib2.Request('https://poloniex.com/tradingApi', post_data,
                                                          {'Sign': hmac.new(self.Secret, post_data, hashlib.sha512).hexdigest(),
                                                           'Key': self.APIKey})).read())

    def returnTicker(self):
        return self.api_query("returnTicker")

    def return24Volume(self):
        return self.api_query("return24Volume")

    def returnOrderBook (self, currencyPair):
        return self.api_query("returnOrderBook", {'currencyPair': currencyPair})

    def returnMarketTradeHistory (self, currencyPair):
        return self.api_query("returnMarketTradeHistory", {'currencyPair': currencyPair})

    # returnBalances - Returns all of your available balances.
    # 
    # Sample output:
    #   {"BTC":"0.59098578",
    #    "LTC":"3.31117268",
    #     ... }
    def returnBalances(self):
        return self.api_query('returnBalances')

    # returnCompleteBalances - Returns all of your balances, including available balance, balance on orders, and the estimated BTC value of your balance.
    # 
    # Sample output:
    #   {"LTC":{"available":"5.015","onOrders":"1.0025","btcValue":"0.078"},
    #    "NXT":{...},
    #     ... }
    def returnCompleteBalances(self):
        return self.api_query('returnCompleteBalances')

    # returnDepositAddresses - Returns all of your deposit addresses.
    # 
    # Sample output:
    #   {"BTC":"19YqztHmspv2egyD6jQM3yn81x5t5krVdJ",
    #    "LTC":"LPgf9kjv9H1Vuh4XSaKhzBe8JHdou1WgUB",
    #    "ITC":"Press Generate.." ... }
    def returnDepositAddresses(self):
        return self.api_query('returnDepositAddresses')

    # generateNewAddress - Generates a new deposit address for the currency specified by the "currency" POST parameter.
    # 
    # Sample output:
    #   {"success":1,"response":"CKXbbs8FAVbtEa397gJHSutmrdrBrhUMxe"}
    # 
    # Addresses for some currencies do not generate immediately. For these, the output will be:
    #   {"success":1,"response":"Address generating."}
    # 
    # All currencies added in the future will return addresses immediately. The ones that currently don't are being changed over to the new system.
    def generateNewAddress(self, currency):
        return self.api_query('generateNewAddress', {"currency":currency})

    # returnDepositsWithdrawals - Returns your deposit and withdrawal history within a range,
    #   specified by the "start" and "end" POST parameters, both of which should be given as UNIX timestamps.
    # 
    # Sample output:
    #   {"deposits":   [{"currency":        "BTC",
    #                    "address":         "...",
    #                    "amount":          "0.01006132",
    #                    "confirmations":   10,
    #                    "txid":            "17f819a91369a9ff6c4a34216d434597cfc1b4a3d0489b46bd6f924137a47701",
    #                    "timestamp":       1399305798,
    #                    "status":          "COMPLETE"},
    #                   {"currency":        "BTC",
    #                    "address":         "...",
    #                    "amount":          "0.00404104",
    #                    "confirmations":   10, 
    #                    "txid":            "7acb90965b252e55a894b535ef0b0b65f45821f2899e4a379d3e43799604695c",
    #                    "timestamp":       1399245916,
    #                    "status":          "COMPLETE"}],
    #    "withdrawals":[{"withdrawalNumber":134933,
    #                    "currency":        "BTC",
    #                    "address":         "1N2i5n8DwTGzUq2Vmn9TUL8J1vdr1XBDFg",
    #                    "amount":          "5.00010000",
    #                    "timestamp":       1399267904,
    #                    "status":          "COMPLETE: 36e483efa6aff9fd53a235177579d98451c4eb237c210e66cd2b9a2d4a988f8e",
    #                    "ipAddress":       "..."}]}
    def returnDepositsWithdrawals(self, start, end):
        return self.api_query('returnDepositsWithdrawals', {"start":start, "end":end})

    # returnOpenOrders - Returns your open orders for a given market, specified by the "currencyPair" POST parameter,
    #   e.g. "BTC_XCP". Set "currencyPair" to "all" to return open orders for all markets.
    # 
    # Sample output for single market:
    #   [{"orderNumber":"120466",
    #     "type":"sell",
    #     "rate":"0.025",
    #     "amount":"100",
    #     "total":"2.5"},
    #    {"orderNumber":"120467",
    #     "type":"sell",
    #     "rate":"0.04",
    #     "amount":"100",
    #     "total":"4"},
    #    ... ]
    # 
    # Or, for all markets:
    # 
    #   {"BTC_1CR":[],
    #    "BTC_AC":[{"orderNumber":"120466",
    #               "type":"sell",
    #               "rate":"0.025",
    #               "amount":"100",
    #               "total":"2.5"},
    #              {"orderNumber":"120467",
    #               "type":"sell",
    #               "rate":"0.04",
    #               "amount":"100",
    #               "total":"4"}],
    #     ... }
    def returnOpenOrders(self, currencyPair):
        return self.api_query('returnOpenOrders', {"currencyPair":currencyPair})

    # returnTradeHistory - Returns your trade history for a given market, specified by the "currencyPair" POST parameter.
    #   You may specify "all" as the currencyPair to receive your trade history for all markets.
    #   You may optionally specify a range via "start" and/or "end" POST parameters, given in UNIX timestamp format.
    # 
    # Sample output:
    #   [{"date":"2014-02-19 03:44:59",
    #     "rate":"0.0011",
    #     "amount":"99.9070909",
    #     "total":"0.10989779",
    #     "orderNumber":"3048809",
    #     "type":"sell"},
    #    {"date":"2014-02-19 04:55:44",
    #     "rate":"0.0015",
    #     "amount":"100",
    #     "total":"0.15",
    #     "orderNumber":"3048903",
    #     "type":"sell"},
    #    ... ]
    # 
    # Or, for all markets:
    #   {"BTC_NXT":[{"date":"2014-02-19 03:44:59",
    #                "rate":"0.0011",
    #                "amount":"99.9070909",
    #                "total":"0.10989779",
    #                "orderNumber":"3048809",
    #                "type":"sell"},
    #               {"date":"2014-02-19 04:55:44",
    #                "rate":"0.0015",
    #                "amount":"100",
    #                "total":"0.15",
    #                "orderNumber":"3048903",
    #                "type":"sell"},
    #               ... ],
    #    "BTC_LTX":[ ... ],
    #    ... }
    def returnTradeHistory(self, currencyPair, start = None, end = None):
        params = {"currencyPair":currencyPair}
        if start: params["start"] = start
        if end: params["end"] = end
        return self.api_query('returnTradeHistory', params)

    # buy - Places a buy order in a given market.
    #   Required POST parameters are "currencyPair", "rate", and "amount".
    #   If successful, the method will return the order number.
    # 
    # Sample output:
    #   {"orderNumber":31226040,
    #    "resultingTrades":[{"amount":"338.8732",
    #                        "date":"2014-10-18 23:03:21",
    #                        "rate":"0.00000173",
    #                        "total":"0.00058625",
    #                        "tradeID":"16164",
    #                        "type":"buy"}]}
    def buy(self, currencyPair, rate, amount):
        return self.api_query('buy', {"currencyPair":currencyPair, "rate":rate, "amount":amount})

    # sell - Places a sell order in a given market.
    #   Parameters and output are the same as for the buy method.
    def sell(self, currencyPair, rate, amount):
        return self.api_query('sell', {"currencyPair":currencyPair, "rate":rate, "amount":amount})

    # cancelOrder - Cancels an order you have placed in a given market.
    #   Required POST parameter is "orderNumber".
    #   If successful, the method will return:
    # 
    # {"success":1}
    def cancel(self, orderNumber):
        return self.api_query('cancelOrder', {"orderNumber":orderNumber})

    # moveOrder - Cancels an order and places a new one of the same type in a single atomic transaction,
    #   meaning either both operations will succeed or both will fail.
    #   Required POST parameters are "orderNumber" and "rate";
    #   you may optionally specify "amount" if you wish to change the amount of the new order.
    # 
    # Sample output:
    #   {"success":1,
    #    "orderNumber":"239574176",
    #    "resultingTrades":{"BTC_BTS":[]}}
    def moveOrder(self, orderNumber, rate, amount = None):
        params = {"orderNumber":orderNumber, "rate":rate}
        if amount: params["amount"] = amount
        return self.api_query('moveOrder', params)

    # withdraw - Immediately places a withdrawal for a given currency, with no email confirmation.
    #   In order to use this method, the withdrawal privilege must be enabled for your API key.
    #   Required POST parameters are "currency", "amount", and "address".
    #   For XMR withdrawals, you may optionally specify "paymentId".
    # 
    # Sample output:
    #   {"response":"Withdrew 2398 NXT."}
    def withdraw(self, currency, amount, address, paymentId = None):
        params = {"currency":currency, "amount":amount, "address":address}
        if paymentId: params["paymentId"] = paymentId
        return self.api_query('withdraw', params)

    # returnAvailableAccountBalances - Returns your balances sorted by account.
    #   You may optionally specify the "account" POST parameter if you wish to fetch only the balances of one account.
    #   Please note that balances in your margin account may not be accessible if you have any open margin positions or orders.
    # 
    # Sample output:
    #   {"exchange":{"BTC":"1.19042859",
    #                "BTM":"386.52379392",
    #                "CHA":"0.50000000",
    #                "DASH":"120.00000000",
    #                "STR":"3205.32958001",
    #                "VNL":"9673.22570147"},
    #    "margin":  {"BTC":"3.90015637",
    #                "DASH":"250.00238240",
    #                "XMR":"497.12028113"},
    #    "lending": {"DASH":"0.01174765",
    #                "LTC":"11.99936230"}}
    def returnAvailableAccountBalances(self, account = None):
        params = {}
        if (account): params["account"] = account;
        return self.api_query('returnAvailableAccountBalances', params)

    # returnTradableBalances - Returns your current tradable balances for each currency in each market for which margin trading is enabled.
    #   Please note that these balances may vary continually with market conditions.
    # 
    # Sample output:
    #   {"BTC_DASH":{"BTC": "8.50274777",
    #                "DASH":"654.05752077"},
    #    "BTC_LTC" :{"BTC": "8.50274777",
    #                "LTC": "1214.67825290"},
    #    "BTC_XMR" :{"BTC": "8.50274777",
    #                "XMR": "3696.84685650"}}
    def returnTradableBalances(self):
        return self.api_query('returnTradableBalances')

    # transferBalance - Transfers funds from one account to another (e.g. from your exchange account to your margin account).
    #   Required POST parameters are "currency", "amount", "fromAccount", and "toAccount".
    # 
    # Sample output:
    #   {"success":1,"message":"Transferred 2 BTC from exchange to margin account."}
    def transferBalance(self, currency, amount, fromAccount, toAccount):
        return self.api_query('transferBalance', {"currency":currency, "amount":amount, "fromAccount":fromAccount, "toAccount":toAccount})

    # returnMarginAccountSummary - Returns a summary of your entire margin account.
    #   This is the same information you will find in the Margin Account section of the Margin Trading page, under the Markets list.
    # 
    # Sample output:
    #   {"totalValue":          "0.00346561",
    #     "pl":                 "-0.00001220",
    #     "lendingFees":        "0.00000000",
    #     "netValue":           "0.00345341",
    #     "totalBorrowedValue": "0.00123220",
    #     "currentMargin":      "2.80263755"}
    def returnMarginAccountSummary(self):
        return self.api_query('returnMarginAccountSummary')

    # marginBuy - Places a margin buy order in a given market.
    #   Required POST parameters are "currencyPair", "rate", and "amount".
    #   You may optionally specify a maximum lending rate using the "lendingRate" parameter.
    #   If successful, the method will return the order number and any trades immediately resulting from your order.
    # 
    # Sample output:
    #   {"success":        1,
    #    "message":        "Margin order placed.",
    #    "orderNumber":    "154407998",
    #    "resultingTrades":{"BTC_DASH":[{"amount": "1.00000000",
    #                                    "date":   "2015-05-10 22:47:05",
    #                                    "rate":   "0.01383692",
    #                                    "total":  "0.01383692",
    #                                    "tradeID":"1213556",
    #                                    "type":   "buy"}]}}
    def marginBuy(self, currencyPair, rate, amount, lendingRate = None):
        params = {"currencyPair":currencyPair, "rate":rate, "amount":amount}
        if lendingRate: params["lendingRate"] = lendingRate
        return self.api_query('marginBuy', params)

    # marginSell - Places a margin sell order in a given market.
    #   Parameters and output are the same as for the marginBuy method.
    def marginSell(self, currencyPair, rate, amount, lendingRate = None):
        params = {"currencyPair":currencyPair, "rate":rate, "amount":amount}
        if lendingRate: params["lendingRate"] = lendingRate
        return self.api_query('marginSell', params)

    # getMarginPosition - Returns information about your margin position in a given market, specified by the "currencyPair" POST parameter.
    #   You may set "currencyPair" to "all" if you wish to fetch all of your margin positions at once.
    #   If you have no margin position in the specified market, "type" will be set to "none".
    #   "liquidationPrice" is an estimate, and does not necessarily represent the price at which an actual forced liquidation will occur.
    #   If you have no liquidation price, the value will be -1.
    # 
    # Sample output:
    #   {"amount":          "40.94717831",
    #    "total":           "-0.09671314",
    #    "basePrice":       "0.00236190",
    #    "liquidationPrice":-1,
    #    "pl":              "-0.00058655",
    #    "lendingFees":     "-0.00000038",
    #    "type":            "long"}
    def getMarginPosition(self, currencyPair):
        return self.api_query('getMarginPosition', {"currencyPair":currencyPair})

    # closeMarginPosition - Closes your margin position in a given market, specified by the "currencyPair" POST parameter.
    #   This call will also return success if you do not have an open position in the specified market.
    #   
    # Sample output:
    #   {"success":1,
    #    "message":"Successfully closed margin position.",
    #    "resultingTrades":{"BTC_XMR":[{"amount":  "7.09215901",
    #                                   "date":    "2015-05-10 22:38:49",
    #                                   "rate":    "0.00235337",
    #                                   "total":   "0.01669047",
    #                                   "tradeID": "1213346",
    #                                   "type":    "sell"},
    #                                  {"amount":  "24.00289920",
    #                                   "date":    "2015-05-10 22:38:49",
    #                                   "rate":    "0.00235321",
    #                                   "total":   "0.05648386",
    #                                   "tradeID": "1213347",
    #                                   "type":    "sell"}]}}
    def closeMarginPosition(self, currencyPair):
        return self.api_query('closeMarginPosition', {"currencyPair":currencyPair})

    # createLoanOffer - Creates a loan offer for a given currency.
    #   Required POST parameters are "currency", "amount", "duration", "autoRenew" (0 or 1), and "lendingRate".
    # 
    # Sample output:
    #   {"success":1,"message":"Loan order placed.","orderID":10590}
    def createLoanOffer(self, currency, amount, duration, autoRenew):
        return self.api_query('createLoanOffer', {"currency":currency, "amount":amount, "duration":duration, "autoRenew":autoRenew})

    # cancelLoanOffer - Cancels a loan offer specified by the "orderNumber" POST parameter.
    # 
    # Sample output:
    #   {"success":1,"message":"Loan offer canceled."}
    def cancelLoanOffer(self, orderNumber):
        return self.api_query('cancelLoanOffer', {"orderNumber":orderNumber})

    # returnOpenLoanOffers - Returns your open loan offers for each currency.
    # 
    # Sample output:
    #   {"BTC":[{"id":10595,"rate":"0.00020000","amount": "3.00000000","duration":2,"autoRenew":1,"date":"2015-05-10 23:33:50"}],
    #    "LTC":[{"id":10598,"rate":"0.00002100","amount":"10.00000000","duration":2,"autoRenew":1,"date":"2015-05-10 23:34:35"}]}
    def returnOpenLoanOffers(self):
        return self.api_query('returnOpenLoanOffers')

    # returnActiveLoans - Returns your active loans for each currency.
    # 
    # Sample output:
    #   {"provided":[{"id":75073,"currency":"LTC","rate":"0.00020000","amount":"0.72234880",
    #                 "range":2,"autoRenew":0,"date":"2015-05-10 23:45:05","fees":"0.00006000" },
    #                {"id":74961,"currency":"LTC","rate":"0.00002000","amount":"4.43860711",
    #                 "range":2,"autoRenew":0,"date":"2015-05-10 23:45:05","fees":"0.00006000" }],
    #    "used":    [{"id":75238,"currency":"BTC","rate":"0.00020000","amount":"0.04843834",
    #                 "range":2,              "date":"2015-05-10 23:51:12","fees":"-0.00000001"}]}
    def returnActiveLoans(self):
        return self.api_query('returnActiveLoans')

    # toggleAutoRenew - Toggles the autoRenew setting on an active loan, specified by the "orderNumber" POST parameter.
    #   If successful, "message" will indicate the new autoRenew setting.
    # 
    # Sample output:
    #   {"success":1,"message":0}
    def toggleAutoRenew(self, orderNumber):
        return self.api_query('toggleAutoRenew', {"orderNumber":orderNumber})
