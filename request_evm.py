from collections import defaultdict
import json
import math
import sys
import requests
import copy
import logging
import graphql

from res_data import ResData

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

balance = defaultdict(int)
tx_hash = defaultdict(list)

all_res:list[ResData] = []

def getCount():
    response = graphql.GetUserInscriptions(0,1)
    count_data = response.json().get("data", {})
    total_count = count_data.get("inscriptions_aggregate", {}).get("aggregate", {}).get("count", 0)
    return total_count

def fetch_data():
    global all_res
    total_count = getCount()

    print("总条目数:", total_count)

    logging.info(f"开始铭文归集请稍后.....")

    # 记录每次进度的百分比
    progress_percentage = 0
    offset = math.ceil(total_count / 50) + 1
    rate = 100 / offset
    currentOffset = 0
   # Fetch data in multiple requests with pagination
    while currentOffset < offset:
        response = response = graphql.GetUserInscriptions(currentOffset,50)
        # print(response.json())
        response_data = response.json().get("data", {})
        inscription_data = response_data.get("inscriptions", [])

        if inscription_data:
            inscription_list = [ResData(entry) for entry in inscription_data]
            for mw  in inscription_list:
                if mw.brc20_command_data is not None:
                    all_res.append(mw)

            currentOffset += 1  # Increment offset for the next page

            # 计算当前进度百分比
            progress_percentage += rate
            if progress_percentage > 100 :
                logging.info(f"当前进度: 100%")
            else:
                logging.info(f"当前进度: {progress_percentage:.2f}%")

        else:
            logging.info(f"市场解析完成.....")
            break

def collect():
    global balance
    global tx_hash
    for res_data in all_res:
        content_uris = res_data.content_uri
        content_uri_bytes = bytes.fromhex(content_uris[2:])
        data_json = content_uri_bytes.decode("utf-8")

       
        content_dict = json.loads(data_json.replace("data:,",""))

        
        p_value = content_dict.get("p")
        tick_value = content_dict.get("tick")
        amt_value = content_dict.get("amt")

        
        group_key = (p_value, tick_value)

        
        balance[group_key] += int(amt_value)
        tx_hash[group_key].append(res_data.content_uri)

fetch_data()
collect()