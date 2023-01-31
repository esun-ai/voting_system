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
from app.services import vote as service_vote
from app.models.team import Team
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError


def get_teams(db: Session, gid: str, account: str):

    try:
        teams = db.query(Team).filter(Team.gid == gid).all()
        for t in teams:
            t.voted = service_vote.is_voted(db, account, gid, t.tid)
            t.done = service_vote.check_if_vote(db, account, gid)
        return teams
 
    except OperationalError:

        raise CustomException(status_code=424, message="DB error")
