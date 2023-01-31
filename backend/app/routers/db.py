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

from app.database import Base, engine, get_db
from app.schema.common import Response
from app.models import team, account, time
from fastapi import APIRouter
from passlib.context import CryptContext
import datetime

router = APIRouter()


@router.get("/init")
async def init():
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    objects = [
        account.Account(
                  account="admin",
                  hashed_password=CryptContext(schemes=["bcrypt"], deprecated="auto").hash('12345678'),
                  is_admin=True),
        team.Team(gid="歌唱組",
                  tid=1,
                  name=['參賽者1'],
                  show_name="歌曲1",
                  feat=['feat歌手1']),
        team.Team(gid="歌唱組",
                  tid=2,
                  name=['參賽者2'],
                  show_name="歌曲2",
                  feat=[]),
        team.Team(gid="歌唱組",
                  tid=3,
                  name=['參賽者3', '參賽者4'],
                  show_name="歌曲3",
                  feat=['feat歌手2']),
        team.Team(gid="歌唱組",
                  tid=4,
                  name=['參賽者5'],
                  feat=['feat歌手3', 'feat歌手4'],
                  show_name="歌曲4"),
        team.Team(gid="才藝組",
                  tid=1,
                  name=['參賽者6', '參賽者7'],
                  show_name="才藝1",
                  show_type="小提琴"),
        team.Team(gid="才藝組",
                  tid=2,
                  name=['參賽者8', '參賽者9', '參賽者10'],
                  show_name="才藝2",
                  show_type="街舞"),
    ]
    for object in objects:
        db.add(object)
        db.commit()
    # 初始化投票時間為啟動 DB 時間的13點～17點30分
    tmp = time.Time(id=1, start_time=datetime.datetime.combine(datetime.date.today(), datetime.time(13, 0)),
                    end_time=datetime.datetime.combine(datetime.date.today(), datetime.time(17, 30)))
    db.add(tmp)
    db.commit()

    return Response(data={"msg": "success"})
