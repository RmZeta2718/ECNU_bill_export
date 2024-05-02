# -*-coding:utf-8-*-
import json
import time

import requests
from objprint import op

import config

BILL_URL = "https://epay.ecnu.edu.cn/openservice/miniprogram/getbilldata"
headers = {
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E217 MicroMessenger/6.8.0(0x16080000) NetType/WIFI Language/en Branch/Br_trunk MiniProgramEnv/Mac",
    "content-type": "application/json",
    "Referer": "https://servicewechat.com/wx8baadd3d2289f1a7/11/page-frame.html",
    "Accept-Encoding": "gzip, deflate, br",
    "sw-Authorization": config.session_key,
}

s = requests.session()


# bills from year/month/02 to year/month+1/01
def GetBill(year: int, month: int) -> list[dict]:
    pagesize = 1000
    req_data = {
        "startdate": f"{year:4d}{month:02d}02",
        "enddate": f"{year if month < 12 else year + 1:4d}{month + 1 if month < 12 else 1:02d}01",
        "pageno": 1,
        "pagesize": pagesize,
    }
    req = s.post(BILL_URL, data=json.dumps(req_data), headers=headers)
    resp = json.loads(req.content)

    # sanity check
    # op(req_data)
    assert "retcode" in resp and resp["retcode"] == "0", op(resp)
    assert resp["data"]["retcode"] == 0, op(resp)
    data = resp["data"]["data"]
    assert data["totalCount"] < pagesize and data["lastPage"] == True, op(data)  # fit into one request

    rst = [
        {
            "amount": -item["amount"],  # consumption is neg in ECard billing, we need positive
            "shopname": item["shopname"],
            "termname": item["termname"] if "termname" in item else "unknown",  # some item has no termname
            "time": item["paytime"],
        }
        for item in data["list"]
        if item["tradetype"] == 2
    ]  # consumption only

    return rst


def GetYearBill(year: int, ms: int, me: int) -> list[dict]:
    rst = []
    for month in range(ms, me + 1):
        rst += GetBill(year, month)
    return rst


if __name__ == "__main__":  # test
    op.config(color=True, line_number=True, arg_name=True)

    year = 2024
    month = 4
    op(GetBill(year, month))
    # print(json.dumps(GetYearBill(year, 1, 13), ensure_ascii=False))
