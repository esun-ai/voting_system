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

from app.database import get_db
from app.schema.common import Response
from app.schema.users import UserCreate
from app.services import users as service_users
from app.services import vote as service_vote
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/userinfo")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    註冊
    """
    userinfo = service_users.create_new_user(user, db)
    return Response(status_code=200, message="success", data=userinfo)


@router.get("/is_voted")
async def vote(account: str, gid: str, db: Session = Depends(get_db)):
    """
    使用者是否投票
    """
    is_voted = service_vote.check_if_vote(db, account, gid)
    return Response(status_code=200, message="success", data=is_voted)


@router.get("/check_user")
async def check_user(account: str, db: Session = Depends(get_db)):
    """
    確認是否為 Admin 用戶
    """
    logined = service_users.check_if_admin(db, account)
    return Response(status_code=200, data=logined)
