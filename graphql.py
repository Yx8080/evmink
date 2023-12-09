import copy
import requests
from datetime import datetime, timedelta, timezone


url = "https://api.evm.ink/v1/graphql/"  # 请替换为实际的 API 地址
headers = {
    "Content-Type": "application/json",
}

PutOnSale_JSON = {
	"query": "mutation PutOnSale($expire_at: String!, $inscription_id: String!, $inscription_internal_id: Int!, $network_id: String!, $payment_token_address: String!, $price: String!) {\n  create_sell_order(\n    object: {expire_at: $expire_at, inscription_id: $inscription_id, inscription_internal_id: $inscription_internal_id, network_id: $network_id, payment_token_address: $payment_token_address, price: $price}\n  ) {\n    ok\n  }\n}",
	"variables": {
		"expire_at": "",#过期时间
		"inscription_id": "",#铭文铸造hash
		"inscription_internal_id": 0,
		"network_id": "eip155:56",
		"payment_token_address": "0x0000000000000000000000000000000000000000",
		"price": "" #上架金额 * 10*18
	},
	"operationName": "PutOnSale"
}

GetUserInscriptions_JSON = {
    "query": "query GetUserInscriptions($limit: Int, $offset: Int, $order_by: [inscriptions_order_by!] = {}, $where: inscriptions_bool_exp = {}, $whereAggregate: inscriptions_bool_exp = {}) {\n  inscriptions_aggregate(where: $whereAggregate) {\n    aggregate {\n      count\n    }\n  }\n  inscriptions(limit: $limit, offset: $offset, order_by: $order_by, where: $where) {\n    block_number\n    confirmed\n    content_uri\n    created_at\n    creator_address\n    owner_address\n    trx_hash\n    id\n    position\n    category\n    mtype\n    internal_trx_index\n    network_id\n    brc20_command {\n      reason\n      is_valid\n    }\n  }\n}",
    "variables": {
        "limit": 50,
        "offset": 1,
        "order_by": [
            {
                "position": "desc"
            }
        ],
        "whereAggregate": {
            "owner_address": {
                "_eq": "0x67c60c3f028ef4ff82de53189f236388ca7a5f6a"
            },
            "network_id": {
                "_eq": "eip155:56"
            },
            "brc20_command": {
                "is_valid": {
                    "_eq": "true"
                }
            }
        },
        "where": {
            "position": {
                # "_lt": "64339249"
            },
            "owner_address": {
                "_eq": "0x67c60c3f028ef4ff82de53189f236388ca7a5f6a"
            },
            "network_id": {
                "_eq": "eip155:56"
            },
            "brc20_command": {
                "is_valid": {
                    "_eq": "true"
                }
            }
        }
    },
    "operationName": "GetUserInscriptions"
}

GetInscriptionByTrxHash_JSON = {
    "query": "query GetInscriptionByTrxHash($where: inscriptions_bool_exp = {}) {\n  inscriptions(where: $where, limit: 1) {\n    block_number\n    confirmed\n    content_uri\n    created_at\n    creator_address\n    id\n    position\n    owner_address\n    trx_hash\n    category\n    mtype\n    internal_trx_index\n    network_id\n    sell_order {\n      created_at\n      expire_at\n      extra\n      payment_token {\n        address\n        decimals\n        decimla_digits\n        usd_price\n      }\n      seller_address\n      price\n    }\n    brc20_command {\n      reason\n      is_valid\n    }\n    ci {\n      collection {\n        name\n        slug\n      }\n    }\n  }\n}",
    "variables": {
        "where": {
            "trx_hash": {
                "_eq": "" #hash
            },
            "network_id": {
                "_eq": "eip155:56"
            },
            "internal_trx_index": {
                "_eq": "0"
            }
        }
    },
    "operationName": "GetInscriptionByTrxHash"
}

def GetUserInscriptions(offset:int,limit:int):
    initial_data = copy.deepcopy(GetUserInscriptions_JSON)
    initial_data["variables"]["offset"] = offset  # 初始 offset
    initial_data["variables"]["limit"] = limit
    return requests.post(url, headers=headers, json=GetUserInscriptions_JSON)

def PutOnSale(tx_hash:str,price:float):
    initial_data = copy.deepcopy(PutOnSale_JSON)
    # 获取当前时间
    current_time = datetime.utcnow()  # 使用UTC时间
    # 添加24小时
    new_time = current_time + timedelta(hours=24)
    # 格式化新时间为字符串
    formatted_time = new_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    to_price = int(price * 10**18)

    initial_data["variables"]["expire_at"] = formatted_time  # 初始 offset
    initial_data["variables"]["inscription_id"] = tx_hash
    initial_data["variables"]["price"] = str(to_price)

    headers.update({"Authorization": "Bearer "+" "}) # 填充实际的token

    return requests.post(url, headers=headers, json=initial_data)

def GetInscriptionByTrxHash(hash:str):
    initial_data = copy.deepcopy(GetInscriptionByTrxHash_JSON)
    initial_data["variables"]["where"]["trx_hash"]["_eq"]  = hash  # 初始 offset
    return requests.post(url, headers=headers, json=GetUserInscriptions_JSON)