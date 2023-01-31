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
from app.exceptions import CustomException
from app.database import get_db
from app.schema.common import Response
from app.schema.time import TimeChange
from app.services import time as service_time
from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

router = APIRouter()

load_dotenv()


@router.post("/change")
def change_time(token: str, request: TimeChange, db: Session = Depends(get_db)):
    """
    更改投票檢查點的時間
    """
    my_token = os.environ.get("MY_TOKEN")
    if token != my_token:
        raise CustomException(status_code=400, message="wrong")
    else:
        service_time.change_time(request, db)
        return Response(data="success")
