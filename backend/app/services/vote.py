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

import pandas as pd
from datetime import datetime, timedelta
from app.exceptions import CustomException
from app.models.team import Team
from app.models.vote import Vote
from app.models.time import Time
from app.schema.vote import VoteCreate
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session


def vote(request: VoteCreate, db: Session):
    try:
        vote = Vote(
            account=request.account,
            tid=request.tid,
            gid=request.gid,
        )
        db.add(vote)
        db.commit()
        db.refresh(vote)
        return vote

    except OperationalError:

        raise CustomException(status_code=424, message="DB error")


def vote2who(db: Session, account: str, gid: str):
    try:
        show_name = []
        ticket = db.query(Vote.id, Team.show_name).join(Team, (Vote.gid==Team.gid) & (Vote.tid==Team.tid)).filter(Vote.account == account, Vote.gid == gid).all()
        for i in ticket:
            show_name.append(i["show_name"])
        if len(show_name) == 0:
            return '查無資訊'
        else:
            if len(show_name) > 1:
                return '、'.join(show_name)
            else:
                return show_name[0]
    except OperationalError:

        raise CustomException(status_code=424, message="DB error")


def check_if_vote(db: Session, account: str, gid: str):
    try:
        vote_number = db.query(Vote).filter(Vote.account == account, Vote.gid == gid).count()
        if gid == "歌唱組" and vote_number == 2:
            return True
        elif gid == "才藝組" and vote_number == 1:
            return True
        return False
    except OperationalError:
        raise CustomException(status_code=424, message="DB error")


def is_voted(db: Session, account: str, gid: str, tid: str):
    try:
        vote_number = db.query(Vote).filter(Vote.account == account, Vote.gid == gid, Vote.tid == tid).count()
        if vote_number > 0:
            return True
        else:
            return False

    except OperationalError:

        raise CustomException(status_code=424, message="DB error")


def check_if_timeout(db: Session):
    try:

        current_time = datetime.now() + timedelta(hours=8)
        t = db.query(Time).filter(Time.start_time <= current_time, Time.end_time >= current_time)

    except OperationalError:

        raise CustomException(status_code=424, message="DB error")
    
    if t.first():
        return True
    else:
        return False


def count_vote(db: Session, gid: str):
    """
    計算投票數，可以用來自製長條圖(可以自行實作投票過程中查看長條圖的功能)。
    """
    try:
        sql_string = f"""
                    SELECT a.tid, a.show_name, COUNT(b.account) AS total_number
                    FROM team a left join 
                        (SELECT DISTINCT v.tid, v.account
                        FROM vote v left join account u on v.account=u.account
                        WHERE v.gid = '{gid}'
                        ) b on a.tid=b.tid
                    WHERE a.gid = '{gid}'
                    GROUP BY a.tid, a.show_name
                     """
        votes = db.execute(sql_string).fetchall()
    except OperationalError:
        raise CustomException(status_code=424, message="DB error")
    return votes


def race_vote(db: Session, gid: str):
    '''
    example:

        |           ts         |         show_name           | count 
        -----------------------+-----------------------------+-------
        2022-09-26 01:30:00+00 | 歌曲1                        |     2
        2022-09-26 06:30:00+00 | 歌曲1                        |     1
        2022-09-26 01:30:00+00 | 歌曲2                        |     1
    '''
    try:
        sql_string = f"""
                    select b.show_name, a.created_at
                    from vote a left join team b on (a.gid, a.tid)=(b.gid, b.tid)
                    where a.gid='{gid}'
                     """
        votes = db.execute(sql_string).fetchall()
    except OperationalError:
        raise CustomException(status_code=424, message="DB error")
    return votes


def get_show_names(db: Session, gid: str):
    '''
    example:

        |           ts          |         show_name          | count 
        -----------------------+----------------------------+-------
        2022-09-26 01:30:00+00 | 歌曲1                        |     2
        2022-09-26 06:30:00+00 | 歌曲1                        |     1
        2022-09-26 01:30:00+00 | 歌曲2                        |     1
    '''
    try:
        data = db.query(Team).filter(Team.gid == gid).all()
        show_names = []
        for d in data:
            show_names.append(d.show_name)
        return show_names
    except OperationalError:

        raise CustomException(status_code=424, message="DB error")


def vote_delete(db: Session, account: str):
    try:
        vote_query = db.query(Vote).filter(Vote.account == account)
        # return vote_query.first()
        if vote_query.first() is not None:
            vote_query.delete()
            db.commit()
            return "success"
        else:
            return "NoData"
    except OperationalError:
        raise CustomException(status_code=424, message="DB error")


def create_sql(gid: str):
    sql_string = f"""
            SELECT a.tid, a.show_name, COUNT(b.account) AS total_number
            FROM team a left join
                (SELECT DISTINCT v.tid, v.account
                FROM vote v left join account u on v.account=u.account
                WHERE v.gid = '{gid}'
                ) b on a.tid=b.tid
            WHERE a.gid = '{gid}'
            GROUP BY a.tid, a.show_name
            ORDER BY total_number desc
            """
    return sql_string


def create_csv(db: Session, path: str):
    try:
        df = pd.DataFrame(columns=["編號", "組別", "表演名稱", "得票數"])
        for t in ["歌唱組", "才藝組"]:
            sql_string = create_sql(t)
            stat = db.execute(sql_string).fetchall()
            temp = pd.DataFrame(stat, columns=["編號", "表演名稱", "得票數"])
            temp["組別"] = t
            df = df.append(temp)
        df.to_excel(path, index=False, encoding='utf-8-sig')
        return "success"
    except OperationalError:
        raise CustomException(status_code=424, message="[DB Error] 請聯絡管理者")


def create_csv2(db: Session, path: str):
    try:
        sqlstring1 = '''select count(*) from vote ;'''
        sqlstring2 = '''select count(distinct account) from vote ;'''
        sqlstring3 = ''' select count(*) from vote where gid='歌唱組';'''
        sqlstring4 = ''' select count(*) from vote where gid='才藝組';'''
        stat1 = db.execute(sqlstring1).fetchall()[0].count
        stat2 = db.execute(sqlstring2).fetchall()[0].count
        stat3 = db.execute(sqlstring3).fetchall()[0].count
        stat4 = db.execute(sqlstring4).fetchall()[0].count
        df2 = pd.DataFrame({"類別": ["總票數", "投票人數", "歌唱組票數", "才藝組票數"],
                            "數量": [str(stat1), str(stat2), str(stat3), str(stat4)]
                            })
        df2.to_excel(path, index=False, encoding='utf-8-sig')
        return "success"
    except OperationalError:
        raise CustomException(status_code=424, message="[DB Error] 請聯絡管理者")
