
import time
from web3_utils import Web3Utils

prk = input("请输入私钥")
receipt = input("需要转账地址:")
num = int(input("转账数量:"))
startBlock = int(input("开始区块:"))
endBlock = int(input("结束区块:"))

web3_utils = Web3Utils("https://rpc.ankr.com/bsc",prk)

transfer_count = 0

def transfer(hex:str):
    global transfer_count
    transaction = {
        "from": web3_utils.address,
        "nonce": web3_utils.nonce,
        "value": 0,
        "gas": 33036,
        "gasPrice": web3_utils.gas_price,
        "to": receipt,
        "chainId": web3_utils.chainId, 
        "data": hex
    }
    
    web3_utils.estimate_gas(transaction)

    tx = web3_utils.send_transaction(transaction)
    transfer_count += 1
    print(f"[成功-{transfer_count}] - https://bscscan.com/tx/{tx}")

if __name__ == '__main__':
    try:
        # py lambda function
        print("正在准备中请稍后....")
        web3_utils.batch_send_transaction(startBlock, endBlock, transaction_handler=transfer)
        print("转账完成...")
        time.sleep(2)
    except Exception as e:
        print("报错信息如下：")
        print(e)
    print("程序执行完毕自动退出")