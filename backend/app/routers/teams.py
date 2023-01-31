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

import os
from app.database import get_db
from app.exceptions import CustomException
from app.services import teams as service_teams
from app.schema.common import Response
from app.schema.team import Request
from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi import Depends, Header
from sqlalchemy.orm import Session

router = APIRouter()

load_dotenv()


@router.post("/get_menu")
def get_menu(request: Request, token: str = Header(None), db: Session = Depends(get_db)):
    '''
    依照 gid 拿取參賽隊伍資訊
    '''
    my_token = os.environ.get("MY_TOKEN")
    if token != my_token:
        raise CustomException(status_code=400, message="wrong")
    result = service_teams.get_teams(db, request.gid, request.account)
    return Response(data=result)
