contract EthereumBitcoinSwap {
	
	struct TicketData {
		address btcAddr;
		bytes10 numWei;
		bytes2 weiPerSatoshi;
	}
	
	struct ClaimData {
		address claimer;
		bytes2 claimExpiry;
		//hash claimTxHash;
		bytes32 claimTxHash;
	}
	
	struct Ticket {
		TicketData ticketData;
		ClaimData claimData;
	}
	
	// try saving with uint64 ?
	uint private gTicketId = 1;  // start out at 1 to minimize issues where an uninitialized variable leads to a valid ticket
	
	mapping (uint => Ticket) gTicket;
	
	function createTicket(address btcAddr, bytes10 numWei, bytes2 weiPerSatoshi) returns (uint) {
		gTicket[gTicketId].ticketData.btcAddr = btcAddr;
		gTicket[gTicketId].ticketData.numWei = numWei;
		gTicket[gTicketId].ticketData.weiPerSatoshi = weiPerSatoshi;
	}
}
