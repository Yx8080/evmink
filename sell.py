import time
import graphql

from web3_utils import Web3Utils

prk = input("请输入私钥")
price = float(input("上架价格(BNB):"))
startBlock = int(input("开始区块:"))
endBlock = int(input("结束区块:"))

marketplace_address = "0x8cda4bF57aF66227d541B728759131bb8137A09C"

web3_utils = Web3Utils("https://rpc.ankr.com/bsc",prk)

def sell(hex:str):
    transaction = {
        "from": web3_utils.address,
        "nonce": web3_utils.nonce,
        "value": 0,
        "gas": 33036,
        "gasPrice": web3_utils.gas_price,
        "to": marketplace_address,
        "chainId": web3_utils.chainId, 
        "data": hex
    }
    
    web3_utils.estimate_gas(transaction)

    web3_utils.send_transaction(transaction)
    print(f"[成功] - https://evm.ink/marketplace/eip155:56/{hex}:0")

def createSellOrder() -> bool:
    response =  graphql.PutOnSale(hash,price)
    data = response.json().get("data", {})
    sell_order_info = data.get("create_sell_order", {})
    return sell_order_info.get("ok", False)

def transfer(hash:str):
    if createSellOrder:
        sell(hash)

if __name__ == '__main__':
    try:
        # py lambda function
        web3_utils.batch_send_transaction(startBlock, endBlock, transaction_handler=transfer)
        print("上架完成...")
        time.sleep(2)
    except Exception as e:
        print("报错信息如下：")
        print(e)
    print("程序执行完毕自动退出")