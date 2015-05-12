inset('btcSpecialTx.py')

# TODO
# claimer 20bytes, claimExpiry 2bytes
# claimTxHash are 32bytes each
# btcAddr 20 bytes, numWei 10bytes, weiPerSatoshi 2bytes


extern relayContract: [verifyTx:iiai:i]


data gTicket[2**64](_btcAddr, _numWei, _weiPerSatoshi, _claimer, _claimExpiry, _claimTxHash)

data gTicketId  # lowest possible is 1

data gBtcRelayContract


macro ONE_HOUR_IN_SECS: 60*60
macro EXPIRY_TIME_SECS: 4 * ONE_HOUR_IN_SECS


def createTicket(btcAddr, numWei, weiPerSatoshi):
    if msg.value < numWei || numWei == 0:
        return(0)

    self.gTicketId += 1
    # use var for gTicketId ?
    self.gTicket[self.gTicketId]._btcAddr = btcAddr
    self.gTicket[self.gTicketId]._numWei = numWei
    self.gTicket[self.gTicketId]._weiPerSatoshi = weiPerSatoshi
    # claimData left as zeros

    return(self.gTicketId)


def reserveTicket(ticketId, txHash):
    if (m_ticketIsUnexpired(ticketId) || m_ticketHasDeposit(ticketId)):
        return(0)

    self.gTicket[ticketId]._claimer = msg.sender
    self.gTicket[ticketId]._claimExpiry = block.timestamp + EXPIRY_TIME_SECS
    self.gTicket[ticketId]._claimTxHash = txHash
    return(1)


def claimTicket(ticketId, txStr:str, txHash, txIndex, sibling:arr, txBlockHash):
    if (txHash != self.gTicket[ticketId]._claimTxHash):
        return(0)

    outputData = self.getFirst2Outputs(txStr, outitems=3)

    if outputData == 0:
        log(msg.sender, data=[-30])
        return(0)

    numSatoshi = outputData[0]
    satoshiNeeded = self.gTicket[ticketId]._numWei / self.gTicket[ticketId]._weiPerSatoshi
    if numSatoshi < satoshiNeeded:
        return(0)


    indexScriptOne = outputData[1]

    #TODO strictly compare the script because an attacker may have a script that mentions
    #our BTC address, but the BTC is not spendable by our private key (only spendable by attacker's key)
    # btcWasSentToMe = compareScriptWithAddr(indexScriptOne, txStr, self.btcAcceptAddr)
    addrBtcWasSentTo = getEthAddr(indexScriptOne, txStr, 20, 6)

    if addrBtcWasSentTo != self.gTicket[ticketId]._btcAddr:
        return(0)


    if gBtcRelayContract.verifyTx(txHash, txIndex, sibling, txBlockHash):

        indexScriptTwo = outputData[2]
        ethAddr = getEthAddr(indexScriptTwo, txStr, 20, 6)
        # log(ethAddr)  # exp 848063048424552597789830156546485564325215747452L

        # expEthAddr = text("948c765a6914d43f2a7ac177da2c2f6b52de3d7c")

        # TODO need to get the satoshis of output1 to calc miner fee

        # res = send(ethAddr, ETH_TO_SEND)

        log(msg.sender, data=[res])
        return(res)


    log(msg.sender, data=[-100])
    return(0)



# required deposit is 5% numWei
macro m_ticketHasDeposit($ticketId):
    msg.value < self.gTicket[$ticketId]._numWei / 20

macro m_ticketIsUnexpired($ticketId):
    block.timestamp <= self.gTicket[$ticketId]._claimExpiry



macro getEthAddr($indexStart, $inStr, $size, $offset):
    $endIndex = ($indexStart*2) + $offset + ($size * 2)

    $result = 0
    $exponent = 0
    $j = ($indexStart*2) + $offset
    while $j < $endIndex:
        $char = getch($inStr, $endIndex-1-$exponent)
        # log($char)

        if ($char >= 97 && $char <= 102):  # only handles lowercase a-f
            $numeric = $char - 87
        else:
            $numeric = $char - 48
        # log($numeric)

        $result += $numeric * 16^$exponent
        # log(result)

        $j += 1
        $exponent += 1

    $result