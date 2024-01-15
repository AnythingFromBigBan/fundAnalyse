# coding: utf-8

import sqlite3
import time

import requests
import datetime
import json
import os

class get_sqlite_conn:
    def __init__(self):
        self.conn = None
    def __enter__(self):
        self.conn = sqlite3.connect('database.db')
        return self
    @property
    def cursor(self):
        if not self.conn:
            raise RuntimeError("connection is closed")

        return self.conn.cursor()

    def execute(self, *args, **kwargs):
        return self.cursor.execute(*args, **kwargs)

    def commit(self):
        if not self.conn:
            raise RuntimeError("connection is closed")

        self.conn.commit()

    def rollback(self):
        if not self.conn:
            raise RuntimeError("connection is closed")

        self.conn.rollback()

    def close(self):
        if self.conn:
            self.conn.close()



    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type:
                print("exception occured", exc_type.__name__)

            else:
                self.commit()
        finally:
            self.close()

def get_all_stocks():
    time_stamp = str(time.time()*1000)[:13]
    today_time = datetime.datetime.today().strftime("%Y-%m-%d")
    url = f"https://push2delay.eastmoney.com/api/qt/clist/get?cb=jQuery112301342499897570688_{time_stamp}&fid=f62&po=1&pz=86&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A90+t%3A2&fields=f12%2Cf14%2Cf2%2Cf3%2Cf62%2Cf184%2Cf66%2Cf69%2Cf72%2Cf75%2Cf78%2Cf81%2Cf84%2Cf87%2Cf204%2Cf205%2Cf124%2Cf1%2Cf13"
    rsp = requests.get(url).text[len(f"jQuery112307365151583797447_{time_stamp}("): -2]
    data = json.loads(rsp)["data"].get("diff")
    all_stocks = {}
    for item in data:
        all_stocks[item.get("f12")] = {
            "bankuai_name":item.get("f14"),
            "up_down":item.get("f3"),
            "big_money_in":item.get("f62"),
            "little_money_out":item.get("f84")
        }
    print(json.dumps(all_stocks,indent=4,ensure_ascii=False))

def masure_fund():
    """
    以基金公司为单位 分析平均评级
    收集每个 基金的分红，经理变更，规模，风格
    进行加权评分
    :return:
    """
    pass
if __name__ == '__main__':
    pass