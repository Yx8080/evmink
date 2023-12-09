import graphlib
import time
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3
from web3.middleware import geth_poa_middleware

class Web3Utils:
    def __init__(self, rpc_url:str,private_key:str):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.account:LocalAccount = Account.from_key(private_key)
        self.address:str = self.account.address
        self.nonce:int = self.w3.eth.get_transaction_count(self.account.address)
        self.gas_price:int = int(self.w3.eth.gas_price * 1) # 可以根据实际情况动态修改比例
        self.chainId:int = self.w3.eth.chain_id
        self.gas = self.w3.eth.estimate_gas

    def estimate_gas(self, txn):
        gas = self.w3.eth.estimate_gas({
            "from": txn['from'],
            "to": txn['to'],
            "value": txn['value'],
            "data": txn['data']
        })
        gas = int(gas + (gas / 10))  # increase 10% of the gas

        txn.update({'gas': int(gas)})

    def send_transaction(self, transaction):
        signer = self.account.sign_transaction(transaction_dict=transaction)
        tx = self.w3.eth.send_raw_transaction(signer.rawTransaction)
        tx_hash =  Web3.to_hex(tx)
        # 检查交易状态
        while True:
            try:
                result = self.w3.eth.get_transaction_receipt(transaction_hash=tx_hash)
                if result is None or result['blockNumber'] is None:
                    time.sleep(3)
                elif result['status']:
                    self.nonce += 1
                    return tx_hash
                else:
                    print(f"[失败] -  https://bscscan.com/tx/{tx_hash}")
                    return False
            except Exception as e:
                print(f"检查交易状态时出错：{e}")
                time.sleep(2)

    def get_range_block(self,startBlock:int,endBlock:int,num:int = None) -> list[str]:
        txHashList = []
        for block_number in range(startBlock,endBlock+1):
            block = self.w3.eth.get_block(block_number,True)
            transactions = block.transactions
            for transaction in transactions:
                fromAddress = transaction['from'].lower()
                toAddress = transaction.to
                if toAddress is not None and toAddress.lower() == fromAddress and fromAddress == self.address.lower():
                    txHashList.append(transaction.hash.hex())
                    print(f'fetched block:{block_number} txHash:{transaction.hash.hex()}')
                    if num is not None and len(txHashList) == num:
                        return txHashList
        return txHashList
    
    def batch_send_transaction(self, startBlock: int, endBlock: int, num: int = None, transaction_handler=None):
        tx_hash = self.get_range_block(startBlock, endBlock, num)

        for hash in tx_hash:
            if self._checkInscriptionValid(hash):
                continue
            if transaction_handler and callable(transaction_handler):
                # 调用传递的方法，传递 hash 作为参数
                transaction_handler(hash)
                
    def _checkInscriptionValid(self,hash:str) -> bool:
        mw_res = graphlib.GetInscriptionByTrxHash(hash).json()
        inscriptions = mw_res.get("data",{}).get("inscriptions",[])
        return (not inscriptions or inscriptions[0].get("owner_address").lower() != self.address.lower())
    