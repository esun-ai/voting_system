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

from app.exceptions import CustomException
from app.schema.time import TimeChange
from app.models.time import Time
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session


def change_time(request: TimeChange, db: Session):
    try:
        db.query(Time).filter(Time.id == 1).update({"start_time": request.start_time,
                                                    "end_time": request.end_time}
                                                   )
        db.commit()

    except OperationalError:

        raise CustomException(status_code=424, message="DB error")
