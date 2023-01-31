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

from pydantic import BaseModel, Field
import datetime


class TimeChange(BaseModel):
    start_time: datetime.datetime = Field(..., title="開始時間", example="2022-10-01 13:00:00")
    end_time: datetime.datetime = Field(..., title="結束時間", example="2022-10-01 17:30:00")
