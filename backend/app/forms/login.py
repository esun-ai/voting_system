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

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from typing import List
from app.schema.users import LoginRequest


class LoginForm:
    def __init__(self, request: LoginRequest):
        self.request: LoginRequest = request
        self.errors: List = []

    def load_data(self):
        self.account = self.request.account
        self.password = self.request.password

    def is_valid(self):
        if not self.account or len(self.account) <= 4:
            self.errors.append("esun_id should be at least 5 chars")
        if not self.password or len(self.password) <= 3:
            self.errors.append("Password must be at least 4 chars")
        if not self.errors:
            return True
        return False
