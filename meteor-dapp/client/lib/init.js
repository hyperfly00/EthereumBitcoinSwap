web3.setProvider(new web3.providers.HttpProvider('http://localhost:8999'));

web3.eth.defaultAccount = web3.eth.coinbase;

ZERO = new BigNumber(0);

TWO_POW_256 = new BigNumber(2).pow(256);

WEI_PER_ETHER = new BigNumber(10).pow(18);
SATOSHI_PER_BTC = new BigNumber(10).pow(8);
WEI_PER_SATOSHI = new BigNumber(10).pow(10);


// useBtcTestnet = false;
// var gOurBtcAddr;

useBtcTestnet = true;
if (useBtcTestnet) {
  gTicketContractAddr = '0x0e19674ebc2c2b6df3e7a1417c49b50235c61924';  // private
  // gTicketContractAddr = '0xb007e8d073af6b6487261bc06660f87ea8740230';
  gVersionAddr = 111;
  //
  // gOurBtcAddr = 'mvBWJFv8Uc84YEyZKBm8HZQ7qrvmBiH7zR';
}
else {
  gTicketContractAddr = '0x668a7adf4cb288d48b5b23e47fe35e8c14c55a81';
  gVersionAddr = 0;

  // from tx190 of block300K
  // hex is 956bfc5575c0a7134c7effef268e51d887ba7015
  // gOurBtcAddr = '1Ed53ZSJiL5hF9qLonNPQ6CAckKYsNeWwJ';
}


// TODO don't forget to update the ABI
gContract = web3.eth.contract(externalEthBtcSwapAbi).at(gTicketContractAddr);
console.log('@@@@ gContract: ', gContract)



$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})
