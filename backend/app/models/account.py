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

from app.database import Base, schema_name
from sqlalchemy import Boolean, Column, Integer, String


class Account(Base):
    __tablename__ = "account"
    __table_args__ = {"schema": schema_name, "extend_existing": True}
    account = Column(String, primary_key=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    vote_counter = Column(Integer, default=0)
