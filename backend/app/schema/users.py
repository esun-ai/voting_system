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


class LoginRequest(BaseModel):
    account: str = Field(..., title="帳號", example="admin")
    password: str = Field(..., title="密碼", example="12345678")


class UserCreate(BaseModel):
    account: str = Field(..., title="帳號", example="user")
    password: str = Field(..., title="密碼", example="12345678")
    is_admin: bool = Field(..., title="是否管理者", example=False)
    is_active: bool = Field(..., title="是否啟用", example=True)
