# -*- coding:utf-8 -*-
# Copyright (C) 2023  E.SUN BANK.
# @Author: Hsin-Hsien Ho, Wan-Chu Lin
# @Date: 2023/01
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import datetime
import os
import pandas as pd
from app.database import get_db
from app.exceptions import CustomException
from app.schema.common import Response
from app.schema.vote import VoteCreate
from app.services import vote as service_vote
from app.services import users as service_users
from app.models.time import Time
from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi import Depends, Header
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

router = APIRouter()

load_dotenv()

@router.get("/now")
def get_now(db: Session = Depends(get_db)):
    """
    拿 Server 的時間, datetime.now 為台灣時區 GMT 時間, 透過 timedelta + 8 個小時回傳給前端
    """
    result = {}
    now_GMT = datetime.datetime.now()
    eight_hour = datetime.timedelta(hours=8)
    now = now_GMT + eight_hour
    result["now"] = now
    result["start_time"] = db.query(Time.start_time).filter(Time.id == 1).first().start_time + datetime.timedelta(hours=-8)
    result["end_time"] = db.query(Time.end_time).filter(Time.id == 1).first().end_time + datetime.timedelta(hours=-8)
    return Response(data=result)


@router.get("/who")
def vote2who(account: str, gid: str, db: Session = Depends(get_db)):
    """
    查詢投票給誰
    """
    result = service_vote.vote2who(db, account, gid)
    return Response(data=result)


@router.post("/vote")
async def vote(request: VoteCreate, token: str = Header(None), db: Session = Depends(get_db)):
    '''
    投票 \n
    Args: \n
        { \n
            "account": "12345", \n
            "tid": 1, \n
            "gid": "歌唱組" \n
        } \n
    Returns: \n
        { \n
        "error": false, \n
        "data": { \n
            "id": 2, \n
            "gid": "才藝組", \n
            "created_at": "2022-08-08T05:47:43.219389+00:00", \n
            "account": "12345", \n
            "tid": 2 \n
            } \n
        } \n
    } \n
    '''
    my_token = os.environ.get("MY_TOKEN")
    if token != my_token:
        raise CustomException(status_code=400, message="wrong")
    if not service_vote.check_if_timeout(db):
        return Response(status_code=424, message="stop")

    if request.gid not in ["歌唱組", "才藝組"]:
        raise CustomException(status_code=424, message="gid is wrong")
    is_voted = service_vote.check_if_vote(db, request.account, request.gid)

    if not is_voted:
        try:
            service_users.add_vote_counter(db, request.account)
            vote = service_vote.vote(request, db)
            return Response(status_code=200, message="success", data=vote)

        except CustomException:
            raise CustomException(status_code=424, message="[DB Error] vote")

    else:
        return Response(status_code=424, message="voted")


@router.get("/race")
async def prod_race(gid, db: Session = Depends(get_db)):
    '''
    正式計算投票統計賽跑圖 \n
    Args: \n
        gid: 歌唱組 or 才藝組 \n
    '''
    result = {}
    try:
        # 可以自行設定開始、結束時間
        start = datetime.datetime.combine(datetime.date.today(), datetime.time(13, 0))
        end = datetime.datetime.now() + datetime.timedelta(hours=8.5)
        delta = datetime.timedelta(minutes=30)
        t = start
        hours = []
        hours_format = []
        while t <= end:
            hours.append(t)
            hours_format.append(t.strftime("%H%M"))
            t += delta
        result["hours"] = hours_format
        # get team list
        teams = service_vote.get_show_names(db, gid)
        result["teams"] = teams
        # get vote data
        vote_data = service_vote.race_vote(db, gid)
        # counting
        value = {}
        df = pd.DataFrame(vote_data, columns=["show_name", "created_at"])
        df['created_at'] = pd.to_datetime(df['created_at']) + pd.Timedelta(hours=8)
        for h in hours:
            temp = []
            for t in teams:
                total = len(df[df["created_at"].dt.time <= h.time()])
                count = len(df[(df["show_name"] == t) & (df["created_at"].dt.time <= h.time())])
                if total == 0:
                    ratio = 0
                else:
                    ratio = round((count / total) * 100, 2)
                temp.append(ratio)
            value[h.strftime("%H%M")] = temp
        result["value"] = value

    except CustomException as e:
        print(e)
        raise CustomException(status_code=424, message="[DB Error] Vote count")

    return Response(data=result)


