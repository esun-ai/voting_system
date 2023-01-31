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
from app.exceptions import CustomException
from app.forms.login import LoginForm
from app.schema.common import Response
from app.schema.users import LoginRequest
from app.services import users as service_users
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    '''
    登入帳號
    '''
    form = LoginForm(request)
    form.load_data()
    if form.is_valid():
        user = service_users.login(request=request, db=db)
        if user:
            return Response(data={"status": 200})
    raise CustomException(status_code=403, message=form.errors)