@router.get("/race/sing")
async def vote_race_sing():
    '''
    投票統計賽跑圖歌唱組測資 \n
    '''
    result = {}
    try:
        result["teams"] = ["歌曲1", "歌曲2", "歌曲3", "歌曲4", "歌曲5", "歌曲6"]
        result["hours"] = ["1300", "1330", "1400", "1430", "1500", "1530", "1600", "1630", "1700", "1730", "1800", "1830"]
        result["value"] = {"1300": [0, 0, 0, 0, 0, 0],
                           "1330": [10.1, 0.3, 20.4, 10.8, 4.3, 3.9],
                           "1400": [10.45, 20.1, 10, 10, 5, 3],
                           "1430": [24.67, 11.3, 30, 20, 7, 0],
                           "1500": [15.89, 10.1, 40.3, 22.2, 8.3, 8.31],
                           "1530": [10.41, 13.4, 34, 21.12, 10, 11],
                           "1600": [14.31, 10.3, 36.41, 15.41, 10, 12],
                           "1630": [20.12, 10.4, 30.4, 11, 16, 17],
                           "1700": [14.12, 24.57, 30.4, 14, 14, 17],
                           "1730": [13.45, 28, 25, 17.13, 10.3, 14],
                           "1800": [12.67, 35.41, 23, 12, 16.3, 13.31],
                           "1830": [18.4, 30.4, 28.4, 18.23, 17.1, 10.3]}
    except CustomException as e:
        print(e)
        raise CustomException(status_code=424, message="[DB Error] Vote count")

    return Response(data=result)


@router.get("/race/talent")
async def vote_race_talent():
    '''
    投票統計賽跑圖才藝組測資 \n
    '''
    result = {}
    try:
        result["teams"] = ["才藝1", "才藝2", "才藝3", "才藝4"]
        result["hours"] = ["1300", "1330", "1400", "1430", "1500", "1530", "1600", "1630", "1700", "1730", "1800", "1830"]
        result["value"] = {"1300": [0, 0, 0, 0],
                           "1330": [10.2, 10.1, 10.3, 10.1],
                           "1400": [14.3, 0, 0, 14.1],
                           "1430": [15, 6.13, 4, 15],
                           "1500": [17.6, 3.7, 3.9, 6],
                           "1530": [19, 8.12, 4, 10],
                           "1600": [19, 6, 5, 13.3],
                           "1630": [12, 9, 6.3, 7],
                           "1700": [15, 13, 9.31, 9.6],
                           "1730": [14, 12.3, 10.1, 8],
                           "1800": [12, 11.6, 11.41, 13],
                           "1830": [15, 10, 13, 17.31]}

    except CustomException as e:
        print(e)
        raise CustomException(status_code=424, message="[DB Error] Vote count")

    return Response(data=result)


@router.get("/delete")
async def vote_delete(token: str, account: str, db: Session = Depends(get_db)):
    '''
    刪除投票
    '''
    if token != "your-token":
        raise CustomException(status_code=400, message="wrong")
    try:
        status = service_vote.vote_delete(db, account)
        return Response(data=status)
    except CustomException:
        raise CustomException(status_code=424, message="[DB Error] Vote delete")


@router.get("/download")
async def vote_download(db: Session = Depends(get_db)):
    '''
    下載各組投票結果，計算各組的得票數
    '''
    try:
        path = "app/assets/stat.xlsx"
        service_vote.create_csv(db, path)
        if os.path.exists(path):
            headers = {'Content-Type': 'application/vnd.ms-excel'}
            return FileResponse(path, filename='stat.xlsx', headers=headers)
    except CustomException as e:
        print(e)
        raise CustomException(status_code=424, message="[DB Error] Vote delete")


@router.get("/download2")
async def vote_download2(db: Session = Depends(get_db)):
    '''
    下載投票總覽，包含計算總票數、投票人數、歌唱組投票數、才藝組投票數
    '''
    try:
        path = "app/assets/stat2.xlsx"
        service_vote.create_csv2(db, path)
        if os.path.exists(path):
            headers = {'Content-Type': 'application/vnd.ms-excel'}
            return FileResponse(path=path, filename="stat2.xlsx", headers=headers)
    except CustomException:
        raise CustomException(status_code=424, message="[DB Error] Vote delete")


@router.get("/count")
async def vote_count(gid, db: Session = Depends(get_db)):
    '''
    投票統計 \n
    Args: \n
        gid: 歌唱組 or 才藝組 \n
    Return: \n
            { \n
            "error": false, \n
            "data": { \n
                "tid": [ 1, 3, 4 ], \n
                "vote_number": [ 3, 1, 1 ] \n
                    } \n
            } \n
    '''
    result = {}
    tid = []
    show_name = []
    total_number = []
    try:
        # total 
        votes = service_vote.count_vote(db, gid)
        for v in votes:
            tid.append(v.tid)
            show_name.append(v.show_name)
            total_number.append(v.total_number)
        result["tid"] = tid
        result["show_name"] = show_name
        result["total_number"] = total_number
    except CustomException as e:
        print(e)
        raise CustomException(status_code=424, message="[DB Error] Vote count")

    return Response(data=result)
